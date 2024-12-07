import json
import folium

# Charger les données JSON Lines
data = []
with open('https://drive.google.com/uc?id=1ZcOKTdqVQDGkDIb4GICtQkb3dfGfQDZq', 'r') as file: #lien vers concatenated_data.jsonl
    for line in file:
        data.append(json.loads(line.strip()))

# Créer la carte Folium
mapM = folium.Map(location=[43.6117, 3.8772], zoom_start=12)

# Ajouter des cercles pour chaque entrée valide
for entry in data:
    intensity = entry.get('intensity', 0)
    coordinates = entry.get('location', {}).get('coordinates', None)
    if coordinates and all(coordinates):  # Vérifie que les coordonnées sont valides
        folium.Circle(
            location=[coordinates[1], coordinates[0]],  # Latitude, Longitude
            radius=intensity * 0.25,  # Ajuster le rayon en fonction de l'intensité
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.5,
            tooltip=f"Intensité : {intensity}"
        ).add_to(mapM)

# Sauvegarder la carte
output_dir = 'map'
import os
os.makedirs(output_dir, exist_ok=True)
mapM.save(os.path.join(output_dir, 'ecoCompteurCercle.html'))

print("Carte sauvegardée dans : map/ecoCompteurCercle.html")
