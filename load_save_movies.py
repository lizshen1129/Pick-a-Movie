import json

MOVIES_DICT_NAME = 'movies.json'


def load_movies():
    try:
        movies_file = open(MOVIES_DICT_NAME, 'r')
        movies = movies_file.read()
        movies_dict = json.loads(movies)

        movies_file.close()
    except:
        movies_dict = {}
    return movies_dict


def save_movies(movies):
    json_file = open(MOVIES_DICT_NAME, "w")
    json.dump(movies, json_file)
    json_file.close()