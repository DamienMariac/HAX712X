#%% 
import pandas as pd

df = pd.read_csv('TAM_MMM_CoursesVelomagg.csv')

colonnes_a_garder = ['Departure', 'Return', 'Departure station', 'Return station','Covered distance (m)','Duration (sec.)']
df_reduit = df[colonnes_a_garder]

colonnes = ['Departure station', 'Return station']

corrections = {
    "Ã©": "é",
    "Ã¨": "è",
    "Ã´": "ô",
    "Saint-Guilhem - Courreau": "Saint-Guilhem"
}

for colonne in colonnes:
    df_reduit[colonne] = df_reduit[colonne].replace(corrections, regex=True)

df_reduit.to_csv('velomagg.csv')

# %%
