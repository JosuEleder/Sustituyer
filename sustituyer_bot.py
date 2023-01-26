import tweepy
from tweepy import StreamingClient, StreamRule
from sustituyer_main import procesafrase
import re
from datetime import datetime
import sys

# Los keys, secrets y tokens del bot 
import config

# Los procesos de autenticación
auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
auth.set_access_token(config.ACCESS_KEY, config.ACCESS_SECRET)
api = tweepy.API(auth)

class TweetPrinterV2(tweepy.StreamingClient):
    def on_disconnect(self, notice):
        # Connection to the stream has been lost, attempt to reconnect
        print("Nos hemos caído")
    
    # Cada vez que se encuentre un tuit que cumple las normas:
    def on_tweet(self, tweet):
        # Se escribirá a consola
        print(f"{tweet.id} {tweet.created_at} ({tweet.author_id}): {tweet.text}")
        print("-"*50)
        titulooriginal = ""
        titulonuevo = ""
        # Al text del tuit original se le eliminará la mención y el hashtag
        titulooriginal = re.sub('(@[Ss]ustituyer ?|#[Rr]ima ?|\")', '', tweet.text)
        # Y se enviará a sustituyer_main para que nos dé el título sustituído
        titulonuevo = procesafrase(titulooriginal)
        reply_text = titulonuevo
        # Y se enviará un nuevo tuit en respuesta, que contenga el título nuevo
        api.update_status(status=reply_text, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
        
printer = TweetPrinterV2(config.BEARER_TOKEN)

if hasattr(printer, 'running'):
    # Y aquí la regla: procesará los tuits que contengan "sustituyer" (aunque sea en una respuesta) y "#rima", pero que no vengan del propio bot
    rule = StreamRule(value="sustituyer #rima -from:sustituyer")
    printer.add_rules(rule)
    printer.filter()
    print("Nueva regla: "+StreamRule.value)

#