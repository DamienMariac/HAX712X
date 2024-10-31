import requests
from bs4 import BeautifulSoup
import os


def trouver_urls_json(url_base):
    response = requests.get(url_base)
    if response.status_code != 200:
        print("Échec de la récupération des données")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    liens = soup.find_all('a', href=True)  # Trouver tous les éléments <a> avec un attribut href
    urls_json = [lien['href'] for lien in liens if lien['href'].endswith('.json')]
    
    return urls_json

def telecharger_json(urls, dossier_cible):
    if not os.path.exists(dossier_cible):
        os.makedirs(dossier_cible)
    
    for url in urls:
        nom_fichier = url.split('/')[-1]  # Extraire le nom de fichier de l'URL
        if 'archive' not in nom_fichier:  # Ignorer les fichiers archivés
            chemin_complet = os.path.join(dossier_cible, nom_fichier)
            response = requests.get(url)
            if response.status_code == 200:
                with open(chemin_complet, 'wb') as fichier:
                    fichier.write(response.content)
                print(f"Téléchargé {nom_fichier}")
            else:
                print(f"Échec du téléchargement de {nom_fichier}")
