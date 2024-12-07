#%%
import pandas as pd
import subprocess

df = pd.read_csv('https://drive.google.com/uc?id=1q2hclEfeGOQhxFHqoz9yN_QLh6vL6dJu') #lien vers velomagg.csv

colonnes_a_garder = ['Departure', 'Return', 'Departure station', 'Return station', 'Covered distance (m)', 'Duration (sec.)']
df_reduit = df[colonnes_a_garder]

colonnes = ['Departure station', 'Return station']
corrections = {
    "Ã©": "é",
    "Ã¨": "è",
    "Ã´": "ô",
    "Saint-Guilhem - Courreau": "Saint-Guilhem",
    "FacdesSciences": "Fac des Sciences" 
}
for colonne in colonnes:
    df_reduit[colonne] = df_reduit[colonne].replace(corrections, regex=True)

df_reduit = df_reduit[(df_reduit['Covered distance (m)'] > 0) & (df_reduit['Duration (sec.)'] >= 25)]

#Sauvegarde temporaire du fichier CSV
output_csv = '/tmp/velomagg2.csv'
df_reduit.to_csv(output_csv, index=False)

# Upload sur Google Drive avec rclone
gdrive_path = "gdrive:/Projet/velomagg2.csv"
subprocess.run(["rclone", "copy", output_csv, gdrive_path], check=True)

#lien public
result = subprocess.run(["rclone", "link", gdrive_path], capture_output=True, text=True, check=True)
file_link = result.stdout.strip()

print(f"Le fichier CSV réduit est disponible à l'adresse : {file_link}")

# %%
