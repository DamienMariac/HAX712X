import geopandas as gpd
import folium
import json
from shapely.geometry import Point
import os

# Chemin vers les données de trafic
traffic_data_path = 'data/concatenated_data.jsonl'

# Charger les données de trafic
traffic_data = []
with open(traffic_data_path, 'r') as file:
    for line in file:
        traffic_data.append(json.loads(line.strip()))

# Valider les données pour s'assurer que les coordonnées sont valides
valid_traffic_data = [
    item for item in traffic_data
    if item.get('location')
    and 'coordinates' in item['location']
    and isinstance(item['location']['coordinates'], list)
    and len(item['location']['coordinates']) == 2
    and item['location']['coordinates'][0] is not None
    and item['location']['coordinates'][1] is not None
]

# Création du GeoDataFrame
traffic_gdf = gpd.GeoDataFrame(
    valid_traffic_data,
    geometry=[Point(data['location']['coordinates']) for data in valid_traffic_data],
    crs="EPSG:4326"
)

# Charger les routes depuis un fichier GeoJSON
routes_gdf = gpd.read_file('data/export.geojson')
routes_gdf = routes_gdf.to_crs(traffic_gdf.crs)

# Effectuer une jointure spatiale
joined_gdf = gpd.sjoin_nearest(routes_gdf, traffic_gdf, how="inner", max_distance=100)

# Fonction pour déterminer la couleur en fonction de l'intensité
def get_color(intensity):

    """
    Détermine une couleur en fonction de l'intensité donnée.

    Args: 
        param (int) : La valeur numérique représentant l'intensité doit être un entier positif.
    
    Return: 
        str : Une chaîne de caractères représentant une couleur :
        
        - 'darkred' : si l'intensité est supérieure à 2000,
        
        - 'red' : si l'intensité est supérieure à 1000 et inférieur à 2000,
        
        - 'darkorange' : si l'intensité est supérieure à 500 et inférieur à 1000,
        
        - 'gold' : si l'intensité est supérieure à 250 et inférieur à 500,
        
        - 'green' : si l'intensité est inférieure ou égale à 250.
    """
    if intensity > 2000:
        return 'darkred'
    elif intensity > 1000 and intensity <= 2000:
        return 'red'
    elif intensity > 500 and intensity <= 1000:
        return 'darkorange'
    elif intensity > 250 and intensity <= 500:
        return 'gold'
    else:
        return 'green'

# Création de la carte
map = folium.Map(location=[43.610769, 3.876716], zoom_start=13)

# Ajout des routes à la carte avec la couleur correspondant à l'intensité
for _, row in joined_gdf.iterrows():
    if row.geometry and row.geometry.geom_type == 'LineString':
        coords = [[p[1], p[0]] for p in row.geometry.coords]
        folium.PolyLine(
            locations=coords,
            color=get_color(row['intensity']),
            weight=5
        ).add_to(map)

# Sauvegarder la carte
output_dir = 'map'
os.makedirs(output_dir, exist_ok=True)
map.save(os.path.join(output_dir, 'ecoCompteurRoutes.html'))