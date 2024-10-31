#%%
import pandas as pd
import re

# Charger le fichier CSV
file_path = 'C:/Users/Abkat/Downloads/video.csv'
data = pd.read_csv(file_path)

# Fonction pour remplacer le numéro au début par 'velomagg' et corriger les erreurs d'orthographe
def replace_station_name(station_name):
    # Remplace le numéro et l'espace avant le nom par 'velomagg '
    station_name = re.sub(r'^\d+\s*', 'vélostation ', station_name)
    # Corrige les variantes de 'facdesSciences'
    station_name = re.sub(r'fac\s*des\s*scien[cs]es', 'fac des sciences', station_name, flags=re.IGNORECASE)
    return station_name

# Appliquer la fonction sur les colonnes 'Departure station' et 'Return station'
data['Departure station'] = data['Departure station'].apply(replace_station_name)
data['Return station'] = data['Return station'].apply(replace_station_name)

# Sauvegarder le fichier modifié
output_path = 'C:/Users/Abkat/Downloads/video2.csv'
data.to_csv(output_path, index=False)

print("Modifications effectuées et fichier sauvegardé sous", output_path)

# %%
