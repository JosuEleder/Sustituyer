import tweepy
from sustituyer_main import procesafrase
import random

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

pelis = []
for datospeli in open("data/movies_clean.txt", "r"): 
    peli = datospeli.split("\t")
    pelis.insert(0, peli)

#random.choice
numero = random.randint(0, len(pelis))
pelioriginal = pelis[numero][0].rstrip()
enlaceoriginal = pelis[numero][2].rstrip()
pelinueva = procesafrase(pelioriginal)
tuit= pelioriginal+" ("+enlaceoriginal+"):\n"+pelinueva

api.update_status(status=tuit)
        
