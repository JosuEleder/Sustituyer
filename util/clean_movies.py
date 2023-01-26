import sys, os
sys.path.insert(0, '..')
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

from sustituyer_main import procesafrase
import re
import yaml

movies = []
nuevasmovies = []
movie = {}
with open(ROOT_DIR + "/data/moviesFARichi.yml", "r") as stream:
    movies = yaml.safe_load(stream)
    for movie in movies:
        nuevamovie = procesafrase(movie["name"])
        if not(movie["name"].lower() == nuevamovie.lower()):
            nuevasmovies.append(movie)

def write_yaml(data):
    """ A function to write YAML file"""
    with open(ROOT_DIR + '/data/moviesFARichi_clean.yml', 'w') as f:
        yaml.dump(data, f, allow_unicode=True)

write_yaml(nuevasmovies)


