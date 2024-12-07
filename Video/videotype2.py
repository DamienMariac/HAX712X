#%%
import os
import pandas as pd
import osmnx as ox
import networkx as nx
from datetime import timedelta
import folium
from folium.plugins import TimestampedGeoJson
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from moviepy.editor import ImageSequenceClip
import numpy as np

# Chemin vers le ChromeDriver
CHROMEDRIVER_PATH = 'C:/Users/Abkat/Downloads/chromedriver_win32/chromedriver.exe'

# Charger les données de trajets
trajets_df = pd.read_csv('C:/Users/Abkat/Downloads/fusion.csv')

# Filtrer les trajets du 5 septembre 2024
date = '2024-09-05'
course = trajets_df[trajets_df['Departure'].str.contains(date)]
course = course.dropna(subset=['latitude_depart', 'longitude_depart', 'latitude_arrivee', 'longitude_arrivee'])

# Charger le graphe des chemins pour vélos à Montpellier
place_name = "Montpellier, France"
graph = ox.graph_from_place(place_name, network_type='bike')

# Conversion des colonnes de temps
course['Departure'] = pd.to_datetime(course['Departure'])
course['Return'] = pd.to_datetime(course['Return'])

# Tolérance pour la distance (±10 %)
TOLERANCE = 0.1

# Préparer les données pour Folium
features = []

# Calcul des routes
for idx, trajet in course.iterrows():
    departure_station = (trajet['latitude_depart'], trajet['longitude_depart'])
    arrival_station = (trajet['latitude_arrivee'], trajet['longitude_arrivee'])

    try:
        node_A = ox.distance.nearest_nodes(graph, departure_station[1], departure_station[0])
        node_B = ox.distance.nearest_nodes(graph, arrival_station[1], arrival_station[0])

        distance_given = trajet['Covered distance (m)']
        best_route = None
        distance_calculated = 0

        try:
            route = nx.shortest_path(graph, node_A, node_B, weight='length')
            distance_calculated = sum(ox.utils_graph.get_route_edge_attributes(graph, route, 'length'))

            if distance_given * (1 - TOLERANCE) <= distance_calculated <= distance_given * (1 + TOLERANCE):
                best_route = route
            else:
                best_route = route
        except Exception:
            continue

        coords = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in best_route]

        # Calcul du temps total
        duration_total = trajet['Duration (sec.)']
        if duration_total == 0:  # Ignorer les trajets de durée nulle
            continue

        interpolated_points = []
        for i in range(len(coords) - 1):
            lat1, lon1 = coords[i]
            lat2, lon2 = coords[i + 1]
            num_interpolations = 50
            lats = np.linspace(lat1, lat2, num_interpolations)
            lons = np.linspace(lon1, lon2, num_interpolations)
            interpolated_points.extend(zip(lats, lons))

        time_step = duration_total / len(interpolated_points)
        if time_step == 0:  # Éviter la division par zéro
            continue

        for i, (lat, lng) in enumerate(interpolated_points):
            features.append({
                'type': 'Feature',
                'geometry': {'type': 'Point', 'coordinates': [lng, lat]},
                'properties': {
                    'time': (trajet['Departure'] + timedelta(seconds=i * time_step)).isoformat(),
                    'icon': 'circle',
                    'style': {
                        'color': 'blue',
                        'opacity': 0.8,
                        'fillColor': 'blue',
                        'fillOpacity': 0.6,
                        'radius': 2
                    }
                }
            })

    except Exception:
        continue

# Carte Folium centrée sur Montpellier
montpellier_coords = [43.610769, 3.876716]
map_base = folium.Map(location=montpellier_coords, zoom_start=13)

# Ajouter les cyclistes animés
timestamped_geojson = TimestampedGeoJson(
    {'type': 'FeatureCollection', 'features': features},
    period="PT2H", 
    add_last_point=True,
    duration="PT2M",  
    transition_time=200  
)
map_base.add_child(timestamped_geojson)

# Sauvegarder la carte
output_dir = 'interactive_frames'
os.makedirs(output_dir, exist_ok=True)
output_file = f"{output_dir}/map.html"
map_base.save(output_file)
print(f"Carte interactive sauvegardée sous : {output_file}")

# Initialiser Selenium WebDriver
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)

# Ouvrir le fichier HTML généré
driver.get(f"file:///{os.path.abspath(output_file)}")

# Attendre que la page se charge complètement
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
print("Page web chargée avec succès!")

# Capturer les images
frames_dir = f"{output_dir}/frames"
os.makedirs(frames_dir, exist_ok=True)

NUM_FRAMES = 120  # Nombre total de frames à capturer
FRAME_INTERVAL = 2  # Intervalle entre les captures (secondes)

# Capturer les captures d'écran
for i in range(NUM_FRAMES):
    frame_file = f"{frames_dir}/frame_{i:04d}.png"
    driver.save_screenshot(frame_file)
    print(f"Image capturée : {frame_file}")
    time.sleep(FRAME_INTERVAL)

# Fermer le navigateur
driver.quit()

# Créer la vidéo à partir des frames capturées
frame_files = sorted([os.path.join(frames_dir, f) for f in os.listdir(frames_dir) if f.endswith(".png")])
print(f"Nombre total de frames capturées: {len(frame_files)}")

# Vérifier la présence de frames
assert len(frame_files) > 0, "Aucune image capturée, impossible de créer la vidéo."

# Générer le clip vidéo
video_file = f"{output_dir}/cyclistes_animation.mp4"
clip = ImageSequenceClip(frame_files, fps=1 / FRAME_INTERVAL)
clip.write_videofile(video_file, codec="libx264", fps=30)

print(f"Vidéo générée avec succès : {video_file}")
assert os.path.exists(video_file), f"Le fichier vidéo {video_file} n'a pas été créé."

# %%
