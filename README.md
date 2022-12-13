# Sustituyer

## La idea
La idea de este programa es "relativamente" sencilla. Quiero hacer un programa Python que, dado un título en castellano de una película o libro (como "El halcón maltés") genere automáticamente variantes donde los sustantivos y adjetivos se sustituyan por palabras con las mismas sílabas, mismas características morfológicas, y que rimen en consonante (como "El cajón burgués"), por efecto cómico.
No, no sirve para nada más: es un experimento para practicar la combinación de desarrollos de PLN complejos en un pipeline con un objetivo muy específico.
## Las características
Cada palabra sustituída debe tener las siguientes características:
* Misma categoría gramatical (sustantivo o adjetivo, en principio)
* Mismos género y número
* Mismo número de sílabas
* Rima consonante
* Y, si puedo, que comience por el mismo patrón de vocal o consonante para evitar hiatos o diptongos forzados y hacer la equivalencia más afinada

Y, por supuesto, que todo esto se haga de manera completamente automática (salvo quizás una parte de revisión final). Quiero que cada paso se realice basándose en diccionarios, corpus y herramientas de acceso público y sin intervención humana.

¿Conseguiré hacer todo esto? Lo veremos.

## Empezando
Vamos a empezar simplemente con una lista de 10 películas, de las mejor valoradas en FilmAffinity, para dar los primeros pasos:
```
pelis = ["El padrino", "Doce hombres sin piedad", "La lista de Schindler", "Testigo de cargo", "Luces de la ciudad", "Cadena perpetua", "El gran dictador", "Tiempos modernos", "Lo que el viento se llevó", "Alguien voló sobre el nido del cuco"]
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
           if features[3]=="F": l = l+"<genero>Fem</genero>"
           if features[3]=="M": l = l+"<genero>Masc</genero>"
           if features[3]=="C": l = l+"<genero>Fem</genero><genero>Masc</genero>"
           if features[4]=="S": l = l+"<numero>Sing</numero>"
           if features[4]=="P": l = l+"<numero>Plur</numero>"
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
def buscarima(palabra):
    try:
        verse = Pyverse(palabra)
        rima = verse.consonant_rhyme
    except:
        print("error en " + palabra)
    return rima
```

Pues, a falta de detallitos posteriores, sólo nos queda el último paso: sacar del diccionario todas las palabras que rimen con cada una de las sustituibles (y que cumplan el resto de las condiciones) y elegir una al azar. ¡Vamos!

## Escoger sustituta
Entonces, por cada sustantivo o adjetivo, repasamos todo el diccionario para ver las que cumplen las mismas condiciones (misma rima, mismo número de sílabas, misma POS, mismo género y número), y confirmando además que no se trate de la misma palabra; ponemos todas las candidatas en una lista, sacamos un número al azar y esa es la palabra que va a sustituir.

```
    for i in d:
        if ("<rima>"+rima+"</rima>" in i and "<silabas>"+str(silabas)+"</silabas>" in i and "<POS>"+POS+"</POS>" in i and "<genero>"+genero+"</genero>" in i and "<numero>"+numero+"</numero>" in i and "<forma>"+palabra+"</forma>" not in i): candidatas.append(i)
    if len(candidatas)==0:
        nueva=palabra
    else:
        escogida = random.randint(0,len(candidatas)-1)
        nueva = candidatas[escogida][10:candidatas[escogida].index("</forma>")]
```

¡Y aquí tenemos un primer resultado!

```
El padrino
El rechino

Doce hombres sin piedad
Doce nombres sin maldad

La lista de Schindler
La vista de Schindler

Testigo de cargo
abrigo de sargo

Luces de la ciudad
cruces de la mitad

El gran dictador
El gran resquemor

Lo que el viento se llevó
Lo que el tiento se llevó

Alguien voló sobre el nido del cuco
Alguien voló sobre el ruido del buco
```

No está nada mal, ¿verdad?

Pero quedan cosas pendientes. El tema de las mayúsculas es una. Y otra es que ha habido unas cuantas donde no ha sugerido nada. A ver si descubrimos por qué.

## Arreglando detalles
*Cadena perpetua* y *Tiempos modernos* se han quedado igual. Tocará debuggear para ver qué ha pasado.

### "Cadena"
"Cadena" debería haber dado un buen conjunto de candidatos, como por ejemplo "melena". No se trata de un problema con la mayúscula, porque vemos que "Luces" lo ha sustiuido bien por "cruces". ¿Entonces?

En el diccionario está todo correcto: ```<p><forma>cadena</forma><lema>cadena</lema><POS>NOUN</POS><genero>Fem</genero><numero>Sing</numero><rima>ena</rima><silabas>3</silabas></p>```. ¡Ajajá! Pero el analizador de spaCy da "Cadena" como si fuera un nombre propio: ```{'original': 'Cadena', 'POS': 'PROPN', 'numero': '', 'genero': '', 'rima': '', 'silabas': 0, 'nueva': 'Cadena'}```. ¿Y por qué no lo hace con "Luces"? Misterio.

Siempre podemos decirle que realice la sustitución en los nombres propios también, y tendríamos algo así como "Vacaciones en Roma" > "Colaciones en Goma".

Pero es un riesgo. Mejor cambiar la mayúscula inicial a minúscula, y luego volver a ponerla. Hecho.

### "perpetua"
Esto es normal: es una palabra rara y no existe en nuestro diccionario ninguna otra de 3 sílabas con la misma rima. Así que todo bien.

### "Tiempos"
Vale. Aqui es otra vez la mayúscula dando un poco por saco. A veces el programa saca "tempos" (correcto", y a veces nos devuelve la misma, "tiempos". ¿Por qué? Porque al ir a comprobar que no nos sugiera la misma palabra, la comprobación falla por culpa de la mayúscula. Así que pasamos a minúscula en el momento de la comprobación y listo: ```and "<forma>"+palabra.lower()+"</forma>" not in i```

### "modernos"
Otro caso raro: ¿por qué no da "eternos", por ejemplo? Aquí no hay mayúscula que valga...

El análisis es correcto: ```{'original': 'modernos', 'POS': 'ADJ', 'numero': 'Plur', 'genero': 'Masc', 'rima': 'ernos', 'silabas': 3, 'nueva': 'modernos'}```, mientras que el diccionario da para "eternos" también lo que esperamos: ```<p><forma>eternos</forma><lema>eterno</lema><POS>ADJ</POS><rima>ernos</rima><silabas>3</silabas></p>```... espera, ¿por qué no pone el género y número en los adjetivos? Vale, porque en el campo "features" que nos devuelve el diccionario, los datos de género y número no están en el mismo lugar que en el sustantivo, sino un carácter por delante. Aay, FreeLing, normalización, por favor... Bueno, se arregla rápido. Ya tenemos *Tempos internos*!

### Signos de puntuación
He hecho una ñapa para que salgan bien los principales. Más adelante ya lo haré mejor.
```
    frasenueva = re.sub(' (\?|,|\)|;|\:|\-|\.|!)', r'\1', frasenueva)
    frasenueva = re.sub('(\¿|¡|\() ', r'\1', frasenueva)
```

## APIs

Bien. La idea es que este código sea accesible por medio de un bot (en Mastodon y Twitter). Y que tenga dos modos de uso: uno interactivo (que el usuario le dé un título y él responda con su sustitución), y otro autónomo (que cada X tiempo vaya posteando títulos sustituídos). Empecemos por el primero.

### Modo interactivo

He preparado un bot que escucha constantemente el stream de Twitter y busca "@sustituyer rima" y un título, y responde con un nuevo tweet con el título cambiado. Me daba el problema de que me procesaba también los tuits escritos por el bot mismo, lo que he arreglado poniendo la regla así: ```rule = StreamRule(value="sustituyer #rima -from:sustituyer")```. Es mejorable, iremos viendo.

## Posibles mejoras

Vamos a irlas dejando aquí apuntadas.

### Mayúsculas
El analizador que estoy usando parece que identifica como nombre propio cualquier palabra con mayúscula que no sea la inicial. Y además no les asigna género ni número. Así que el resultado en nombres como "Doce Hombres sin Piedad" no iba a ser muy bueno. Por ahora dejo que solo pueda ir en mayúscula la primera palabra del título, y ya veremos más adelante.

### Palabras muy raras
Una cosa que no me convence es que a veces saca palabras extremadamente poco conocidas: vale, es posible que la única rima para "ruido" sea "suido", pero ¿vosotros sabíais que un "suido" era un "mamífero del grupo de los artiodáctilos paquidermos, con jeta bien desarrollada y caninos largos y fuertes, que sobresalen de la boca, como por ejemplo el jabalí"? Pues hala, cuando veáis a un jabalí se lo podéis decir. Pero estaría bien que aquí salieran palabras sólo con un mínimo de frecuencia. ¿Cómo podría hacerse? No parece claro que desde spaCy pueda hacerse nativamente...

### Errores en pyverse
He visto dos:
* El error cuando le das una palabra con tres vocales seguidas, tipo "radioautografía"
* El error cuando le das una "stop word", como "si"

### "desnudo"
"Eva al desnudo" falla porque en el diccionario que uso no aparece "desnudo" como sustantivo. O lo añado, o le hago una rutina para que cuando no encuentra un sustantivo lo busque como adjetivo.

### Sinalefas
Una cosa que me gustaría añadir es que la sustitución tuviera en cuenta las sinalefas. Por ejemplo, que "Al final de la escapada" no se sustituya por "Al panal de la mermelada", sino por otra que empiece por vocal, como "Al final de la ensenada". Pero esto me lo dejo como "nice-to-have".

