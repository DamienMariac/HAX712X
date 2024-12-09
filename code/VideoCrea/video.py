#%%
import os
import pandas as pd
import osmnx as ox
import networkx as nx
from datetime import timedelta
import folium
from folium.plugins import TimestampedGeoJson
import numpy as np
import time
from moviepy.editor import ImageSequenceClip
import shutil

# Chargement des données de trajets depuis un fichier CSV
trajets_df = pd.read_csv('https://drive.google.com/uc?id=1ItR7BfdJsxUN1wakCtLic6_uaYqD5eVE')

date = '2024-09-05'
# Filtrage des trajets pour la date spécifiée
course = trajets_df[trajets_df['Departure'].str.contains(date)]
# Suppression des trajets avec des données GPS manquantes
course = course.dropna(subset=['latitude_depart', 'longitude_depart', 'latitude_arrivee', 'longitude_arrivee'])

# Définition de la zone géographique et création du graphe des routes
place_name = "Montpellier, France"
graph = ox.graph_from_place(place_name, network_type='bike')

# Conversion des colonnes de dates en format datetime
course['Departure'] = pd.to_datetime(course['Departure'])
course['Return'] = pd.to_datetime(course['Return'])

# Liste pour stocker les fonctionnalités GeoJSON
features = []

# Boucle pour traiter chaque trajet
for idx, trajet in course.iterrows():
    """
    Traite chaque trajet pour générer une route, interpoler les points entre le départ
    et l'arrivée, et formater les données en GeoJSON pour la visualisation sur la carte.
    """
    departure_station = (trajet['latitude_depart'], trajet['longitude_depart'])
    arrival_station = (trajet['latitude_arrivee'], trajet['longitude_arrivee'])

    try:
        # Trouver les nœuds les plus proches dans le graphe pour les points de départ et d'arrivée
        node_A = ox.distance.nearest_nodes(graph, departure_station[1], departure_station[0])
        node_B = ox.distance.nearest_nodes(graph, arrival_station[1], arrival_station[0])

        try:
            # Calcul du chemin le plus court entre les nœuds
            route = nx.shortest_path(graph, node_A, node_B, weight='length')
        except nx.NetworkXNoPath:
            # Si aucun chemin n'est trouvé, un chemin aléatoire est généré
            all_nodes = list(graph.nodes)
            route = [node_A] + list(np.random.choice(all_nodes, 5)) + [node_B]

        # Extraction des coordonnées des nœuds du chemin
        coords = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in route]

        # Durée totale du trajet
        duration_total = trajet['Duration (sec.)']
        if duration_total <= 0:
            continue

        # Interpolation des points entre chaque segment de la route
        interpolated_points = []
        num_interpolations = 50  # Nombre de points interpolés entre chaque segment

        for i in range(len(coords) - 1):
            lat1, lon1 = coords[i]
            lat2, lon2 = coords[i + 1]
            lats = np.linspace(lat1, lat2, num_interpolations)
            lons = np.linspace(lon1, lon2, num_interpolations)
            interpolated_points.extend(zip(lats, lons))

        # Calcul de l'intervalle temporel entre chaque point interpolé
        time_step = duration_total / len(interpolated_points)
        if time_step <= 0:
            continue

        # Création des objets GeoJSON pour chaque point interpolé
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
                        'radius': 3
                    }
                }
            })

        if idx % 10 == 0:
            print(f"Trajet {idx + 1}/{len(course)} traité avec succès.")

    except Exception as e:
        print(f"Erreur pour le trajet {idx}: {e}")
        continue

# Création de la carte interactive
montpellier_coords = [43.610769, 3.876716]
map_base = folium.Map(location=montpellier_coords, zoom_start=13)

# Ajout des trajets animés à la carte
timestamped_geojson = TimestampedGeoJson(
    {'type': 'FeatureCollection', 'features': features},
    period="PT5S",        # Fréquence de répétition
    duration="PT5S",      # Durée pendant laquelle chaque point est affiché
    transition_time=100   # Durée des transitions
)
map_base.add_child(timestamped_geojson)

# Enregistrement de la carte en fichier HTML
output_file = "map_animation_15s.html"
map_base.save(output_file)
print(f"Carte animée générée : {output_file}")


def capture_frames():
    """
    Capture les frames de la carte pour générer une vidéo.
    Enregistre chaque image PNG dans un répertoire temporaire.
    
    Returns:
        str: Le chemin du répertoire contenant les frames.
    """
    output_dir = "frames"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in range(500):  # Capture 500 frames pour la vidéo
        map_base.save(os.path.join(output_dir, f"frame_{i:03d}.png"))
        time.sleep(0.01)  # Petite pause pour garantir une capture fluide

    return output_dir


def create_video_from_frames(frame_dir):
    """
    Crée une vidéo à partir des images capturées.

    Args:
        frame_dir (str): Chemin du répertoire contenant les images PNG.

    Returns:
        None: La vidéo est enregistrée sous le nom 'output_video.mp4'.
    """
    frame_files = [os.path.join(frame_dir, f) for f in sorted(os.listdir(frame_dir)) if f.endswith('.png')]
    clip = ImageSequenceClip(frame_files, fps=30)  # Vidéo à 30 images par seconde
    clip.write_videofile("output_video.mp4", codec="libx264")


# Capture des frames de la carte
frame_dir = capture_frames()

# Création de la vidéo à partir des frames
create_video_from_frames(frame_dir)

# Suppression du répertoire temporaire contenant les frames
shutil.rmtree(frame_dir)

print("Vidéo générée : output_video.mp4")
