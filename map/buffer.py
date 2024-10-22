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

traffic_geo = gpd.GeoDataFrame(traffic_data, geometry='geometry')

routes = gpd.read_file('../collecte/data/export.geojson')

traffic_geo.set_crs(routes.crs, inplace=True)

buffer_distance = 0.005  
traffic_geo['buffer'] = traffic_geo.geometry.buffer(buffer_distance)

buffers = gpd.GeoDataFrame(traffic_geo, geometry='buffer', crs=traffic_geo.crs)
intersected_routes = gpd.sjoin(buffers, routes, how='inner', op='intersects')

routes_traffic = intersected_routes.groupby('index_right').agg({
    'intensity': 'mean' 
}).rename(columns={'intensity': 'average_intensity'})


final_routes = routes.join(routes_traffic, how='left')


import folium

map = folium.Map(location=[43.610769, 3.876716], zoom_start=13)

for idx, row in final_routes.iterrows():
    sim_geo = [[point[1], point[0]] for point in row['geometry'].coords] 
    folium.PolyLine(sim_geo,
                    color='green' if row['average_intensity'] < 5000 else 'orange' if row['average_intensity'] < 10000 else 'red',
                    weight=3,
                    opacity=0.8).add_to(map)

map.save('traffic.html')
# %%
