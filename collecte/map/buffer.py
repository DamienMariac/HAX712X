#%%
import sys
print(sys.path)  # Cela vous montrera tous les chemins où Python cherche des modules


import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString
import folium
from recolte.scraping import Scraper
from recolte.extract import DataExtractor

scraper = Scraper('https://data.montpellier3m.fr/dataset/comptages-velo-et-pieton-issus-des-compteurs-de-velo', '../collecte/eco_compte')
json_links = scraper.collect_json_links()
scraper.download_and_fuse_json(json_links, '../collecte/eco_compte/fusion.json')


extractor = DataExtractor('../collecte/data/TAM_MMM_CoursesVelomagg.csv', '../collecte/eco_compte/fusion.json')
data_with_coordinates = extractor.extract_coordinates_from_json()

traffic_data = pd.DataFrame(data_with_coordinates)
traffic_data['geometry'] = [Point(xy) for xy in zip(traffic_data['longitude'], traffic_data['latitude'])]
traffic_geo = gpd.GeoDataFrame(traffic_data, geometry='geometry')

routes = gpd.read_file('../collecte/data/export.geojson')
traffic_geo.set_crs(routes.crs, inplace=True)

buffer_distance = 0.005  # 500 mètres autour d'un eco compte (c'est complétement arbitraire)
traffic_geo['buffer'] = traffic_geo.geometry.buffer(buffer_distance)

buffers = gpd.GeoDataFrame(traffic_geo, geometry='buffer', crs=traffic_geo.crs)
intersected_routes = gpd.sjoin(buffers, routes, how='inner', op='intersects')

routes_traffic = intersected_routes.groupby('index_right').agg({
    'intensity': 'mean' 
}).rename(columns={'intensity': 'average_intensity'})

final_routes = routes.join(routes_traffic, how='left')

map = folium.Map(location=[43.610769, 3.876716], zoom_start=13)

for idx, row in final_routes.iterrows():
    sim_geo = [[point[1], point[0]] for point in row['geometry'].coords]
    folium.PolyLine(sim_geo,
                    color='green' if row['average_intensity'] < 5000 else 'orange' if row['average_intensity'] < 10000 else 'red',
                    weight=3,
                    opacity=0.8).add_to(map)

map.save('Montpellier_trafic.html')

# %%
