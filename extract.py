from bs4 import BeautifulSoup
import requests
import os


url = 'https://data.montpellier3m.fr/dataset/comptages-velo-et-pieton-issus-des-compteurs-de-velo'

response = requests.get(url)



soup = BeautifulSoup(response.text, 'html.parser')

for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('.csv'):  
            csv_url = href
            if not csv_url.startswith('http'): 
                csv_url = 'https://data.montpellier3m.fr' + csv_url
            

            csv_response = requests.get(csv_url)
            file_name = os.path.join('data', csv_url.split('/')[-1])
            

            with open(file_name, 'wb') as file:
                file.write(csv_response.content)
            print(f"Fichier téléchargé : {file_name}")
