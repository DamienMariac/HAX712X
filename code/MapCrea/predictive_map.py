import pandas as pd
import geopandas as gpd
import folium
from shapely.geometry import Point
import shapely
from CirculationDuJour import get_color


data = pd.read_csv('https://drive.google.com/uc?id=1jH-56gBcZc41KZdH5Dwrj7dB1nRWTdI7', delimiter=';') #lien vers all_archives.csv

data['coordinates'] = list(zip(data['longitude'], data['latitude']))
data['date'] = pd.to_datetime(data['date'].str.split('/').str[0])
data['day_of_week'] = data['date'].dt.day_name()

# Calculer la moyenne de l'intensité par jour de la semaine et par coordonnées
traffic_moy = data.groupby(['day_of_week', 'coordinates']).agg({
    'intensity': 'mean'
}).reset_index()

routes_gdf = gpd.read_file('https://drive.google.com/uc?id=1qy3LPau5A7AfbSY1c1BJHGYPnhgeoFBe') #lien vers export.geojson
routes_gdf = routes_gdf.to_crs("EPSG:4326")

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
for day in days:

    day_data = traffic_moy[traffic_moy['day_of_week'] == day]   # De Lundi à Dimanche

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

    map.save(f"map/{day.lower()}_map.html")