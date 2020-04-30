Data Enrichment Service *OPENSOURCE PROJECT*

We are creating a service for grabbing relevant data from any webpage. Optimization is a major part of this project. Our current appraoch
includes a Flask app that accepts url and returns Open graph tags. For now, this is only valid for sites following the Open Graph protocol.

Up and running at: https://enrich-data.herokuapp.com/

How to use: https://enrich-data.herokuapp.com/get?= [add your url here] 

Sample Youtube Video: https://enrich-data.herokuapp.com/get?url=https://www.youtube.com/watch?v=dzqpfu5izjE

Note: First request can take a bit longer as the server sleeps after 30mins of inactivity.