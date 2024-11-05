import geopandas as gpd
import folium
import json
from shapely.geometry import Point

#données
traffic_data_path = 'collecte/map/eco_comptage.json'
with open(traffic_data_path, 'r') as file:
    traffic_data = json.load(file)

#coordonnées null enlevé
valid_traffic_data = [
    item for item in traffic_data 
    if 'coordinates' in item['location'] and item['location']['coordinates'][0] is not None and item['location']['coordinates'][1] is not None
]

#Geo Data Frame
traffic_gdf = gpd.GeoDataFrame(
    valid_traffic_data,
    geometry=[Point(data['location']['coordinates']) for data in valid_traffic_data],
    crs="EPSG:4326"
)


#routes
routes_gdf = gpd.read_file('collecte/map/export.geojson')
routes_gdf = routes_gdf.to_crs(traffic_gdf.crs)

joined_gdf = gpd.sjoin_nearest(routes_gdf, traffic_gdf, how="inner", max_distance=100)

def get_color(intensity):
    if intensity > 1000:
        return 'red'
    elif intensity > 500:
        return 'orange'
    else:
        return 'green'

map = folium.Map(location=[43.610769, 3.876716], zoom_start=13)

for _, row in joined_gdf.iterrows():
    route_color = get_color(row['intensity'])
    folium.PolyLine(
        locations=[[p[1], p[0]] for p in list(row['geometry'].coords)],
        color=route_color,
        weight=5
    ).add_to(map)

map.save('collecte/map/intensité_routes.html')
