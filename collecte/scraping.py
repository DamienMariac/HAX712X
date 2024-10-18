import os
import pooch
import requests
from bs4 import BeautifulSoup
import json


url = 'https://data.montpellier3m.fr/dataset/comptages-velo-et-pieton-issus-des-compteurs-de-velo'
data = "./collecte/eco_compte"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# On repère les fichiers à download
json_links = []
for link in soup.find_all('a', href=True):
    href = link['href']
    if href.endswith('.json') and "archive" not in href:
        json_links.append(href)


for json_link in json_links:
    filename = os.path.basename(json_link)
    pooch.retrieve(
        url=json_link,
        known_hash=None,
        fname=filename,
        path=data
    )



# FUSION

fusion = './collecte/eco_compte/fusion.json'

with open(fusion, 'w') as outfile:
    outfile.write('[') 
    first = True
    for json_link in json_links:
        filename = os.path.basename(json_link)
        file_path = pooch.retrieve(
            url=json_link,
            known_hash=None,
            fname=filename,
            path=data
        )
        with open(file_path, 'r') as infile:
            for line in infile:
                if not first:
                    outfile.write(',\n')
                outfile.write(line.strip())
                first = False
        os.remove(file_path)
    outfile.write(']')