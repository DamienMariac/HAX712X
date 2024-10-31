from recolte.telechargeur import telecharger_json
from recolte.telechargeur import trouver_urls_json
from recolte.fusionneur import fusionner_json

url_base = "https://data.montpellier3m.fr/dataset/comptages-velo-et-pieton-issus-des-compteurs-de-velo"
dossier_cible = "map/data"

urls_json = trouver_urls_json(url_base)
telecharger_json(urls_json, dossier_cible)
fusionner_json('map/data', 'map/eco_comptage.json')