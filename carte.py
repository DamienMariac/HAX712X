#%%
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

ox.config(log_console=True, use_cache=True)

place_name = "Montpellier, France"

graph = ox.graph_from_place(place_name, network_type='walk')

location_1 = ox.geocode("012 Boutonnet, Montpellier, France")
location_2 = ox.geocode("057 Saint-Guilhem, Montpellier, France")

node_start = ox.distance.nearest_nodes(graph, X=location_1[1], Y=location_1[0])
node_end = ox.distance.nearest_nodes(graph, X=location_2[1], Y=location_2[0])

route = nx.shortest_path(graph, node_start, node_end, weight='length')

fig, ax = ox.plot_graph_route(graph, route, node_size=0)
plt.show()

# %%
