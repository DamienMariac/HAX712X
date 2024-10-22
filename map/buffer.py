#%%
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString
import json

with open('../collecte/eco_compte/fusion.json', 'r') as file:
    data = json.load(file)

traffic_data = pd.DataFrame(data)

traffic_data['geometry'] = [Point(xy) for xy in zip(traffic_data['location'].apply(lambda x: x['coordinates'][0]),
                                                    traffic_data['location'].apply(lambda x: x['coordinates'][1]))]

# Créer un GeoDataFrame à partir des données
traffic_geo = gpd.GeoDataFrame(traffic_data, geometry='geometry')

# Charger le fichier GeoJSON contenant les routes
routes = gpd.read_file('../collecte/data/export.geojson')

# Assurer que les CRS correspondent pour les opérations spatiales
traffic_geo.set_crs(routes.crs, inplace=True)

# Créer des buffers autour de chaque point de mesure (choisir une distance de buffer appropriée, ex. 50 mètres)
buffer_distance = 0.001  # à ajuster selon le système de coordonnées
traffic_geo['buffer'] = traffic_geo.geometry.buffer(buffer_distance)

# Identifier les routes qui intersectent ces buffers
# Convertir les buffers en un GeoDataFrame pour utiliser la fonction sjoin
buffers = gpd.GeoDataFrame(traffic_geo, geometry='buffer', crs=traffic_geo.crs)
intersected_routes = gpd.sjoin(buffers, routes, how='inner', op='intersects')

# Optionnel: résumer les données pour afficher l'intensité moyenne du trafic pour chaque route
routes_traffic = intersected_routes.groupby('index_right').agg({
    'intensity': 'mean'  # Calculer l'intensité moyenne du trafic pour chaque route intersectée
}).rename(columns={'intensity': 'average_intensity'})

# Joindre les résultats avec les données des routes pour visualiser
final_routes = routes.join(routes_traffic, how='left')

# Visualiser les résultats
import folium

# Créer une carte
map = folium.Map(location=[43.610769, 3.876716], zoom_start=13)

# Ajouter des lignes pour les routes
for idx, row in final_routes.iterrows():
    sim_geo = [[point[1], point[0]] for point in row['geometry'].coords]  # coords pour LineString
    folium.PolyLine(sim_geo,
                    color='green' if row['average_intensity'] < 500 else 'orange' if row['average_intensity'] < 1000 else 'red',
                    weight=3,
                    opacity=0.8).add_to(map)

# Sauvegarder la carte
map.save('traffic_map.html')
# %%
