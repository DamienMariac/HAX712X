import geopandas as gpd
import folium
import json
from shapely.geometry import Point
import os

# Lire les données JSON Lines
traffic_data_path = 'data/concatenated_data.jsonl'
with open(traffic_data_path, 'r') as file:
    traffic_data = [json.loads(line.strip()) for line in file]

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

# Créer un GeoDataFrame
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

# Fonction pour déterminer la couleur
def get_color(intensity):
    if intensity > 2000:
        return 'darkred'
    elif intensity > 1000:
        return 'red'
    elif intensity > 500:
        return 'darkorange'
    elif intensity > 250:
        return 'gold'
    else:
        return 'green'

# Générer une carte Folium
map = folium.Map(location=[43.610769, 3.876716], zoom_start=13)

for _, row in joined_gdf.iterrows():
    if row.geometry and row.geometry.geom_type == 'LineString':
        coords = [[p[1], p[0]] for p in row.geometry.coords]
        folium.PolyLine(
            locations=coords,
            color=get_color(row['intensity']),
            weight=5
        ).add_to(map)

# Sauvegarder la carte dans un dossier
output_dir = 'map'
os.makedirs(output_dir, exist_ok=True)
map.save(os.path.join(output_dir, 'ecoCompteurRoutes.html'))
