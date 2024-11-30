import requests
from bs4 import BeautifulSoup
import os

url = 'https://data.montpellier3m.fr/dataset/comptages-velo-et-pieton-issus-des-compteurs-de-velo'

folder = 'data/json_files'
donne = 'data'
os.makedirs(folder, exist_ok=True)

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.find_all('a', href=True)

json_links = [link['href'] for link in links if link['href'].endswith('.json') and 'archive' not in link['href']]

for link in json_links:
    json_url = link
    json_response = requests.get(json_url)
    json_filename = json_url.split('/')[-1]
    json_path = os.path.join(folder, json_filename)
    with open(json_path, 'wb') as json_file:
        json_file.write(json_response.content)

concatenated_path = os.path.join(donne, 'concatenated_data.jsonl')  # '.jsonl' pour JSON Lines
with open(concatenated_path, 'w') as concat_file:
    for filename in os.listdir(donne):
        if filename.endswith('.json'):
            file_path = os.path.join(donne, filename)
            with open(file_path, 'r') as file:
                data = file.read()
                concat_file.write(data + '\n')  # Écrire les données avec un retour à la ligne