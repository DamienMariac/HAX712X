import geopandas as gpd
import folium
import json
import shapely
from shapely.geometry import Point
from IPython.display import HTML

# Données
traffic_data_path = 'data/concatenated_data.jsonl'
with open(traffic_data_path, 'r') as file:
    traffic_data = json.load(file)


valid_traffic_data = [
    item for item in traffic_data 
    if 'coordinates' in item['location'] and item['location']['coordinates'][0] is not None and item['location']['coordinates'][1] is not None
]

traffic_gdf = gpd.GeoDataFrame(
    valid_traffic_data,
    geometry=[Point(data['location']['coordinates']) for data in valid_traffic_data],
    crs="EPSG:4326"
)


routes_gdf = gpd.read_file('data/export.geojson')
routes_gdf = routes_gdf.to_crs(traffic_gdf.crs)


joined_gdf = gpd.sjoin_nearest(routes_gdf, traffic_gdf, how="inner", max_distance=100)


def get_color(intensity):
    """
    Fonction pour déterminer la couleur d'une route en fonction de l'intensité du trafic.

    :param intensity: L'intensité du trafic pour une route donnée.
    :type intensity: float
    :return: La couleur associée à l'intensité du trafic.
    :rtype: str
    """
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
"""
Cette fonction détermine la couleur de la route en fonction de l'intensité du trafic. Les seuils de couleur sont : 
- 'darkred' pour intensité > 2000,
- 'red' pour intensité > 1000,
- 'darkorange' pour intensité > 500,
- 'gold' pour intensité > 250,
- 'green' pour intensité <= 250.
"""



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


HTML(map._repr_html_())

map.save('map/ecoCompteurRoutes.html')