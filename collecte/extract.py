#%%
import pandas as pd

###############################################################################

data = pd.read_csv('./data/TAM_MMM_CoursesVelomagg.csv') #début / arrivé

selected_data = data[['Departure station', 'Return station']]

output_path = './data/selected_stations.csv'
selected_data.to_csv(output_path, index=False)

###############################################################################
# %%
