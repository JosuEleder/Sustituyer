from bs4 import BeautifulSoup
import urllib.request
import yaml
import re
import sys, os
sys.path.insert(0, '..')
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

baseurl = "https://www.filmaffinity.com/es/userlist.php?user_id=959742&list_id=1001&chv=list&page="
baseshort = "https://www.filmaffinity.com"
pages = []
movies = []
firstpage = 1
lastpage = 11

def extractmovies(soup):
    collection = soup.find(class_="movies_list") 
    elements = collection.find_all("li")
    for element in elements:
        wrap = element.find(class_="mc-title")
        link = wrap.a["href"].strip()
        name = wrap.a.text.strip()
        nameyear = re.sub(" +", " ", wrap.text).strip()
        nextdiv = wrap.find_next_sibling("div")
        punctdiv = nextdiv.div
        punctuation = punctdiv.text.strip()
        nextdiv2 = punctdiv.find_next_sibling("div")
        reviews = nextdiv2.text.strip()
        if wrap.a.has_attr("title"):
            movie = {"name":name, "punctuation":punctuation, "reviews":reviews, "link":link, "nameyear":nameyear}
            movies.append(movie)

# MAIN

# Creo un array "pages" de cada página de la lista y voy entrando en cada una
for page in range(firstpage, lastpage):
    pageurl = baseurl + str(page)
    data = urllib.request.urlopen(pageurl)
    soup = BeautifulSoup(data, 'html.parser')
    # Llamo a la función "extractmovies", que me buscará los títulos de las películas de esa página y los meterá en un array "movies"
    extractmovies(soup)
    
def write_yaml(data):
    """ A function to write YAML file"""
    with open(ROOT_DIR + '/data/moviesFARichi.yml', 'w') as f:
        yaml.dump(data, f, allow_unicode=True)

write_yaml(movies)