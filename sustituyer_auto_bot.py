import tweepy
from sustituyer_main import procesafrase
import random, os
import yaml

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '.'))

# Los keys, secrets y tokens del bot 
import config

# Los procesos de autenticación
auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
auth.set_access_token(config.ACCESS_KEY, config.ACCESS_SECRET)
api = tweepy.API(auth)

pelis = []
with open(ROOT_DIR + "/data/moviesFARichi_clean.yml", "r") as stream:
    pelis = yaml.safe_load(stream)

#random.choice
numero = random.randint(0, len(pelis))

pelioriginal = pelis[numero]["name"]
enlaceoriginal = pelis[numero]["link"]
pelianyooriginal = pelis[numero]["nameyear"]
pelinueva = procesafrase(pelioriginal)
#tuit= pelioriginal+" ("+enlaceoriginal+"):\n"+pelinueva
tuit= pelianyooriginal+" " + enlaceoriginal + ":\n"+pelinueva

api.update_status(status=tuit)
        
