import os
import pandas as pd
import osmnx as ox
import networkx as nx
from datetime import timedelta
import folium
from folium.plugins import TimestampedGeoJson
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from moviepy.editor import ImageSequenceClip

# Chemin vers votre pilote ChromeDriver
CHROMEDRIVER_PATH = 'C:/Users/Abkat/Downloads/chromedriver_win32/chromedriver.exe'

# Chargement des données de trajets
trajets_df = pd.read_csv('https://drive.google.com/uc?id=1ItR7BfdJsxUN1wakCtLic6_uaYqD5eVE') #lien vers fusion.csv

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

# Préparer les données pour Folium
features = []
for idx, trajet in course.iterrows():
    departure_station = (trajet['latitude_depart'], trajet['longitude_depart'])
    arrival_station = (trajet['latitude_arrivee'], trajet['longitude_arrivee'])
    try:
        # Trouver les nœuds les plus proches dans le graphe
        node_A = ox.distance.nearest_nodes(graph, departure_station[1], departure_station[0])
        node_B = ox.distance.nearest_nodes(graph, arrival_station[1], arrival_station[0])
        
        # Calculer le chemin le plus court
        route = nx.shortest_path(graph, node_A, node_B, weight='length')
        coords = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in route]

        # Ajouter un point pour chaque étape du trajet avec un timestamp
        for i, (lat, lng) in enumerate(coords):
            features.append({
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [lng, lat],
                },
                'properties': {
                    'time': (trajet['Departure'] + timedelta(seconds=i)).isoformat(),
                    'icon': 'circle',  # Force l'affichage comme cercle
                    'style': {
                        'color': 'blue',  # Couleur bleue
                        'radius': 5,      # Taille du cercle
                        'fillOpacity': 0.8
                    }
                }
            })

    except Exception as e:
        print(f"Erreur pour le trajet {idx} : {e}")
        continue

# Base de la carte Folium centrée sur Montpellier
montpellier_coords = [43.610769, 3.876716]
map_base = folium.Map(location=montpellier_coords, zoom_start=13)

# Ajouter les cyclistes comme points animés
timestamped_geojson = TimestampedGeoJson(
    {
        'type': 'FeatureCollection',
        'features': features,
    },
    period="PT1H",  # Période d'animation
    add_last_point=False,
    duration="PT1M",  # Durée d'apparition d'un point
    transition_time=200,  # Temps de transition
)
timestamped_geojson.add_to(map_base)

# Sauvegarder la carte en HTML
output_dir = 'interactive_frames'
os.makedirs(output_dir, exist_ok=True)
output_file = f"{output_dir}/map.html"
map_base.save(output_file)

# Vérifier l'existence du fichier HTML
assert os.path.exists(output_file), f"Le fichier HTML {output_file} n'a pas été créé."

# Initialiser Selenium pour capturer les captures d'écran
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)
driver.set_window_size(1920, 1080)

# Charger la carte HTML dans Selenium
driver.get(f"file://{os.path.abspath(output_file)}")
time.sleep(5)  # Attendre que la carte se charge

# Capturer des images pour chaque étape de l'animation
frames = []
for i in range(60):  # Nombre de frames dans la vidéo
    screenshot_path = f"{output_dir}/frame_{i:03d}.png"
    driver.save_screenshot(screenshot_path)
    assert os.path.exists(screenshot_path), f"La capture d'écran {screenshot_path} n'a pas été créée."
    frames.append(screenshot_path)
    time.sleep(0.5)  # Pause entre les captures

# Fermer Selenium
driver.quit()

# Convertir les captures en vidéo MP4
frame_rate = 10  # Images par seconde
video_path = 'code/VideoCrea'

# Générer la vidéo à partir des images
clip = ImageSequenceClip(frames, fps=frame_rate)
clip.write_videofile(video_path, codec="libx264", audio=False)

# Vérifier l'existence de la vidéo
assert os.path.exists(video_path), f"La vidéo {video_path} n'a pas été créée."

# Nettoyer les fichiers temporaires
for frame in frames:
    if os.path.exists(frame):
        os.remove(frame)

print(f"Animation MP4 sauvegardée sous : {video_path}")
