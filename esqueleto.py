##header
import spacy
from spacy.vocab import Vocab
from pyverse import Pyverse
import random

##data
pelis = ["El padrino", "Doce hombres sin piedad", "La lista de Schindler", "Testigo de cargo", "Luces de la ciudad", "Cadena perpetua", "El gran dictador", "Tiempos modernos", "Lo que el viento se llevó", "Alguien voló sobre el nido del cuco"]
#pelis = []

nlp = spacy.load("es_core_news_lg")

d = []
rima=""
silabas=0
POS=""
numero=""
genero=""
frasenueva=""

##functions

def sustituye(palabra, POS, numero, genero, rima, silabas):
    candidatas = []
    for i in d:
        if ("<rima>"+rima+"</rima>" in i and "<silabas>"+str(silabas)+"</silabas>" in i and "<POS>"+POS+"</POS>" in i and "<genero>"+genero+"</genero>" in i and "<numero>"+numero+"</numero>" in i and "<forma>"+palabra.lower()+"</forma>" not in i): candidatas.append(i)
    if len(candidatas)==0:
        nueva=palabra
    else:
        escogida = random.randint(0,len(candidatas)-1)
        nueva = candidatas[escogida][10:candidatas[escogida].index("</forma>")]
    return nueva

def buscarima(palabra):
    rima=""
    silabas=0
    try:
        verse = Pyverse(palabra)
        rima = verse.consonant_rhyme
        silabas = verse.count
    except:
        print("error en " + palabra)
    return rima, silabas

def creardiccionario():
    d.append("<dic>")
    with open("data/MM.adj") as f:
        for linea in f:
            (palabradic, lema, features) = linea.split()
            l = "<p><forma>" + palabradic + "</forma><lema>"+lema+"</lema><POS>ADJ</POS>"
            if features[3]=="F": l = l+"<genero>Fem</genero>"
            if features[3]=="M": l = l+"<genero>Masc</genero>"
            if features[3]=="C": l = l+"<genero>Fem</genero><genero>Masc</genero>"
            if features[4]=="S": l = l+"<numero>Sing</numero>"
            if features[4]=="P": l = l+"<numero>Plur</numero>"
            rima=""
            silabas=0
            (rima,silabas) = buscarima(palabradic)
            l = l+"<rima>"+rima+"</rima>"
            l = l+"<silabas>"+str(silabas)+"</silabas>"
            l = l+"</p>"
            if palabradic=="sórdido": print(l)
            d.append(l)
    with open("data/MM.nom") as f:
        for linea in f:
            (palabradic, lema, features) = linea.split()
            l = "<p><forma>" + palabradic + "</forma><lema>"+lema+"</lema><POS>NOUN</POS>"
            if features[2]=="F": l = l+"<genero>Fem</genero>"
            if features[2]=="M": l = l+"<genero>Masc</genero>"
            if features[2]=="C": l = l+"<genero>Fem</genero><genero>Masc</genero>"
            if features[3]=="S": l = l+"<numero>Sing</numero>"
            if features[3]=="P": l = l+"<numero>Plur</numero>"
            rima=""
            silabas=0
            (rima,silabas) = buscarima(palabradic)
            l = l+"<rima>"+rima+"</rima>"
            l = l+"<silabas>"+str(silabas)+"</silabas>"
            l = l+"</p>"
            d.append(l)
    d.append("</dic>")

##main

creardiccionario()

for peli in pelis:
    frasenueva=""
    doc = nlp(peli)
    print("\n" + peli)
    primerapalabra=1
    for token in doc:
        rima=""
        silabas=0
        numero=""
        genero=""
        nueva=token.text
        if (token.pos_=="ADJ" or token.pos_=="NOUN"):
            numero = token.morph.get("Number")[0]
            try:
                genero = token.morph.get("Gender")[0]
            except:
                genero="Fem,Masc"
            (rima, silabas)=buscarima(token.text)
            nueva = sustituye(token.text, token.pos_, numero, genero, rima, silabas)
        p = {"original":token.text, "POS":token.pos_, "numero":numero, "genero":genero, "rima":rima, "silabas":silabas, "nueva":nueva}
        if primerapalabra==1: p["nueva"]=p["nueva"].capitalize()
        frasenueva = frasenueva+p["nueva"]+" "
        primerapalabra=0
    print(frasenueva)




