# %%
import folium
import pandas as pd
import json

with open('../collecte/eco_compte/fusion.json') as file: 
    data = json.load(file)

df = pd.DataFrame(data)
df['latitude'] = df['location'].apply(lambda x: x['coordinates'][1])
df['longitude'] = df['location'].apply(lambda x: x['coordinates'][0])
df['intensity'] = df['intensity'].astype(int)
df['laneId'] = df['laneId'].astype(str)  


with open('../collecte/data/export.geojson') as f:  
    routes_geojson = json.load(f)

map = folium.Map(location=[43.610769, 3.876716], zoom_start=13)

for route in routes_geojson['features']:
    if 'geometry' in route and 'coordinates' in route['geometry']:
        path = route['geometry']['coordinates']
        route_id = route['properties'].get('@id', '').split('/')[-1]  

        if route_id in df['laneId'].values:
            intensity = df[df['laneId'] == route_id]['intensity'].iloc[0]
            color = 'green' if intensity < 500 else 'orange' if intensity < 1000 else 'red'
            folium.PolyLine(
                locations=[(p[1], p[0]) for p in path],
                color=color,
                weight=5,
                opacity=0.8
            ).add_to(map)

map.save('traffic_map.html')


# %%
