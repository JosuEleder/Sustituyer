import tweepy
from sustituyer_main import procesafrase
import random, os

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '.'))

# Los keys, secrets y tokens del bot 
ACCESS_KEY = '1602241689996886018-4lKhpc0KsVwvM7KOfFg33534TDcwXr'
ACCESS_SECRET = '6UIJJyVXozV8xDbCJVkyxwn8NUClx8hoDfEB4Sa8a6Ll8'
CONSUMER_KEY = '2hA0EVrJigEDjj4NPyT80EnwN'
CONSUMER_SECRET = 'zAVBv5sRaXRFemTWnoi8LvqwyAYPDI54CQgpMdq4Mu2zRNqlqq'
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAKZtkQEAAAAAPdlwBxnNvWnDG0H4gwYuGQJH82o%3DrjBLaXU5ZlInnGQetAH2ftdAVp9XrZudHh9Fmmy0XQJfw1zQM3"

# Los procesos de autenticación
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

#El padrino	El padrino (1972)	9,0	173.519	https://www.filmaffinity.com/es/film809297.html
pelis = []
for datospeli in open(ROOT_DIR + "/data/moviesFARichi_clean.txt", "r"): 
    peli = datospeli.split("\t")
    pelis.insert(0, peli)

#random.choice
numero = random.randint(0, len(pelis))
pelioriginal = pelis[numero][0].strip()
enlaceoriginal = pelis[numero][4].strip()
pelianyooriginal = pelis[numero][1].strip()
pelinueva = procesafrase(pelioriginal)
#tuit= pelioriginal+" ("+enlaceoriginal+"):\n"+pelinueva
tuit= pelianyooriginal+" " + enlaceoriginal + ":\n"+pelinueva

api.update_status(status=tuit)
        
