"""
A the movie db cache layer that stores the values in the configured
mongo db and local image path.
"""
import tmdb
import requests
import pymongo
import os
from sh import rm, mkdir
from PIL import Image
from StringIO import StringIO

# config
try:
    api_key = os.environ['TMDB_API_KEY']
    tmdb.configure(api_key)
except KeyError as e:
    print "You need to set the environment variable TMDB_API_KEY to your the movie db key."
    raise e

try:
    mongo_db_name = os.environ['MONGO_MEDIA_INFO_MONGO_DB']
    mongo_client = pymongo.MongoClient()
    mongo_db = mongo_client[mongo_db_name]

    # mongo collections
    movie_queries = mongo_db.movie_queries
    movies = mongo_db.movies

except KeyError as e:
    print "You need to configure the mongo db to use by setting the environment variable MONGO_MEDIA_INFO_MONGO_DB."
    raise e

try:
    img_cahe_dir = os.environ['MONGO_MEDIA_INFO_IMG_CACHE_DIR']
except KeyError as e:
    print "You need to configure a path to download images to. Plear set the environment variable MONGO_MEDIA_INFO_IMG_CACHE_DIR."
    raise e


def __image_cache_dir():
    return os.path.abspath(img_cahe_dir)


def __cache_image(path):
    img_name = os.path.basename(path)
    r = requests.get(path)
    i = Image.open(StringIO(r.content))
    destination = os.path.join(__image_cache_dir(),
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
    """
    Resets the cache.

    This drops all the mongo db collections used as well as
    deletes all the images downloaded.
    """
    movie_queries.drop()
    movies.drop()
    rm('-r', __image_cache_dir())
    mkdir('-p', __image_cache_dir())


def movie_details(movie_id):
    """
    Fetch the details for a given movie id.

    This will prefer the cache, if its not in the cache tmdb is queried,
    which takes mutch more time. In that case it also donwloads all the
    relevant images, poster / backdrop / ... .

    You should run warm_cache() in a batch job beforhand if you can
    anticipate which movies will probably be queried for.
    """
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
    """
    Query the movie db. Best results are obtained by "Moviename (year)".

    This will prefer the cache. If its not found in the cache tmdb will
    be queried, which take much more time.

    You can prevent this my running warm_cache() as batch process
    beforhand.
    """
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


def warm_cache(movie_names):
    """
    Given a list of movie queries, this will fetch and cache all the
    results for each query and download and cache all the details of
    each movie found.

    Run this as a worker process so to speed up calls during runtime.
    """
    for movie_name in movie_names:
        for movie in find_movies(movie_name):
            movie_details(movie['id'])
