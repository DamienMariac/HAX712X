import pooch

# URL du fichier CSV
url = 'https://data.montpellier3m.fr/sites/default/files/ressources/MMM_MMM_GeolocCompteurs.csv'

# Téléchargement avec Pooch
file_path = pooch.retrieve(
    url=url,
    known_hash=None, 
    fname='comptage-velo-pieton.csv',
    path='./data' 
)

print(f"Fichier téléchargé et enregistré ici : {file_path}")
