#%%
import pandas as pd

TAMvelomag = 'C:/Users/damie/Documents/MASTER/HAX712X/proj/HAX712X/collecte/data/velomagg.csv'      # CHEMON ABSOLU A CHANGER DE FACON PERSO
data = pd.read_csv(TAMvelomag)

data['Departure'] = pd.to_datetime(data['Departure'])
data['Return'] = pd.to_datetime(data['Return'])

filtered_data = data[(data['Departure'].dt.date == pd.to_datetime("2024-09-01").date())]

useful_columns = filtered_data[['Departure', 'Return', 'Departure station', 'Return station', 'Covered distance (m)', 'Duration (sec.)']]

output_path = 'video.csv'
useful_columns.to_csv(output_path, index=False)

print("Les données filtrées ont été enregistrées sous :", output_path)
print(useful_columns.head()) 