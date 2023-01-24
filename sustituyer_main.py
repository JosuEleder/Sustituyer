##header 
import spacy
from spacy.vocab import Vocab
from pyverse import Pyverse
import random, re, sys, os

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '.'))

## Ejemplos de pelis. Se usarán sólo en el modo "Test=2"
pelis = ["El padrino", "Doce hombres sin piedad", "La lista de Schindler", "Testigo de cargo", "Luces de la ciudad", "Cadena perpetua", "El gran dictador", "Tiempos modernos", "Lo que el viento se llevó", "Alguien voló sobre el nido del cuco"]
#pelis = ["El padrino", "El padrino. Parte II", "Doce Hombres sin Piedad", "La lista de Schindler", "Testigo de cargo", "Luces de la ciudad", "Cadena perpetua", "El gran dictador", "Tiempos modernos", "Pulp Fiction", "El golpe", "Ser o no ser", "Harakiri", "El crepúsculo de los dioses", "La vida es bella", "Eva al desnudo", "Queen Live at Wembley '86", "Senderos de gloria", "Shoah", "Thank you for watching", "El infierno del odio", "Los siete samuráis", "Amanecer", "Perdición", "El apartamento", "Ciudad de Dios", "El chico", "Pulse: Live at Earls Court", "La evasión", "La quimera del oro", "Psicosis", "Uno de los nuestros", "Los Miserables 25º aniversario", "Casablanca", "Alguien voló sobre el nido del cuco", "Les Luthiers: Mastropiero que nunca", "Barbarroja", "El hombre que mató a Liberty Valance", "Los olvidados", "Cinema Paradiso", "American History X", "M, el vampiro de Düsseldorf", "Dersu Uzala: El cazador", "La condición humana III: La plegaria del soldado", "Las uvas de la ira", "Érase una vez en América", "Les Luthiers: Unen canto con humor", "Les Luthiers: Grandes hitos", "Human", "Echoes: Pink Floyd", "El intendente Sansho", "Ladrón de bicicletas", "Matar a un ruiseñor", "Con faldas y a lo loco", "La pasión de Juana de Arco", "Vivir", "Una noche en la ópera", "El maquinista de La General", "Seven", "Candilejas", "El verdugo", "Con la muerte en los talones", "El pianista", "Les Luthiers: Bromato de armonio", "Sherlock: La caída de Reichenbach", "Vértigo: De entre los muertos", "Apocalypse Now", "Samsara", "El mundo de Apu", "Cuentos de Tokio", "Metrópolis", "Sin perdón", "Rick y Morty: Cadena Rickpetua", "La canción del camino", "Ordet", "Rebeca", "El tercer hombre", "El silencio de los corderos", "El último", "Perversidad", "La ventana indiscreta", "Las noches de Cabiria", "Rocco y sus hermanos", "¿Qué fue de Baby Jane?", "¡Qué bello es vivir!", "El precio del poder", "Hora de Aventuras: La aventura final", "Les Luthiers hacen muchas gracias de nada", "Noche y niebla", "La parada de los monstruos", "La naranja mecánica", "Forrest Gump", "Hasta que llegó su hora", "Crimen perfecto", "El bueno, el feo y el malo", "La batalla de Chile (Parte II): El golpe de estado", "La batalla de Chile (Parte I): La insurrección de la burguesía", "Rebelión", "Los mejores años de nuestra vida", "Un condenado a muerte se ha escapado"]

# carga del modelo lingüístico grande de spaCy
nlp = spacy.load("es_core_news_lg")

d = []
rima=""
silabas=0
POS=""
numero=""
genero=""
frasenueva=""
os.path.join(ROOT_DIR)

## Funciones

# Función que crea el diccionario (d) de todas las palabras, con sus características morfológicas.

def creardiccionario():
    d.append("<dic>")

# Se prepara el diccionario de "comunes" para comparar luego y que se quede sólo con las palabras más comunes del castellano
    with open(ROOT_DIR + "/data/10000_formas.txt",'r') as fichero_comunes:
        comunes=[]
        for linea in fichero_comunes:
            comunes.append(linea.split()[1])

# Primero el fichero de adjetivos
    with open(ROOT_DIR + "/data/MM.adj") as f:
        for linea in f:
            # Ejemplo de formato: aberenjenadas aberenjenado AQ0FP00
            (palabradic, lema, features) = linea.split()
            # Compara con "comunes"
            if palabradic in comunes:
                # Reformatea a un formato XML
                l = "<p><forma>" + palabradic + "</forma><lema>"+lema+"</lema><POS>ADJ</POS>"
                # Mapea el género y número para que coincidan con el que luego nos dará el analizador
                if features[3]=="F": l = l+"<genero>Fem</genero>"
                if features[3]=="M": l = l+"<genero>Masc</genero>"
                if features[3]=="C": l = l+"<genero>Fem,Masc</genero>"
                if features[4]=="S": l = l+"<numero>Sing</numero>"
                if features[4]=="P": l = l+"<numero>Plur</numero>"
                # Se añade el número de sílabas y el esquema de rima con la función "buscarima"
                # Ejemplo: el esquema de rima de "cansina" será "ina"
                rima=""
                silabas=0
                (rima,silabas) = buscarima(palabradic)
                l = l+"<rima>"+rima+"</rima>"
                l = l+"<silabas>"+str(silabas)+"</silabas>"
                l = l+"</p>"
                # Se añade al diccionario d
                d.append(l)
    # Se hace lo mismo con los sustantivos.
    with open(ROOT_DIR + "/data/MM.nom") as f:
        for linea in f:
            (palabradic, lema, features) = linea.split()
            if palabradic in comunes:
                l = "<p><forma>" + palabradic + "</forma><lema>"+lema+"</lema><POS>NOUN</POS>"
                # Cuidado: el formato es distinto que en adjetivos
                # Ejemplo de formato: abadejos abadejo NCMP000
                if features[2]=="F": l = l+"<genero>Fem</genero>"
                if features[2]=="M": l = l+"<genero>Masc</genero>"
                if features[2]=="C": l = l+"<genero>Fem,Masc</genero>"
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

# Función que, dada una palabra, devuelve su número de sílabas y su esquema de rima. Usa el módulo externo "Pyverse" (ver Readme)
def buscarima(palabra):
    rima=""
    silabas=0
    try:
        verse = Pyverse(palabra)
        rima = verse.consonant_rhyme
        silabas = verse.count
    except:
        pass
    return rima, silabas

# Función que recibe una palabra y sus características y devuelve la palabra nueva que poner en su lugar
def sustituye(palabra, POS, numero, genero, rima, silabas):
    candidatas = []
    # Iteración principal: cada palabra del diccionario que coincida con las características de la palabra original (y que no sea ella misma) la añadimos a un array de candidatas.
    for i in d:
        if ("<rima>"+rima+"</rima>" in i and "<silabas>"+str(silabas)+"</silabas>" in i and "<POS>"+POS+"</POS>" in i and "<genero>"+genero+"</genero>" in i and "<numero>"+numero+"</numero>" in i and "<forma>"+palabra.lower()+"</forma>" not in i): candidatas.append(i)
    # Si no ha salido ninguna candidata, nos quedamos con la original
    if len(candidatas)==0:
        nueva=palabra
    else:
        #Si hay candidatas, escogemos un número al azar y la lanzamos
        escogida = random.randint(0,len(candidatas)-1)
        nueva = candidatas[escogida][10:candidatas[escogida].index("</forma>")]
    return nueva


## API: funciones para realizar diferentes acciones

# Función que toma una frase y le aplica las sustituciones necesarias para obtener la nueva
def procesafrase(frase):
    frasenueva=""
    caps=0
    # Si empieza por mayúscula, se pasa a minúscula y se guarda la info para reponer la mayúscula después
    if frase[0].isupper():
        caps=1
        frase=frase[0].lower() + frase[1:]
        # Se lanza el análisis lingüístico de la frase con el "nlp" de spaCy
    doc = nlp(frase)
    # spaCy devuelve cada palabra en un objeto "token" con diferente información. 
    for token in doc:
        rima=""
        silabas=0
        numero=""
        genero=""
        # La palabra nueva será la misma que la original salvo para adjetivos y sustantivos
        nueva=token.text
        
        # En esos dos casos se devuelve el género y número que ha dado el analizador
        if (token.pos_=="ADJ" or token.pos_=="NOUN"):
            try:
                numero = token.morph.get("Number")[0]
            except:
                numero=""
            try:
                genero = token.morph.get("Gender")[0]
            except:
                genero="Fem,Masc"
            # Y también el esquema de rima y sílabas que da "buscarima"
            (rima, silabas)=buscarima(token.text)
            # Y con esos datos se llama a "sustituye" para obtener la palabra nueva
            nueva = sustituye(token.text, token.pos_, numero, genero, rima, silabas)
        # Se imprime la info en consola para debug
        p = {"original":token.text, "POS":token.pos_, "numero":numero, "genero":genero, "rima":rima, "silabas":silabas, "nueva":nueva}
        # print(p)
        frasenueva = frasenueva+p["nueva"]+" "
    # A la frase nueva se le arreglan los signos de puntuación 
    frasenueva = re.sub(' (\?|,|\)|;|\:|\-|\.|!)', r'\1', frasenueva)
    frasenueva = re.sub('(\¿|¡|\() ', r'\1', frasenueva)
    # Se repone la mayúscula en su caso
    if caps==1: frasenueva = frasenueva[0].upper() + frasenueva[1:]
    # Y se devuelve
    return(frasenueva.strip())

## Main: distintas acciones que se pueden realizar

# Esta es necesaria y es lo primero que se hace
creardiccionario()

test=0

# Modo Test 1: si se llama a "sustituyer_main.py" con un título, devuelve su sustitución
if test==1:
    if len(sys.argv)>1:
        frase=sys.argv[1]
        frasenueva = procesafrase(frase)
        print(frase+"\n"+frasenueva)
    else:
        print("")



