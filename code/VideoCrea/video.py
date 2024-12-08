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

trajets_df = pd.read_csv('https://drive.google.com/uc?id=1ItR7BfdJsxUN1wakCtLic6_uaYqD5eVE')

date = '2024-09-05'
course = trajets_df[trajets_df['Departure'].str.contains(date)]
course = course.dropna(subset=['latitude_depart', 'longitude_depart', 'latitude_arrivee', 'longitude_arrivee'])

place_name = "Montpellier, France"
graph = ox.graph_from_place(place_name, network_type='bike')


course['Departure'] = pd.to_datetime(course['Departure'])
course['Return'] = pd.to_datetime(course['Return'])


features = []


for idx, trajet in course.iterrows():
    departure_station = (trajet['latitude_depart'], trajet['longitude_depart'])
    arrival_station = (trajet['latitude_arrivee'], trajet['longitude_arrivee'])

    try:
        
        node_A = ox.distance.nearest_nodes(graph, departure_station[1], departure_station[0])
        node_B = ox.distance.nearest_nodes(graph, arrival_station[1], arrival_station[0])

        try:
           
            route = nx.shortest_path(graph, node_A, node_B, weight='length')
        except nx.NetworkXNoPath:
            
            all_nodes = list(graph.nodes)
            route = [node_A] + list(np.random.choice(all_nodes, 5)) + [node_B]

       
        coords = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in route]

        
        duration_total = trajet['Duration (sec.)']
        if duration_total <= 0:
            continue

        
        interpolated_points = []
        num_interpolations = 50  

        for i in range(len(coords) - 1):
            lat1, lon1 = coords[i]
            lat2, lon2 = coords[i + 1]
            lats = np.linspace(lat1, lat2, num_interpolations)
            lons = np.linspace(lon1, lon2, num_interpolations)
            interpolated_points.extend(zip(lats, lons))

       
        time_step = duration_total / len(interpolated_points)
        if time_step <= 0:
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
                        'radius': 3
                    }
                }
            })

        if idx % 10 == 0:
            print(f"Trajet {idx + 1}/{len(course)} traité avec succès.")

    except Exception as e:
        print(f"Erreur pour le trajet {idx}: {e}")
        continue


montpellier_coords = [43.610769, 3.876716]
map_base = folium.Map(location=montpellier_coords, zoom_start=13)


timestamped_geojson = TimestampedGeoJson(
    {'type': 'FeatureCollection', 'features': features},
    period="PT5S",        
    duration="PT5S",      
    transition_time=100    
)
map_base.add_child(timestamped_geojson)


output_file = "map_animation_15s.html"
map_base.save(output_file)
print(f"Carte animée générée : {output_file}")



def capture_frames():
    output_dir = "frames"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    
    for i in range(500):  
        map_base.save(os.path.join(output_dir, f"frame_{i:03d}.png"))
        time.sleep(0.01)  

    return output_dir


def create_video_from_frames(frame_dir):
    
    frame_files = [os.path.join(frame_dir, f) for f in sorted(os.listdir(frame_dir)) if f.endswith('.png')]
    clip = ImageSequenceClip(frame_files, fps=30) 
    clip.write_videofile("output_video.mp4", codec="libx264")


frame_dir = capture_frames()


create_video_from_frames(frame_dir)


shutil.rmtree(frame_dir)

print("Vidéo générée : output_video.mp4")


