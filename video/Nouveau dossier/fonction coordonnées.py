
# %%

#ici, j'ai seulement recuperer les cordonnées des stations que je pouvais.
import pandas as pd
import osmnx as ox

def is_valid_station_name(station_name):
    """Vérifie si le nom de la station est bien formaté."""
    station_name = station_name.strip()
    return station_name.istitle() and (3 <= len(station_name) <= 50)

def geocode_station(station_name):
    """Récupère le vrai nom de la station via geocode() d'osmnx."""
    try:
        location = ox.geocoder.geocode(station_name)
        if location:
            return location[0]  # Renvoie le nom récupéré
    except Exception as e:
        print(f"Erreur lors de la géocodage de '{station_name}': {e}")
    return None

def process_stations(csv_file, output_file):
    """Traite le fichier CSV pour récupérer les vrais noms de stations et filtre les résultats."""
    # Lire le fichier CSV
    df = pd.read_csv(csv_file)

    # Vérifier les colonnes
    if 'Departure station' not in df.columns or 'Return station' not in df.columns:
        print("Les colonnes 'Departure station' et 'Return station' doivent être présentes dans le fichier CSV.")
        return

    # Appliquer le géocodage aux stations de départ et de retour
    df['Geocoded Departure Station'] = df['Departure station'].apply(lambda x: geocode_station(x) if is_valid_station_name(x) else None)
    df['Geocoded Return Station'] = df['Return station'].apply(lambda x: geocode_station(x) if is_valid_station_name(x) else None)

    # Filtrer les lignes où les colonnes de géocodage sont vides
    filtered_df = df.dropna(subset=['Geocoded Departure Station', 'Geocoded Return Station'])

    # Sauvegarder les résultats dans un nouveau fichier CSV
    filtered_df.to_csv(output_file, index=False)
    print(f"Les résultats filtrés ont été sauvegardés dans '{output_file}'.")

# Exemple d'utilisation
csv_input_file ='C:/Users/Abkat/Downloads/video.csv'  # Remplacez par le chemin de votre fichier CSV
csv_output_file = 'C:/Users/Abkat/Downloads/geocoded_stations.csv'  # Nom du fichier de sortie

process_stations(csv_input_file, csv_output_file)

# %%
import pandas as pd
import osmnx as ox

def is_valid_station_name(station_name):
    """Vérifie si le nom de la station est bien formaté."""
    station_name = station_name.strip()
    return station_name.istitle() and (3 <= len(station_name) <= 50)

def geocode_station(station_name):
    """Récupère les coordonnées géographiques de la station via geocode() d'osmnx."""
    try:
        location = ox.geocoder.geocode(station_name)
        if location:
            return location  # Renvoie les coordonnées (latitude, longitude)
    except Exception as e:
        print(f"Erreur lors de la géocodage de '{station_name}': {e}")
    return None

def process_stations(csv_file, output_file):
    """Traite le fichier CSV pour récupérer les coordonnées géographiques des stations et filtre les résultats."""
    # Lire le fichier CSV
    df = pd.read_csv(csv_file)

    # Vérifier les colonnes
    if 'Departure station' not in df.columns or 'Return station' not in df.columns:
        print("Les colonnes 'Departure station' et 'Return station' doivent être présentes dans le fichier CSV.")
        return

    # Appliquer le géocodage aux stations de départ et de retour
    df['Geocoded Departure Station'] = df['Departure station'].apply(lambda x: geocode_station(x) if is_valid_station_name(x) else None)
    df['Geocoded Return Station'] = df['Return station'].apply(lambda x: geocode_station(x) if is_valid_station_name(x) else None)

    # Filtrer les lignes où les colonnes de géocodage sont vides
    filtered_df = df.dropna(subset=['Geocoded Departure Station', 'Geocoded Return Station'])

    # Sauvegarder les résultats dans un nouveau fichier CSV
    filtered_df.to_csv(output_file, index=False)
    print(f"Les résultats filtrés ont été sauvegardés dans '{output_file}'.")

# Exemple d'utilisation
csv_input_file ='C:/Users/Abkat/Downloads/video.csv'  # Remplacez par le chemin de votre fichier CSV
csv_output_file = 'C:/Users/Abkat/Downloads/geeocoded_stations.csv'  # Nom du fichier de sortie

process_stations(csv_input_file, csv_output_file)

# %%
