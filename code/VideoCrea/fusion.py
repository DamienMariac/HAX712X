#%%
import pandas as pd

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

trajets_df.to_csv('data/fusion.csv', index=False)

print("Le fichier CSV fusionné a été sauvegardé.")

# %%
