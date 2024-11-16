import geopandas as gpd
import folium
import json
import pandas as pd
import shapely
from shapely.geometry import LineString, Point 

with open('data/eco_comptage_archive.json', 'r') as file:
    traffic_data = json.load(file)

valid_traffic_data = [
    item for item in traffic_data 
    if 'coordinates' in item['location'] and item['location']['coordinates'][0] is not None and item['location']['coordinates'][1] is not None
]

traffic_df = pd.DataFrame(valid_traffic_data)

traffic_df['dateObserved'] = pd.to_datetime(traffic_df['dateObserved'].str.split('/').str[0])

# Ajouter une colonne pour le jour de la semaine
traffic_df['day_of_week'] = traffic_df['dateObserved'].dt.day_name()

traffic_df['coordinates'] = traffic_df['location'].apply(lambda loc: tuple(loc['coordinates']))
# Calculer la moyenne par jour de la semaine
average_traffic = traffic_df.groupby(['day_of_week', 'coordinates']).agg({
    'intensity': 'mean'
}).reset_index()


routes_gdf = gpd.read_file('data/export.geojson')
routes_gdf = routes_gdf.to_crs("EPSG:4326")

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

# Création de cartes pour chaque jour de la semaine
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
for day in days:
    # Filtrer les données pour le jour spécifique
    day_data = average_traffic[average_traffic['day'] == day]

    traffic_gdf = gpd.GeoDataFrame(
        day_data,
        geometry=[Point(coords) for coords in day_data['coordinates']],
        crs="EPSG:4326"
    )

    joined_gdf = gpd.sjoin_nearest(routes_gdf, traffic_gdf, how="inner", max_distance=100)

    map = folium.Map(location=[43.610769, 3.876716], zoom_start=13)
    for _, row in joined_gdf.iterrows():
        route_color = get_color(row['intensity'])
        if isinstance(row.geometry, shapely.geometry.LineString):
            coords = [[p[1], p[0]] for p in list(row.geometry.coords)]
        elif isinstance(row.geometry, shapely.geometry.Polygon):
            coords = [[p[1], p[0]] for p in list(row.geometry.exterior.coords)]
        else:
            continue

        folium.PolyLine(
            locations=coords,
            color=route_color,
            weight=5
        ).add_to(map)

    map.save(f"prediction/{day.lower()}_map.html")
