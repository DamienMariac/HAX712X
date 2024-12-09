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


def load_data(date):
    """
    Charge et filtre les données pour une date spécifique.

    Args:
        date (str): La date au format 'YYYY-MM-DD'.

    Returns:
        pd.DataFrame: Un dataframe filtré contenant les trajets pour cette date.
    """
    trajets_df = pd.read_csv('https://drive.google.com/uc?id=1ItR7BfdJsxUN1wakCtLic6_uaYqD5eVE')
    course = trajets_df[trajets_df['Departure'].str.contains(date)]
    course = course.dropna(subset=['latitude_depart', 'longitude_depart', 'latitude_arrivee', 'longitude_arrivee'])

    # Conversion des colonnes de dates
    course['Departure'] = pd.to_datetime(course['Departure'])
    course['Return'] = pd.to_datetime(course['Return'])
    return course


def create_graph(place_name="Montpellier, France"):
    """
    Crée un graphe des routes pour une zone donnée.

    Args:
        place_name (str): Le nom de l'endroit.

    Returns:
        networkx.MultiDiGraph: Le graphe des routes.
    """
    return ox.graph_from_place(place_name, network_type='bike')


def process_trajets(course, graph):
    """
    Traite les trajets pour générer les fonctionnalités GeoJSON nécessaires à l'animation.

    Args:
        course (pd.DataFrame): Les trajets filtrés.
        graph (networkx.MultiDiGraph): Le graphe des routes.

    Returns:
        list: Une liste de fonctionnalités GeoJSON.
    """
    features = []

    for idx, trajet in course.iterrows():
        departure_station = (trajet['latitude_depart'], trajet['longitude_depart'])
        arrival_station = (trajet['latitude_arrivee'], trajet['longitude_arrivee'])

        try:
            # Trouver les nœuds les plus proches dans le graphe
            node_A = ox.distance.nearest_nodes(graph, departure_station[1], departure_station[0])
            node_B = ox.distance.nearest_nodes(graph, arrival_station[1], arrival_station[0])

            try:
                # Calcul du chemin le plus court entre les nœuds
                route = nx.shortest_path(graph, node_A, node_B, weight='length')
            except nx.NetworkXNoPath:
                # Si aucun chemin n'est trouvé, générer un chemin aléatoire
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

    return features


def create_map(features, center_coords=[43.610769, 3.876716]):
    """
    Crée une carte interactive avec des trajets animés.

    Args:
        features (list): Les fonctionnalités GeoJSON.
        center_coords (list): Coordonnées centrales de la carte.

    Returns:
        folium.Map: Une carte interactive.
    """
    map_base = folium.Map(location=center_coords, zoom_start=13)

    # Ajout des trajets animés à la carte
    timestamped_geojson = TimestampedGeoJson(
        {'type': 'FeatureCollection', 'features': features},
        period="PT5S",        # Fréquence de répétition
        duration="PT5S",      # Durée pendant laquelle chaque point est affiché
        transition_time=100   # Durée des transitions
    )
    map_base.add_child(timestamped_geojson)
    return map_base


def capture_frames(map_base, output_dir="frames"):
    """
    Capture les frames de la carte pour générer une vidéo.

    Args:
        map_base (folium.Map): La carte interactive.
        output_dir (str): Répertoire pour stocker les frames.

    Returns:
        str: Le chemin du répertoire contenant les frames.
    """
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


def main():
    date = '2024-09-05'

    course = load_data(date)
    graph = create_graph()
    features = process_trajets(course, graph)
    map_base = create_map(features)

    output_file = "map_animation_15s.html"
    map_base.save(output_file)
    print(f"Carte animée générée : {output_file}")

    frame_dir = capture_frames(map_base)
    create_video_from_frames(frame_dir)
    shutil.rmtree(frame_dir)
    print("Vidéo générée : output_video.mp4")


if __name__ == "__main__":
    main()
