import pandas as pd
import folium

# Charger le fichier CSV
station = pd.read_csv('data/stationcoor.csv', delimiter=',')

# Initialiser la carte centrée sur Montpellier
map_center = [43.610769, 3.876716]
map = folium.Map(location=map_center, zoom_start=13)

# Ajouter des marqueurs en utilisant station.apply()
def add_marker(row):
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Nom: {row['nom']}<br>Secteur: {row['secteur']}<br>Type: {row['type_stati']}",
        tooltip=row['nom']
    ).add_to(map)

# Appliquer la fonction à chaque ligne sans boucle explicite
station.apply(add_marker, axis=1)

# Sauvegarder la carte
map.save("map/bikestation_map.html")
