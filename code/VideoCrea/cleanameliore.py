#%%
import pandas as pd

df = pd.read_csv('video/velomagg.csv')

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

df_reduit.to_csv('video/velomagg2.csv')

# %%
