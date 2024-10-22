# Projet de groupe HAX712X (BIKEMAP)

## Description du projet

Notre projet consiste à la réalisation d'un site internet autour de la circulation à vélo dans Montpellier. 
Pour ce faire, nous avons utilisé les données mises à disposition par la TAM.
L'objectif étant de faire une carte interactive prédisant le trafic et une vidéo montrant les trajets effectués sur une date donnée.

## Objectif

### Comment prédire le trafic de vélo ?
La circulation dépend du jour (la circulation un dimanche n'est pas la meme qu'un mardi). Ainsi on va prédire en fonction du jour de la semaine en se basant sur les données des semaines précédentes.

### Comment représenter les données ?
On utilise les fichiers (https://data.montpellier3m.fr/dataset/comptages-velo-et-pieton-issus-des-compteurs-de-velo). Les éco-compteurs donnent le nombre de passage à un point donnée. Il faut alors pouvoir interpréter les données afin de les représenter sur une map.
Une autre approche consiste à créer des "buffers" autour de chaque point de mesure (éco-compteurs). Un buffer est une zone géographique qui entoure un point jusqu'à une certaine distance. Vous pouvez considérer qu'une route tombe dans l'influence d'un point de mesure si elle intersecte ou touche le buffer de ce point.

## Packages utilisés

- **NumPy**
La bibliothèque NumPy sert essentiellement pour le calcul numérique. En partie, elle permet la création de tableaux multidimensionnels et propose des fonctions mathématiques avancées pour les manipuler.

- **Pandas**
La bibliothèque Pandas fournit des outils pour lire et écrire des données depuis et vers différents formats.  Elle est particulièrement efficace pour le nettoyage et la préparation des données.

- **Pooch**
La bibliothèque Pooch simplifie le téléchargement et la gestion de données. Elle facilite la gestion des dépendances de fichiers et permet de les stocker à des emplacements spécifiques, ce qui simplifie le partage et l’utilisation des données dans les projets.

- **Folium**
La bibliothèque Folium permet de traiter des données en Python et de les visualiser sur une carte Leaflet interactive. Nous l'utiliserons pour tracer le trafic cycliste.

- **Beautiful Soup**
La bibliothèque Beautiful Soup permet d'extraire des données de fichiers HTML et XML, facilitant ainsi le web scraping.


## Répartition des tâches 

- **Diagramme de Gantt** : Représentation du calendrier de notre projet dans le but de le planifier et d'en avoir un suivi.
- **Données** : Récupération, nettoyage et analyse des données de comptage cyclistes et piétons.
- **Carte intéractive** :  Représentation, sur une carte intéractive, de la prédiction du trafic de vélos à Montpellier sur des périodes données avec des animations pour illustrer le flux de circulation.
- **Vidéo** : Représentation dynamique de l'évolution du trafic de vélos avec des visualisations des points de départ et d'arrivée.
- **Site web** : Gestion et développement d'un site contenant tous les résultats de notre projet : carte intéractive, vidéo prédictive.