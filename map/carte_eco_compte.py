import json
import folium

with open('collecte/eco_compte/fusion.json', 'r') as f:
    data = json.load(f)


map_center = [43.6, 3.89]  
mymap = folium.Map(location=map_center, zoom_start=12)


for entry in data:
    coordinates = entry['location']['coordinates']
    if coordinates and all(coordinates):
        folium.Marker(
            location=[coordinates[1], coordinates[0]],  
            popup=f"Intensity: {entry['intensity']}"
        ).add_to(mymap)

mymap.save('./map/eco_compte.html')


# %%
