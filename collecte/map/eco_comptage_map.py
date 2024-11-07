import geopandas as gpd
import folium
import json
from shapely.geometry import Point

file_path = 'collecte/map/eco_comptage.json'
with open(file_path, 'r') as file:
    data = json.load(file)

data = [item for item in data if item['location']['coordinates'][0] is not None and item['location']['coordinates'][1] is not None]
gdf = gpd.GeoDataFrame(data)


gdf['geometry'] = [Point(xy) for xy in gdf['location'].apply(lambda loc: loc['coordinates'])]


gdf.set_crs(epsg=4326, inplace=True)

map = folium.Map(location=[43.610769, 3.876716], zoom_start=13)  

def color(intensity):
    if intensity > 1000:
        return 'red'
    elif intensity > 500:
        return 'orange'
    else:
        return 'green'

for _, row in gdf.iterrows():
    folium.CircleMarker(
        location=[row['geometry'].y, row['geometry'].x],
        radius=5,
        color=color(row['intensity']),
        fill=True,
        fill_color=color(row['intensity']),
        fill_opacity=0.7
    ).add_to(map)

map.save('collecte/map/intensité_ecocompteur.html')
