# CambiaNombres

## La idea
La idea de este programa es "relativamente" sencilla. Quiero hacer un programa Python que, dado un título en castellano de una película o libro (como "El halcón maltés") genere automáticamente variantes donde los sustantivos y adjetivos se sustituyan por palabras con las mismas sílabas, mismas características morfológicas, y que rimen en consonante (como "El cajón burgués"), por efecto cómico.
No, no sirve para nada más: es un experimento para practicar la combinación de desarrollos de PLN complejos en un pipeline con un objetivo muy específico.
## Las características
Cada palabra sustituída debe tener las siguientes características:
* Misma categoría gramatical (sustantivo o adjetivo, en principio)
* Mismo número de sílabas
* Rima consonante
* Y, si puedo, que comience por el mismo patrón de vocal o consonante para evitar hiatos o diptongos forzados y hacer la equivalencia más afinada

Y, por supuesto, que todo esto se haga de manera completamente automática (salvo quizás una parte de revisión final). Quiero que cada paso se realice basándose en diccionarios, corpus y herramientas de acceso público y sin intervención humana.

¿Conseguiré hacer todo esto? Lo veremos.

## Empezando
Vamos a empezar simplemente con una lista de 10 películas, de las mejor valoradas en FilmAffinity, para dar los primeros pasos:
```
pelisoriginales = ["El padrino", "Doce hombres sin piedad", "La lista de Schindler", "Testigo de cargo", "Luces de la ciudad", "Cadena perpetua", "El gran dictador", "Tiempos modernos", "Lo que el viento se llevó", "Alguien voló sobre el nido del cuco"]
```
Y lo primero que vamos a hacer es conseguir la información morfológica de cada una de las palabras de los títulos. En concreto necesito:
* Categoría gramatical (sustantivo, adjetivo...)
* Género (femenino, masculino...)
* Número (singular, plural...)
* Por ahora vamos a dejar fuera los verbos, pero si me meto con ellos necesitaré tiempo, modo, persona...

¿Y cómo consigo eso? Pues utilizando alguna herramienta de NLP. De entre todas las que existen para Python, vamos a empezar con Spacy, que parece la más versátil para nuestros propósitos.

## Análisis gramatical con spaCy.
Primero lo instalamos con ```pip3 install -U spacy```. Cuando termine, en nuestro script, ```import spacy```.

Ahora tenemos que encontrar la forma de que spaCy realice un análisis sintáctico de cada título, porque no queremos que nos diga que "cargo" puede ser el verbo "cargar" en presente: queremos que sepa que en "testigo de cargo", "cargo" es sólo (o muy probablemente) un sustantivo. O sea, queremos que *desambigüe*.

Para ello nos descargamos un modelo lingüístico del español, con ```python3 -m spacy download es_core_news_lg```, y lo definimos en el script con ```nlp = spacy.load("es_core_news_lg")```

Por último, vamos por cada peli de la lista, le pasamos el título a nuestro nuevo objeto lingüístico "nlp", y ya tenemos los datos de cada palabra: "text" es la palabra tal cual, "pos_" es la categoría gramatical, "morph" es la información morfológica (número, género...). Metemos toda esa información en un diccionario. 

```
for peli in pelis:
    doc = nlp(peli)
    print("\n" + peli)
    for token in doc:
        p = {"original":token.text, "POS":token.pos_, "numero":token.morph.get("Number"), "genero":token.morph.get("Gender"), "nueva":sustituye(token.text, token.pos_)}
        print(p)
```
Y veréis que en el diccionario he añadido ya un lugar para la palabra nueva, que se obtendría con la función "sustituye" (que por ahora no hace casi nada). Pronto volveremos a esto.

## Acceder al diccionario de todo el castellano

Bien. Ya tenemos las palabras que queremos sustituir, y sabemos sus características morfológicas. ¿Cómo encontramos ahora una palabra que rime con ellas? Porque obviamente, no va a haber un módulo al que poder decirle "dame una palabra X que rime con tal".

No encuentro una forma de obtener un listado de todas las palabras del modelo con sus características. Así que la otra opción es bajarme un diccionario de español que contenga todas las formas (o sea, no sólo "blanco", sino también "blanca", "blancos" y "blancas"), y sus características gramaticales (POS, género y número), para poder identificar las palabras que necesitamos. Y cargarlo como un objeto diccionario en Python, para poder acceder a él con facilidad.

Así que nos bajamos a un directorio ```data``` los diccionarios de adjetivos y sustantivos de otro proyecto, FreeLing https://github.com/TALP-UPC/FreeLing/tree/master/data/es/dictionary/entries , MM.adj y MM.noun. y los parseamos, para hacer explícita su información. Metemos toda la info en una lista de cadenas, con formato XML, por si luego queremos exportarla. Por ahora queda así, por ejemplo para los adjetivos:

```
    d.append("<dic>")
    with open("data/MM.adj") as f:
        for linea in f:
           (palabradic, lema, features) = linea.split()
           l = "<p><forma>" + palabradic + "</forma><lema>"+lema+"</lema><POS>ADJ</POS>"
           if features[2]=="F": l = l+"<genero>Fem</genero>"
           if features[2]=="M": l = l+"<genero>Masc</genero>"
           if features[2]=="C": l = l+"<genero>Fem,Masc</genero>"
           if features[3]=="S": l = l+"<numero>Sing</numero>"
           if features[3]=="P": l = l+"<numero>Plur</numero>"
           l = l+"</p>"
           d.append(l)
    d.append("</dic>")
```
Me doy cuenta de que el número de formas para el castellano no es muy grande: unas 170k formas. Pero por ahora nos bastará.
    
Con esto ya tendríamos la información para sustituir cada palabra por una de características similares, pero... ¿y la rima, que es lo que le da la gracia? ¡A ello!
    
## A rimar

Mi primera intención era hacerme yo el esquema de rima para todas las palabras: crear un algoritmo de separación por sílabas, otro de acentuación, y otro que a partir de ahí extrajera el "modelo de rima consonante" de cada palabra para ver cuál rima con cuál. Y hubiera estado muy bien, si no fuera... ¡que alguien más lo ha hecho!

Un tal Ruben Karlsson ha creado *pyverse* https://pypi.org/project/pyverse/ , un proyecto que literalmente cuenta las sílabas de una línea de texto y devuelve su métrica y su rima. Pues vamos a probarlo, ¿no?

```
def buscarima(palabra):
    verse = Pyverse(palabra)
    rima = verse.consonant_rhyme
    return rima
```
Esto devuelve "abra" para "palabra", por ejemplo. Bien. Veo algún problema, como que da error con palabras como "el" o "de". En principio no nos importa porque sólo lo vamos a usar con sustantivos y adjetivos.

Así que añadiremos el modelo de rima a cada palabra de los títulos que sea sustantivo o adjetivo: ```if (token.pos_=="ADJ" or token.pos_=="NOUN"): rima=buscarima(token.text)```

¡Y parece que funciona!
```
{'original': 'Tiempos', 'POS': 'NOUN', 'numero': ['Plur'], 'genero': ['Masc'], 'rima': 'empos', 'nueva': '_Tiempos_'}
{'original': 'modernos', 'POS': 'ADJ', 'numero': ['Plur'], 'genero': ['Masc'], 'rima': 'ernos', 'nueva': '_modernos_'}
```
Pues a poner el esquema de rimas de todo el diccionario.

Primer problema: con "esternohioidea" (vale) el programa se rompe porque se ve que no esperaba esa combinación de vocales. Bueno, podemos vivir con ello. Pongamos una excepción y listo.
```
            try:
                rima = buscarima(palabradic)
            except:
                print("error en "+palabradic)
```
