import tmdb
import requests
import pymongo
import os
from PIL import Image
from StringIO import StringIO

# config
api_key = '2eceb4866c7ff0659613dc805c591232'
mongo_db_name = "tmdb_cache"
img_dl_path = "/tmp/image_cache"

# init tmdb
tmdb.configure(api_key)

# init mongo
mongo_client = pymongo.MongoClient()
mongo_db = mongo_client[mongo_db_name]

# mongo collections
movie_queries = mongo_db.movie_queries
movies = mongo_db.movies


def __cache_image(path):
    img_name = os.path.basename(path)
    r = requests.get(path)
    i = Image.open(StringIO(r.content))
    destination = os.path.join(os.path.abspath(img_dl_path),
                               img_name)
    i.save(destination)
    return destination


def __movie_to_dict(movie):
    return {
        'is_adult': movie.is_adult(),
        'collection_id': movie.get_collection_id(),
        'collection_name': movie.get_collection_name(),
        'collection_backdrop': __cache_image(movie.get_collection_backdrop()),
        'collection_poster': __cache_image(movie.get_collection_poster()),
        'budget': movie.get_budget(),
        'genres': movie.get_genres(),
        'homepage': movie.get_homepage(),
        'imdb_id': movie.get_imdb_id(),
        'runtime': movie.get_runtime(),
        'vote_average': movie.get_vote_average(),
        'vote_count': movie.get_vote_count(),
        'backdrop': __cache_image(movie.get_backdrop()),
        'popularity': movie.get_popularity(),
        'release_date': movie.get_release_date(),
        'title': movie.get_title(),
        'poster': __cache_image(movie.get_poster()),
    }


def reset_cache():
    movie_queries.drop()


def movie_details(movie_id):
    r = movies.find_one({'_id': movie_id})
    if r:
        print "cachte hit for movie details " + r['value']['title']
        return r['value']
    else:
        m = __movie_to_dict(tmdb.Movie(movie_id))
        movies.insert({'_id': movie_id,
                              'value': m})
        return m


def find_movies(query):
    r = movie_queries.find_one({'_id': query})
    if r:
        print "cache hit for " + query
        return r['result']
    else:
        print "searching tmdb for " + query
        movies = list(tmdb.Movies(query).iter_results())
        movie_queries.insert({'_id': query,
                              'result': movies})
        return movies

# reset_cache()
movie_data = find_movies('Iron Man (2008)')[0]
movie = movie_details(movie_data['id'])
print movie
