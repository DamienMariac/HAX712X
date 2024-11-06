
# %%
import pandas as pd
import folium
import osmnx as ox
import networkx as nx
import itertools

# Charger les données des stations de vélo depuis le fichier CSV
stations_data = pd.read_csv('C:/Users/Abkat/Downloads/stationvelov2.csv') #ici le fichier csv est le stationcoor.csv dans data.

# Créer une carte centrée sur Montpellier
m = folium.Map(location=[43.6119, 3.8772], zoom_start=13)

# Ajouter des points pour chaque station de vélo
for index, row in stations_data.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=5,  # Taille du point
        color='blue',  # Couleur du point
        fill=True,
        fill_color='blue'
    ).add_to(m)

# Charger le réseau routier cyclable de Montpellier depuis OpenStreetMap en filtrant pour le type de voie 'bike'
G = ox.graph_from_place('Montpellier, France', network_type='bike')

# Générer une liste de coordonnées des stations de vélo
station_coords = stations_data[['latitude', 'longitude']].values.tolist()

# Créer un itinéraire global passant par toutes les stations en utilisant uniquement les routes cyclables
for start_coords, end_coords in itertools.combinations(station_coords, 2):
    try:
        # Trouver les nœuds les plus proches dans le réseau routier cyclable
        start_node = ox.distance.nearest_nodes(G, start_coords[1], start_coords[0])
        end_node = ox.distance.nearest_nodes(G, end_coords[1], end_coords[0])
        
        # Calculer le plus court chemin entre les nœuds de départ et d'arrivée en utilisant uniquement les pistes cyclables
        shortest_path = nx.shortest_path(G, start_node, end_node, weight='length')
        path_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in shortest_path]
        
        # Ajouter la ligne représentant le chemin sur la carte
        folium.PolyLine(locations=path_coords, color='red', weight=2.5, opacity=1).add_to(m)
    except nx.NetworkXNoPath:
        print(f"Aucun chemin cyclable trouvé entre les nœuds {start_node} et {end_node}.")

# Enregistrer la carte dans un fichier HTML
m.save("C:/Users/Abkat/Downloads/stations_velo_montpellier.html")
print("La carte interactive avec des itinéraires passant par toutes les stations a été sauvegardée dans 'stations_velo_montpellier.html'.")

# %%
