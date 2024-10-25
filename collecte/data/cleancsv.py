#%% 
import pandas as pd

df = pd.read_csv('selected_stations.csv')
colonnes = ['Departure station', 'Return station']

corrections = {
    "Ã©": "é",
    "Ã¨": "è",
    "Ã´": "ô"
}

for colonne in colonnes:
    df[colonne] = df[colonne].replace(corrections, regex=True)

#%% 
df.to_csv('selected_stations_corrected.csv')
