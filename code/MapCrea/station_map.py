import pandas as pd
import folium


station = pd.read_csv('data/stationcoor.csv', delimiter=',')

map_center = [43.610769, 3.876716]
map = folium.Map(location=map_center, zoom_start=13)

def add_marker(row):
    """
    Ajoute un marqueur sur une carte Folium à partir des données géographiques des stations VéloMagg.

    Cette fonction crée un marqueur sur une carte en utilisant la localisation des stations.
    Le marqueur est placé à la latitude et longitude spécifiées dans la ligne, et un popup est ajouté pour afficher le nom de la station). 

    : param row :
        Une ligne de DataFrame (CSV par exemple) contenant les informations nécessaires pour créer un marqueur. La ligne comporte
        au moins les colonnes suivantes : 'latitude', 'longitude', 'nom', 'secteur', et 'type_stati'.

    Remarque:
    Cette fonction ne peut être utilisé que si un objet `map` de type `folium.Map` est déjà créé et accessible.
    """
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Nom: {row['nom']}<br>Secteur: {row['secteur']}<br>Type: {row['type_stati']}",
        tooltip=row['nom']
    ).add_to(map)

station.apply(add_marker, axis=1)
map.save("map/bikestation_map.html")
