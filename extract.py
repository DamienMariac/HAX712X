import os
import pooch
from bs4 import BeautifulSoup
import requests

url = 'https://data.montpellier3m.fr/dataset/courses-des-velos-velomagg-de-montpellier-mediterranee-metropole'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

#on soupe

# json_links = []
# for link in soup.find_all('a', href=True):
#     href = link['href']
#     if href.endswith('.json'):
#         json_links.append(href)


csv_list = []
for link in soup.find_all('a', href=True):
    href = link['href']
    if href.endswith('.csv'):
        csv_list.append(href)




data_folder = './data'

#on supp

for file in os.listdir(data_folder):
    file_path = os.path.join(data_folder, file)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)  # Supprimer les fichiers ou liens symboliques
            print(f"Fichier supprimé : {file_path}")
    except Exception as e:
        print(f"Erreur en supprimant {file_path} : {e}")


#on ajoute

for url in csv_list:
    file_name = url.split('/')[-1]
    file_path = pooch.retrieve(
        url=url,
        known_hash=None, 
        fname=file_name, 
        path='./data'
    )