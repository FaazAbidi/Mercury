import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import difflib
from concurrent.futures import ThreadPoolExecutor
import os

spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID')
spotify_client_skey = os.getenv('SPOTIFY_CLIENT_SKEY')

spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        spotify_client_id, spotify_client_skey
    )
)


def search_shows(query):
    spotify_result = spotify.search(query,limit=5,type='show',market='US',offset=0)

    result = []

    for each in spotify_result['shows']['items']:
        if each is not None:
            single_result = {}

            single_result['title'] = each['name']
            single_result['creators'] = [each['publisher']]
            single_result['image'] = each['images'][0]['url']
            single_result['url'] = each['external_urls']['spotify']
            single_result['medium'] = 'podcast'

            result.append(single_result)
            del single_result

    return result

def search_podcast_episode(query):
    spotify_result = spotify.search(query,limit=5,type='episode',market='US',offset=0)
    result = []

    for each in spotify_result['episodes']['items']:
        single_result = {}

        if each is not None:
            idd = each['id']
            single_result['title'] = each['name']
            single_result['image'] = each['images'][0]['url']
            single_result['url'] = each['external_urls']['spotify']
            single_result['medium'] = 'podcast_episode'
            creators = spotify.episode(idd,market='US')
            single_result['creators'] = [creators['show']['publisher']]

            result.append(single_result)
            del single_result


    return result


def search_podcast(query):

    pool = ThreadPoolExecutor(max_workers=2)
    shows = pool.submit(search_shows, query).result()
    show_episodes = pool.submit(search_podcast_episode, query).result()

    main_result = shows+show_episodes

    if main_result:
        result_size = len(main_result)
    else:
        result_size = 1

    relevance_sort = difflib.get_close_matches(
        query, [x["title"] for x in main_result], n=result_size, cutoff=0
    )

    final = []
    added = []

    for rel_sorted in relevance_sort:
        for result in main_result:
            if (
                result["title"] == rel_sorted
                and len(final) < 10
                and rel_sorted not in added
            ):
                final.append(result)
                added.append(rel_sorted)
                break

    del relevance_sort
    del added

    return final