#%%
import pandas as pd

stations_df = pd.read_csv('C:/Users/Abkat/Downloads/video/stationcoor.csv')
trajets_df = pd.read_csv('C:/Users/Abkat/Downloads/video/velomagg2.csv')

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

trajets_df.to_csv('C:/Users/Abkat/Downloads/video/fusion.csv', index=False)

print("Le fichier CSV fusionné a été sauvegardé.")



# %%
import pandas as pd
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime


trajets_df = pd.read_csv('C:/Users/Abkat/Downloads/fusion.csv')

#ici je prend seulemnt les trajets du 1er javier
date= '2024-01-01'  
course = trajets_df[trajets_df['Departure'].str.contains(date)]
course = course.dropna(subset=['latitude_depart', 'longitude_depart', 'latitude_arrivee', 'longitude_arrivee'])#suppression des lignes qui contiennent pas de valeurs

#ok
place_name = "Montpellier, France"
graph = ox.graph_from_place(place_name, network_type='bike')


fig, ax = plt.subplots(figsize=(15, 15))

fig.patch.set_facecolor('black')  
ax.set_facecolor('black')         

# Afficher le graphe avec des couleurs adaptées au fond noir
ox.plot_graph(
    graph, 
    ax=ax, 
    node_color="gray", 
    edge_color="gray", 
    bgcolor="gray", 
    show=False, 
    close=False
)


course['Departure'] = pd.to_datetime(course['Departure'])#transformer en tableau manipulable
course['Return'] = pd.to_datetime(course['Return'])#idem


course['start_time'] = (course['Departure'] - course['Departure'].dt.normalize()).dt.total_seconds() # sans ca mon code finissait pas de compiler
course['end_time'] = (course['Return'] - course['Return'].dt.normalize()).dt.total_seconds()

#Chatgpt
lines = []  
points = []  
start_times = course['start_time'].tolist()
end_times = course['end_time'].tolist()

compression_ratio = 86400 / 1000 # pour compressr une jouné zen 30 seco,nde

#là animation
for idx, trajet in course.iterrows():
    departure_station = (trajet['latitude_depart'], trajet['longitude_depart'])
    arrival_station = (trajet['latitude_arrivee'], trajet['longitude_arrivee'])

    try:
        #ici je voulais utiliser les distance qui me sont données mais lorsque je le fais mon pc finit pas de compiler donc jai prris les routes proches
        node_A = ox.distance.nearest_nodes(graph, departure_station[1], departure_station[0])
        node_B = ox.distance.nearest_nodes(graph, arrival_station[1], arrival_station[0])
        route = nx.shortest_path(graph, node_A, node_B, weight='length')

        x, y = zip(*[(graph.nodes[node]['x'], graph.nodes[node]['y']) for node in route])


        #line, = ax.plot(x, y, linewidth=2, alpha=0.5)
        #lines.append(line)

        #animation gif
        point, = ax.plot([], [], 'bo', markersize=5)
        points.append({
            'point': point,
            'x': x,
            'y': y,
            'start_time': trajet['start_time'],
            'end_time': trajet['end_time'],
            'duration': trajet['end_time'] - trajet['start_time']
        })

    except Exception as e:
        print(f"Erreur pour le trajet {idx} : {e}")
        continue


# Fonction d'animation donnée par chatgpt
def animate(frame):
    current_time = frame * compression_ratio
    for p in points:
        if p['start_time'] <= current_time <= p['end_time']:
            progress = (current_time - p['start_time']) / p['duration']
            index = int(progress * (len(p['x']) - 1))
            p['point'].set_data(p['x'][index], p['y'][index])
        else:
            p['point'].set_data([], [])

    return [p['point'] for p in points]


# Création
ani = FuncAnimation(fig, animate, frames=50, interval=1000 / 30, blit=True)
ani.save('C:/Users/Abkat/Downloads/trajet_cycsliste_montpellier.gif', writer='pillow', fps=300)
plt.show()


# %%