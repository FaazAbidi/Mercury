import requests
import typing
from bs4 import BeautifulSoup, SoupStrainer
from typing import Dict
from constants import google_url

def create_url(query: str) -> str:
    url = google_url + query
    return url

def get_response(url: str):
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
        }
    response = requests.get(url, headers = headers)
    return response.text

def parse_links_and_titles(page, query):
    links = []
    titles = []
    bsoup = BeautifulSoup(page, 'lxml', parse_only=SoupStrainer(class_="r")).find_all('div', class_="r")
    for i in bsoup:
        x = i.find('a')
        links.append(x['href'])
        title = x.find('h3')
        titles.append(title.text if title else x.text)
    return links, titles

def get_google_links_and_titles(query: str) -> Dict:
    data = []
    url = create_url(query)
    page = get_response(url)
    links, titles = parse_links_and_titles(page, query)
    if len(links) > 10:
        links = links[:10]
        titles = titles[:10]

    for i, item in enumerate(links):
        data.append({'url': item, 'title': titles[i]})

    return data
