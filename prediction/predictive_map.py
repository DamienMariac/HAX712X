import pandas as pd
import geopandas as gpd
import folium
from shapely.geometry import Point
import shapely

traffic_df = pd.read_csv('data/all_archive.csv', delimiter=';')

traffic_df['coordinates'] = list(zip(traffic_df['longitude'], traffic_df['latitude']))
traffic_df['date'] = pd.to_datetime(traffic_df['date'].str.split('/').str[0])
traffic_df['day_of_week'] = traffic_df['date'].dt.day_name()

# Calculer la moyenne de l'intensité par jour de la semaine et par coordonnées
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

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
for day in days:
    # Filtrer les données pour le jour spécifique
    day_data = average_traffic[average_traffic['day_of_week'] == day]

    traffic_gdf = gpd.GeoDataFrame(
        day_data,
        geometry=[Point(coords) for coords in day_data['coordinates']],
        crs="EPSG:4326"
    )

    joined_gdf = gpd.sjoin_nearest(routes_gdf, traffic_gdf, how="inner", max_distance=100)

    map = folium.Map(location=[43.610769, 3.876716], zoom_start=13)

    # Ajouter les polylignes sur la carte
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