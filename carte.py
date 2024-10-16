#%%
import osmnx as ox
import networkx as nx

ox.config(log_console=True, use_cache=True)

place_name = "Montpellier, France"

graph = ox.graph_from_place(place_name, network_type='walk', simplify=True)

location_1 = ox.geocode("012 Boutonnet, Montpellier, France")
location_2 = ox.geocode("057 Saint-Guilhem, Montpellier, France")
node_start = ox.distance.nearest_nodes(graph, X=location_1[1], Y=location_1[0])
node_end = ox.distance.nearest_nodes(graph, X=location_2[1], Y=location_2[0])

route = nx.shortest_path(graph, node_start, node_end, weight='length')

m = ox.plot_route_folium(graph, route, route_color='red', route_opacity=0.8, route_weight=5)
m.save('route_map.html')
m  









# %%
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
from geopy.geocoders import Nominatim
from shapely.geometry import LineString

# Charger les données
data = pd.read_csv('./collecte/data/extrait.csv')

# Initialiser le géocodeur
geolocator = Nominatim(user_agent="mappage")

# Fonction pour géocoder les stations
def get_location(station):
    location = geolocator.geocode(station + ", Montpellier, France")
    if location:
        return (location.latitude, location.longitude)
    else:
        print(f"Failed to geocode: {station}")
        return (None, None)

# Appliquer la fonction de géocodage
data['Departure_coords'] = data['Departure station'].apply(get_location)
data['Return_coords'] = data['Return station'].apply(get_location)

# Supprimer les lignes où le géocodage a échoué
data = data.dropna(subset=['Departure_coords', 'Return_coords'])

# Assurer que les coordonnées sont disponibles avant de créer des LineString
data['geometry'] = data.apply(lambda row: LineString([row['Departure_coords'], row['Return_coords']]) 
                              if None not in row['Departure_coords'] and None not in row['Return_coords'] 
                              else None, axis=1)

# Nettoyer les données pour retirer les entrées où la création de LineString a échoué
data = data.dropna(subset=['geometry'])
gdf = gpd.GeoDataFrame(data, geometry='geometry')

# Visualisation avec Matplotlib
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, linewidth=1, color='blue')
plt.show()

# Création d'une carte interactive avec Folium
m = folium.Map(location=[43.610769, 3.876716], zoom_start=13)
for _, row in gdf.iterrows():
    folium.PolyLine(locations=[list(row['Departure_coords']), list(row['Return_coords'])], color='blue').add_to(m)
m.save('map.html')
m

# %%
