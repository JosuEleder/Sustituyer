import sys
sys.path.insert(0, '..')

from sustituyer_main import procesafrase
import re

with open("../data/movies.txt", "r") as movies:
    for movie in movies:
        movievalues = movie.split("\t")
        print(movievalues[0])
        nuevamovie = procesafrase(movie[0].rstrip())
        if not(movie[0].rstrip().lower() == nuevamovie.lower()): print(movie[0].rstrip())
