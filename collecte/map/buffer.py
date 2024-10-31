import geopandas as gpd
import folium
import json
from shapely.geometry import Point


file_path = 'collecte/map/eco_comptage.json'
with open(file_path, 'r') as file:
    data = json.load(file)

gdf = gpd.GeoDataFrame(data)

gdf['geometry'] = [Point(xy) for xy in zip(gdf['longitude'], gdf['latitude'])]
gdf.set_crs(epsg=4326, inplace=True) 

gdf['geometry'] = gdf.apply(lambda row: row['geometry'].buffer(row['intensity'] * 0.5), axis=1)

map_center = gdf.geometry.unary_union.centroid
map = folium.Map(location=[map_center.y, map_center.x], zoom_start=13)

def style_function(feature):
    return {
        'fillColor': '#ffaf00',
        'color': '#556b2f',
        'weight': 1.5,
        'fillOpacity': 0.5
    }

folium.GeoJson(gdf, style_function=style_function).add_to(map)

map.save('map.html')
