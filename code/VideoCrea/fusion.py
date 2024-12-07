#%%
import pandas as pd
import subprocess

stations_df = pd.read_csv('https://drive.google.com/uc?id=1RQj7GIXPC-Ut9EeFJtjBUY-05Benqa7s') #lien vers stationcoor.csv
trajets_df = pd.read_csv('https://drive.google.com/uc?id=1jPMzs1dbHGu6u6y0l8mrEApmU3tIlYX-') #lien vers velomagg2.csv

trajets_df['Departure station'] = trajets_df['Departure station'].apply(lambda x: ' '.join(x.split()[1:]))
trajets_df['Return station'] = trajets_df['Return station'].apply(lambda x: ' '.join(x.split()[1:]))

trajets_df = trajets_df.merge(stations_df, left_on='Departure station', right_on='nom', how='left', suffixes=('', '_dep'))
trajets_df = trajets_df.merge(stations_df, left_on='Return station', right_on='nom', how='left', suffixes=('', '_arr'))

columns_to_keep = [
    'Departure', 'Return', 'Departure station', 'Return station', 'Covered distance (m)', 'Duration (sec.)', 'longitude', 'latitude', 'longitude_arr', 'latitude_arr'
]
trajets_df = trajets_df[columns_to_keep]
trajets_df = trajets_df.rename(columns={
    'longitude': 'longitude_depart',
    'latitude': 'latitude_depart',
    'longitude_arr': 'longitude_arrivee',
    'latitude_arr': 'latitude_arrivee'
})

output_csv = '/tmp/fusion.csv'
trajets_df.to_csv(output_csv, index=False)

# Upload sur Google Drive avec rclone
gdrive_path = "gdrive:/Projet/fusion.csv"  # Chemin cible dans Google Drive
subprocess.run(["rclone", "copy", output_csv, gdrive_path], check=True)

# Obtenir le lien public
result = subprocess.run(["rclone", "link", gdrive_path], capture_output=True, text=True, check=True)
file_link = result.stdout.strip()

# Afficher le lien
print(f"Le fichier CSV fusionné est disponible à l'adresse : {file_link}")
# %%
