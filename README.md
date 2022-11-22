# CambiaNombres

## La idea
La idea de este programa es "relativamente" sencilla. Quiero hacer un programa que, dado un título en castellano de una película o libro (como "El halcón maltés") genere automáticamente variantes donde los sustantivos y adjetivos se sustituyan por palabras con las mismas sílabas, mismas características morfológicas, y que rimen en consonante (como "El cajón burgués"), por efecto cómico.
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

¿Y cómo consigo eso? Pues utilizando alguna herramienta de NLP. Hay dos principales que trabajan bien con Python: NLTK y Spacy. Vamos a empezar con NLTK.

### Análisis gramatical con NLTK
Empezamos con ```import nltk```

