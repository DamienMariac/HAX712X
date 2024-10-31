#%%
import pandas as pd
import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter



# Charger les données vidéo
file_video = 'C:/Users/Abkat/Downloads/geeocoded_stations.csv'
video_data = pd.read_csv(file_video)

# Charger le réseau routier de Montpellier depuis OpenStreetMap
G = ox.graph_from_place("Montpellier, France", network_type="bike")

# Initialisation de la figure
fig, ax = ox.plot_graph(G, show=False, close=False, node_size=0, edge_color="gray", edge_linewidth=0.5)

# Préparer les trajets et les durées
paths = []
durations = []

for index, row in video_data.iterrows():
    depart_coords = row['Geocoded Departure Station']
    arrivee_coords = row['Geocoded Return Station']
    duration = row['Duration (sec.)']
    
    # Convertir les coordonnées en tuples de float
    try:
        depart_lat, depart_lon = map(float, depart_coords.split(','))
        arrivee_lat, arrivee_lon = map(float, arrivee_coords.split(','))
        
        # Trouver les nœuds les plus proches dans le réseau routier
        start_node = ox.distance.nearest_nodes(G, depart_lon, depart_lat)
        end_node = ox.distance.nearest_nodes(G, arrivee_lon, arrivee_lat)
        
        # Calculer le plus court chemin entre les nœuds de départ et d'arrivée
        shortest_path = nx.shortest_path(G, start_node, end_node, weight="length")
        paths.append(shortest_path)
        durations.append(duration)
        
    except Exception as e:
        print(f"Erreur pour le trajet entre {depart_coords} et {arrivee_coords}: {e}")

# Préparer les lignes pour les cyclistes dans l'animation
lines = [ax.plot([], [], color="blue", alpha=0.7, linewidth=1)[0] for _ in paths]

# Fonction d'initialisation pour l'animation
def init():
    for line in lines:
        line.set_data([], [])
    return lines

# Fonction de mise à jour pour chaque frame de l'animation
def update(frame):
    for i, path in enumerate(paths):
        progress = min(frame / durations[i], 1)  # Normaliser la progression du trajet
        num_nodes = int(progress * len(path))
        
        if num_nodes > 1:
            x, y = zip(*[(G.nodes[node]['x'], G.nodes[node]['y']) for node in path[:num_nodes]])
            lines[i].set_data(x, y)
    
    return lines

# Définir le nombre de frames en fonction du trajet le plus long
max_duration = max(durations) if durations else 100
ani = FuncAnimation(fig, update, frames=range(int(max_duration)), init_func=init, blit=True, repeat=False)

# Sauvegarder l'animation sous forme de vidéo
writer = FFMpegWriter(fps=30)
ani.save("simulation_trajets.mp4", writer=writer)
print("La simulation a été sauvegardée sous forme de vidéo : simulation_trajets.mp4")

# %%
