import sys
sys.path.insert(0, '..')

from sustituyer_main import procesafrase
import re

with open("../data/movies.txt", "r") as movies:
    for movie in movies:
        movievalues = movie.split("\t")
        nuevamovie = procesafrase(movie[0].strip())
        if not(movievalues[0].strip().lower() == nuevamovie.lower()):
            print(movievalues[0].strip() +"\t"+ movievalues[1].strip() +"\t"+ movievalues[2].strip())
