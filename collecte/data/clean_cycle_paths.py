# %%
import pandas as pd

df = pd.read_csv('cycle_paths.csv')

colonnes = [
    'id_local', 'id_osm', 'code_com_d', 'ame_d', 'sens_d', 'local_d', 
    'statut_d','code_com_g', 'ame_g', 'sens_g','statut_g', 'date_maj'
]

df = df[colonnes]

df = df[(df['statut_d'] == 'EN SERVICE') & (df['statut_g'] == 'EN SERVICE')]

df.to_csv('active_bike_paths.csv', index=False)
# %%
