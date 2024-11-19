import pandas as pd
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime

# Chargement des données de trajets
trajets_df = pd.read_csv('video/fusion.csv')

# Filtrer les trajets du 1er janvier 2024
date = '2024-01-01'
course = trajets_df[trajets_df['Departure'].str.contains(date)]
course = course.dropna(subset=['latitude_depart', 'longitude_depart', 'latitude_arrivee', 'longitude_arrivee'])

# Charger le graphe des chemins pour vélos à Montpellier
place_name = "Montpellier, France"
graph = ox.graph_from_place(place_name, network_type='bike')

# Configuration du graphique
fig, ax = plt.subplots(figsize=(15, 15))
fig.patch.set_facecolor('black')
ax.set_facecolor('black')

# Affichage du graphe avec des couleurs adaptées au fond noir
ox.plot_graph(
    graph, 
    ax=ax, 
    node_color="gray", 
    edge_color="gray", 
    bgcolor="gray", 
    show=False, 
    close=False
)

# Conversion des colonnes de temps et calcul des secondes depuis minuit
course['Departure'] = pd.to_datetime(course['Departure'])
course['Return'] = pd.to_datetime(course['Return'])
course['start_time'] = (course['Departure'] - course['Departure'].dt.normalize()).dt.total_seconds()
course['end_time'] = (course['Return'] - course['Return'].dt.normalize()).dt.total_seconds()

# Préparation des points pour l'animation
points = []
for idx, trajet in course.iterrows():
    departure_station = (trajet['latitude_depart'], trajet['longitude_depart'])
    arrival_station = (trajet['latitude_arrivee'], trajet['longitude_arrivee'])
    try:
        node_A = ox.distance.nearest_nodes(graph, departure_station[1], departure_station[0])
        node_B = ox.distance.nearest_nodes(graph, arrival_station[1], arrival_station[0])
        route = nx.shortest_path(graph, node_A, node_B, weight='length')
        x, y = zip(*[(graph.nodes[node]['x'], graph.nodes[node]['y']) for node in route])

        point, = ax.plot([], [], 'bo', markersize=10)
        points.append({
            'point': point,
            'x': x,
            'y': y,
            'start_time': trajet['start_time'],
            'end_time': trajet['end_time'],
            'duration': trajet['end_time'] - trajet['start_time']
        })

    except Exception as e:
        print(f"Erreur pour le trajet {idx} : {e}")
        continue

# Fonction d'animation mise à jour
def animate(frame):
    current_time = frame * compression_ratio
    for p in points:
        if p['start_time'] <= current_time <= p['end_time']:
            progress = (current_time - p['start_time']) / p['duration']
            index = int(progress * (len(p['x']) - 1))
            p['point'].set_data([p['x'][index]], [p['y'][index]])  # Mise en séquence des coordonnées
        else:
            p['point'].set_data([], [])

    return [p['point'] for p in points]

compression_ratio = 86400 / 1000  # Compression du temps
ani = FuncAnimation(fig, animate, frames=50, interval=1000 / 30, blit=True)
ani.save('video/montpelliervelo.gif', writer='pillow', fps=30)
plt.show()
