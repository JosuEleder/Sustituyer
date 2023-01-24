from bs4 import BeautifulSoup
import urllib.request

baseurl = "https://www.elseptimoarte.net"
firstpages = []
pages = []
movies = []
firstyear = 1920
lastyear = 2024

def extractmovies(soup):
    collection = soup.find(id="collections") 
    h3s = collection.find_all("h3")
    for h3 in h3s:
        if len(h3.find_all("a"))>0 and h3.parent.has_attr("data-puntuacion"):
            link = "https://www.elseptimoarte.net" + h3.a["href"]
            movie = {"name":h3.string, "punctuation":h3.parent["data-puntuacion"], "link":link}
            movies.append(movie)

# Creo un array de la primera página de cada año
for year in range(firstyear, lastyear):
    firstpageurl = baseurl + "/peliculas/" + str(year) + "/"
    firstpages.append(firstpageurl)

# Para cada año, añado la página a un array "pages", la analizo, y si contiene "go_next", saco su valor, creo la siguiente página y continúo
for firstpage in firstpages:
    pages.append(firstpage)
    data = urllib.request.urlopen(firstpage)
    soup = BeautifulSoup(data, 'html.parser')
    # Y de paso llamo a la función "extractmovies", que me buscará los títulos de las películas de esa página y los meterá en un array "movies"
    extractmovies(soup)
    while len(soup.select('div[class="go_next"]'))>0:
        tag = soup.select('div[class="go_next"]')[0].a['href']
        nextpage = baseurl + tag
        pages.append(nextpage)
        data = urllib.request.urlopen(nextpage)
        soup = BeautifulSoup(data, 'html.parser')
        extractmovies(soup)

for movie in movies:
        if movie["punctuation"][0] in ("9", "8", "7"):
            print(movie["name"].strip() + "\t" + movie["punctuation"].strip() + "\t" + movie["link"].strip())
