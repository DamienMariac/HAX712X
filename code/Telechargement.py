# Telecharge les donnée de puis le site de la tam (automatisé par github action)

import requests
from bs4 import BeautifulSoup
import os

# URL de la page où se trouvent les fichiers JSON
url = 'https://data.montpellier3m.fr/dataset/comptages-velo-et-pieton-issus-des-compteurs-de-velo'

# Dossier pour stocker les fichiers JSON
folder = 'data/json_files'
donne = 'data'
os.makedirs(folder, exist_ok=True)

# Obtenir la page et extraire les liens
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.find_all('a', href=True)

# Filtrer les liens qui se terminent par '.json' et exclure ceux qui contiennent "archive"
json_links = [link['href'] for link in links if link['href'].endswith('.json') and 'archive' not in link['href']]

# Télécharger les fichiers JSON
for link in json_links:
    json_url = link
    json_response = requests.get(json_url)
    json_filename = json_url.split('/')[-1]
    json_path = os.path.join(folder, json_filename)
    with open(json_path, 'wb') as json_file:
        json_file.write(json_response.content)

# Concaténer le contenu de tous les fichiers JSON dans un fichier, chaque fichier sur une ligne
concatenated_path = os.path.join(donne, 'concatenated_data.jsonl')  # '.jsonl' pour JSON Lines
with open(concatenated_path, 'w') as concat_file:
    for filename in os.listdir(donne):
        if filename.endswith('.json'):
            file_path = os.path.join(donne, filename)
            with open(file_path, 'r') as file:
                data = file.read()
                concat_file.write(data + '\n')  # Écrire les données avec un retour à la ligne