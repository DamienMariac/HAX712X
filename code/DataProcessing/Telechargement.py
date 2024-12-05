import requests
from bs4 import BeautifulSoup
import os

# URL de la page contenant les fichiers JSON
url = 'https://data.montpellier3m.fr/dataset/comptages-velo-et-pieton-issus-des-compteurs-de-velo'

# Dossier pour stocker les fichiers téléchargés
folder = 'data/json_files'
concatenated_folder = 'data'
os.makedirs(folder, exist_ok=True)
os.makedirs(concatenated_folder, exist_ok=True)

# Récupération des liens JSON depuis la page
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.find_all('a', href=True)

# Filtrer les liens JSON
json_links = [link['href'] for link in links if link['href'].endswith('.json') and 'archive' not in link['href']]

# Téléchargement des fichiers JSON
for link in json_links:
    # Construction de l'URL complète si nécessaire
    json_url = link if link.startswith('http') else f'https://data.montpellier3m.fr{link}'
    json_response = requests.get(json_url)
    json_filename = json_url.split('/')[-1]
    json_path = os.path.join(folder, json_filename)
    with open(json_path, 'wb') as json_file:
        json_file.write(json_response.content)
    print(f"Téléchargé : {json_path}")

# Concaténation des fichiers JSON dans un fichier JSON Lines
concatenated_path = os.path.join(concatenated_folder, 'concatenated_data.jsonl')
with open(concatenated_path, 'w') as concat_file:
    for filename in os.listdir(folder):  # Corriger le dossier utilisé
        if filename.endswith('.json'):
            file_path = os.path.join(folder, filename)  # Utiliser le dossier correct
            with open(file_path, 'r') as file:
                data = file.read().strip()  # Enlever les espaces ou sauts de ligne inutiles
                concat_file.write(data + '\n')  # Écrire les données avec un retour à la ligne
    print(f"Données concaténées dans : {concatenated_path}")
