import pandas as pd
import folium
import geopandas as gpd
from shapely.geometry import Point
import json
import os
from MapCrea.CirculationDuJour import get_color  # Assurez-vous que la fonction 'get_color' est correctement importée

class MapAdder : 
    def __init__(self, map_center=[43.610769, 3.876716], zoom_start=13):
        self.map = folium.Map(location=map_center, zoom_start=zoom_start)
    
    def add_station_markers(self, csv_url):
        """
        Ajoute des marqueurs pour les stations VéloMagg à partir d'un fichier CSV.
        
        Args:
            csv_url (str) : URL du fichier CSV contenant les données des stations (latitude, longitude, etc.)
        """
        station = pd.read_csv(csv_url, delimiter=',')
        
        def add_marker(row):
            """
            Ajoute un marqueur sur la carte pour chaque station de vélo.
            """
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"Nom: {row['nom']}<br>Secteur: {row['secteur']}<br>Type: {row['type_stati']}",
                tooltip=row['nom']
            ).add_to(self.map)

        station.apply(add_marker, axis=1)

    def save_station_map(self, file_name="bikestation_map.html"):
        """
        Sauvegarde la carte des stations VéloMagg.
        
        Args:
            file_name (str) : Nom du fichier HTML de sortie pour la carte des stations.
        """
        self.map.save(f"map/{file_name}")
    
    def add_ecocompteur_circles(self, jsonl_file):
        """
        Ajoute des cercles représentant les intensités des éco-compteurs à partir d'un fichier JSONL.
        
        Args:
            jsonl_file (str) : Chemin vers le fichier JSON Lines contenant les données des éco-compteurs.
        """
        data = []
        with open(jsonl_file, 'r') as file:
            for line in file:
                data.append(json.loads(line.strip()))

        mapM = folium.Map(location=[43.6117, 3.8772], zoom_start=12)

        for entry in data:
            intensity = entry.get('intensity', 0)
            coordinates = entry.get('location', {}).get('coordinates', None)
            if coordinates and all(coordinates):
                folium.Circle(
                    location=[coordinates[1], coordinates[0]],
                    radius=intensity * 0.25,
                    color='blue',
                    fill=True,
                    fill_color='blue',
                    fill_opacity=0.5,
                    tooltip=f"Intensité : {intensity}"
                ).add_to(mapM)

        os.makedirs('map', exist_ok=True)
        mapM.save('map/ecoCompteurCercle.html')
        print("Carte sauvegardée dans : map/ecoCompteurCercle.html")

    def execute(self, csv_url, jsonl_file, station_map_name="bikestation_map.html", eco_map_name="ecoCompteurCercle.html"):
        """
        Méthode pour exécuter l'ensemble des actions : 
        1. Ajouter des marqueurs de stations.
        2. Ajouter des cercles des éco-compteurs.
        3. Sauvegarder les cartes.
        """
        # Ajouter des stations
        print("Ajout des marqueurs des stations...")
        self.add_station_markers(csv_url)
        self.save_station_map(station_map_name)
        print(f"Carte des stations sauvegardée sous '{station_map_name}'")

        # Ajouter des cercles des éco-compteurs
        print("Ajout des cercles des éco-compteurs...")
        self.add_ecocompteur_circles(jsonl_file)
        print(f"Carte des éco-compteurs sauvegardée sous '{eco_map_name}'")
