# mongo-media-info

A store for media meta data, like ratings / posters / ... . Data is fetched from the movie db and cached in a local mongo db.

## dependencies

- mongo db
- pymongo
- sh
- PIL
- requests
- tmdb


## usage

```python
import mongo_media_info

query_result = mongo_media_info.find_movies("Iron Man (2008)")
movie = mongo_media_info.movie_details(query_result[0]['id'])
```


## installation

You will need a working [mongoDB](http://www.mongodb.org/) setup and a valid [movie db api key](http://www.themoviedb.org/documentation/api).

Run this to install all the python dependencies and the library.

```
pip install -e 'git+https://github.com/doganaydin/themoviedb.git@master#egg=tmdb'
pip install -e 'git+https://github.com/Velrok/mongo-media-info.git@master#egg=mongo_media_info'
```

After that you need to set the following environment variables according to your needs:

```
export TMDB_API_KEY="your-api-key"
export MONGO_MEDIA_INFO_MONGO_DB="movie_media_cache"
export MONGO_MEDIA_INFO_IMG_CACHE_DIR="/tmp/image_cache"
```