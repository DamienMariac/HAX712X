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
# %%
