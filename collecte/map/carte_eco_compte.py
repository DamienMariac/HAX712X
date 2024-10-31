#%%
#import json
#import folium
#import os

#with open('../collecte/eco_compte/fusion.json', 'r') as f:
 #   data = json.load(f)


#map_center = [43.6, 3.89]  
#mymap = folium.Map(location=map_center, zoom_start=12)


#for entry in data:
 #   coordinates = entry['location']['coordinates']
  #  if coordinates and all(coordinates):
   #     folium.Marker(
    #        location=[coordinates[1], coordinates[0]],  
     #       popup=f"Intensity: {entry['intensity']}"
      #  ).add_to(mymap)

#mymap.save('eco_compte.html')


# %%
import folium
import json
import pandas as pd

# Coordonnées centrales de Montpellier, France
montpellier_coords = [43.6119, 3.8772]

# Créer la carte centrée sur Montpellier
carte_montpellier = folium.Map(location=montpellier_coords, zoom_start=13)

# Chemin vers le fichier GeoJSON des routes cyclables
fichier_geojson_cyclables = r"C:\Users\abkat\Downloads\Nouveau dossier\osm-mmm-bnac.json"

# Charger le fichier GeoJSON des routes cyclables
with open(fichier_geojson_cyclables, "r", encoding="utf-8") as file:
    data_cyclables = json.load(file)

# Fonction pour déterminer la couleur en fonction de l'intensité (trafic_vit)
def get_color(trafic_vit):
    if trafic_vit:
        if int(trafic_vit) > 40:
            return 'red'
        elif int(trafic_vit) > 20:
            return 'green'
        else:
            return 'yellow'
    return 'gray'

# Ajouter les routes cyclables sur la carte
for feature in data_cyclables['features']:
    coordinates = feature['geometry']['coordinates']
    trafic_vit = feature['properties'].get('trafic_vit')
    color = get_color(trafic_vit)
    points = [(coord[1], coord[0]) for coord in coordinates]
    folium.PolyLine(points, color=color, weight=3, opacity=0.7).add_to(carte_montpellier)

# Charger les données CSV des éco-compteurs
fichier_eco_compteurs_csv = r"C:\Users\abkat\Downloads\Nouveau dossier\MMM_MMM_GeolocCompteurs.csv"
eco_compteurs = pd.read_csv(fichier_eco_compteurs_csv)

# Ajouter les éco-compteurs en tant que marqueurs
for _, row in eco_compteurs.iterrows():
    latitude = row['Latitude']
    longitude = row['Longitude']
    nom = row['nom'] if 'nom' in row else 'Éco-compteur'
    trafic = row['trafic'] if 'trafic' in row else 'Inconnu'
    popup = folium.Popup(f"{nom}<br>Trafic: {trafic}", max_width=200)
    folium.Marker(location=[latitude, longitude], popup=popup, icon=folium.Icon(color='blue')).add_to(carte_montpellier)

# Sauvegarder la carte
carte_montpellier.save("carte_montpellier_eco_compteurs.html")

# Afficher la carte
from IPython.display import IFrame
IFrame("carte_montpellier_eco_compteurs.html", width=700, height=500)