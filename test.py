from sustituyer_main import procesafrase

pelis = ["El padrino", "Doce hombres sin piedad", "La lista de Schindler", "Testigo de cargo", "Luces de la ciudad", "Cadena perpetua", "El gran dictador", "Tiempos modernos", "Lo que el viento se llevó", "Alguien voló sobre el nido del cuco"]
for peli in pelis: 
    nuevapeli = procesafrase(peli)
    print(peli + " -> " + nuevapeli)