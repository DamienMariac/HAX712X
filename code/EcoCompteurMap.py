import json
import folium

with open('data/concatenated_data.jsonl', 'r') as file:
    data = json.load(file)

mapM = folium.Map(location=[43.6117, 3.8772], zoom_start=12)

for entry in data:
    intensity = entry.get('intensity', 0)
    coordinates = entry.get('location', {}).get('coordinates', None)
    if coordinates and all(coordinates):

        folium.Circle(
            location=[coordinates[1], coordinates[0]],
            radius=intensity * 0.25,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.5,
            tooltip=f"Intensité : {intensity}"
        ).add_to(mapM)


mapM.save('map/ecoCompteurCercle.html')


