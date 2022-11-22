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

Para ello nos descargamos un modelo lingüístico del español, con ```python3 -m spacy download es_core_news_sm```, y lo definimos en el script con ```nlp = spacy.load("es_core_news_sm")```

Por último, vamos por cada peli de la lista, le pasamos el título a nuestro nuevo objeto lingüístico "nlp", y ya tenemos los datos de cada palabra: "text" es la palabra tal cual, "pos_" es la categoría gramatical, "morph" es la información morfológica (número, género...). Metemos toda esa información en un diccionario. 

```
for peli in pelisoriginales:
    doc = nlp(peli)
    for token in doc:
        numero, genero = obtenergennum(str(token.morph))
        p = {"original":token.text, "POS":token.pos_, "numero":numero, "genero":genero, "nueva":sustituye(token.text)}
        print(p)
 ```
Ah, para sacar el número y el género de "morph" he hecho una función cutre que lo lee con unos if. Seguro que se podrá hacer mejor, ya le daré otra vuelta.
```
def obtenergennum(morf):
    numero=""
    genero=""
    if "Number=Sing" in morf:
        numero="sg"
    if "Number=Plur" in morf:
        numero="pl"
    if "Gender=Fem" in morf:
        genero="fm"
    if "Gender=Masc" in morf:
        genero="mc"
    return numero, genero
```
Y veréis que en el diccionario he añadido ya un lugar para la palabra nueva, que se obtendría con la función "sustituye" (que por ahora no hace casi nada). Pronto volveremos a esto.



