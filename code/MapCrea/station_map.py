import pandas as pd
import folium


station = pd.read_csv('data/stationcoor.csv', delimiter=',')

map_center = [43.610769, 3.876716]
map = folium.Map(location=map_center, zoom_start=13)

def add_marker(row):
    """
    Ajoute un marqueur sur une carte Folium à partir des données géographiques des stations VéloMagg.

    Args:
        param (pandas.Series) : Une ligne d'un DataFrame contenant les informations nécessaires pour créer un marqueur. La ligne doit inclure au moins les colonnes suivantes :
        - 'latitude' (float) : Latitude de la station.
        - 'longitude' (float) : Longitude de la station.
        - 'nom' (str) : Nom de la station.
        - 'secteur' (str) : Secteur géographique de la station.
        - 'type_stati' (str) : Type de station (exemple : "Vélo" ou "Parking").

    Note: Cette fonction ne peut être utilisé que si un objet `map` de type `folium.Map` est déjà créé et accessible.
    """
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Nom: {row['nom']}<br>Secteur: {row['secteur']}<br>Type: {row['type_stati']}",
        tooltip=row['nom']
    ).add_to(map)

station.apply(add_marker, axis=1)
map.save("map/bikestation_map.html")
