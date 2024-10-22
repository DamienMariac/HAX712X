#%%
import pandas as pd

###############################################################################


# Charger les données
data = pd.read_csv('./collecte/data/TAM_MMM_CoursesVelomagg.csv')

# 2024-09-25
filtered_data = data[data['Departure'].str.startswith('2024-09-25')]

# Sélectionner uniquement les colonnes 'Departure', 'Departure station', et 'Return station'
selected_columns = filtered_data[['Departure', 'Departure station', 'Return station']]

selected_columns.to_csv('./collecte/data/extrait.csv', index=False)

###############################################################################
#%%
import pandas as pd

# Charger les données depuis le fichier JSON
data = pd.read_json('./eco_compte/fusion.json')

# Tentative de récupérer les coordonnées en vérifiant leur existence
def extract_coordinates(loc):
    if isinstance(loc, dict) and 'coordinates' in loc and loc['coordinates'] is not None:
        if len(loc['coordinates']) == 2:
            return pd.Series([loc['coordinates'][1], loc['coordinates'][0]])
    return pd.Series([None, None])

data[['latitude', 'longitude']] = data['location'].apply(extract_coordinates)

# Supprimer les lignes où les coordonnées sont nulles
data = data.dropna(subset=['latitude', 'longitude'])

# Vérifier à nouveau les données
print(data.head())

# %%
