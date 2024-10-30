import os
import pandas as pd
import geopandas as gpd
import folium
import osmnx as ox

# Chemin vers le fichier CSV contenant les pistes cyclables
csv_path = '/home/marinegermain/PROJET/collecte/data/active_bike_paths.csv'  
df = pd.read_csv(csv_path)

# Filtrer les données (si nécessaire)
df_filtered = df[df['statut_d'] == 'actif']  # Ajuste selon tes critères
osm_ids = df_filtered['id_osm'].unique()

# Récupérer les géométries pour toutes les pistes cyclables
gdf = ox.geometries_from_place('Montpellier, France', tags={'highway': 'cycleway'})

# Créer une carte centrée sur Montpellier
m = folium.Map(location=[43.6115, 3.8772], zoom_start=13)

# Ajouter chaque piste cyclable à la carte avec une couleur rouge
for _, row in gdf.iterrows():
    folium.GeoJson(
        row['geometry'],
        style_function=lambda x: {
            'fillColor': 'red',
            'color': 'red',
            'weight': 2,
            'opacity': 0.6
        }
    ).add_to(m)

# Enregistrer la carte en tant que fichier HTML
m.save('/home/marinegermain/PROJET/collecte/map/map_cycle_paths.html')
