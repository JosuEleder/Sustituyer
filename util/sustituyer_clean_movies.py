import sys, os
sys.path.insert(0, '..')
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

from sustituyer_main import procesafrase
import re

with open(ROOT_DIR + "/data/moviesFARichi.txt", "r") as movies:
    for movie in movies:
        movievalues = movie.split("\t")
        nuevamovie = procesafrase(movievalues[0].strip())
        if not(movievalues[0].strip().lower() == nuevamovie.lower()):
            try:
                print(movievalues[0].strip() + "\t" + movievalues[1].strip() + "\t" + movievalues[2].strip() + "\t" + movievalues[3].strip() + "\t" + movievalues[4].strip())
            except:
                print("ERROR EN " + movievalues[0])
