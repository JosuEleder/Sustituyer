from sustituyer_main import procesafrase
import re

with open("data/movies.txt", "r") as movies:
    for movie in movies:
        nuevamovie = procesafrase(movie.rstrip())
        if not(movie.rstrip().lower() == nuevamovie.lower()): print(movie.rstrip())
