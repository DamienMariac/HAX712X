# Projet de groupe HAX712X (BIKEMAP)

## Description du projet

Notre projet vise à développer un site internet autour de la circulation à vélo dans Montpellier. 
Pour ce faire, nous avons utilisé les données mises à disposition par la TAM.
L'objectif est de créer une carte interactive prédisant le trafic et une vidéo montrant les trajets des Vélomagg effectués sur une date donnée.

## Site web
Vous pouvez consulter le site web du projet ici : [BikeMap](https://damienmariac.github.io/HAX712X/)

## Objectif

### Comment prédire le trafic de vélo ?
La circulation varie en fonction des jours (la circulation un dimanche n'est pas la même qu'un mardi). Ainsi nos prédictions tiendront compte du jour de la semaine, en se basant sur les données des semaines précédentes.

### Comment représenter les données ?
Nous récupérons les fichiers dont nous avons besoin sur ce lien (https://data.montpellier3m.fr/dataset/comptages-velo-et-pieton-issus-des-compteurs-de-velo). 
Les éco-compteurs donnent le nombre de passage à un point donnée. L'objectif est d'interpréter ces données pour les visualiser sur une carte.
Notre approche consiste à créer des "buffers" autour de chaque point de mesure (éco-compteurs). Un buffer est une zone géographique qui entourant un point jusqu'à un certain rayon. On considère qu'une route tombe dans l'influence d'un point de mesure si elle intersecte ou touche le buffer de ce point.

## Packages utilisés

- **NumPy** :
La bibliothèque NumPy sert essentiellement pour le calcul numérique. En partie, elle permet la création de tableaux multidimensionnels et propose des fonctions mathématiques avancées pour les manipuler.

- **Pooch** :
La bibliothèque Pooch simplifie le téléchargement et la gestion de données. Elle facilite la gestion des dépendances de fichiers et permet de les stocker à des emplacements spécifiques, ce qui simplifie le partage et l’utilisation des données dans les projets.

- **Folium** :
La bibliothèque Folium permet de traiter des données en Python et de les visualiser sur une carte Leaflet interactive. Nous l'utiliserons pour tracer le trafic cycliste.

- **Beautiful Soup** :
La bibliothèque Beautiful Soup permet d'extraire des données de fichiers HTML et XML, facilitant ainsi le web scraping.

- **Pandas** :
La bibliothèque Pandas fournit des outils pour lire et écrire des données depuis et vers différents formats.  Elle est particulièrement efficace pour le nettoyage et la préparation des données.

- **Geopandas** :
Le package GeoPandas est une extension de Pandas permettant de manipuler des objets géographiques et d'effectuer des opérations spatiales.

- **Shapely** :
La bibliothèque Shapely permet de manipuler et analyser des objets géométriques en réalisant des opérations géométriques comme des calculs de distances. On utilisera Shapely pour créer des "buffers" autour des eco compteurs.

- **recolte**
  C'est un package crée par nous-même.
  - **Scraping** : Ce module permet de récupérer des liens de fichiers JSON depuis une page web (celui de la TAM), de les télécharger, de les combiner en un seul fichier json, puis de supprimer les fichiers individuels après leur utilisation.
  - **Extract** : Ce module extrait les données pertinentes des fichiers JSON, comme l'heure de départ, les stations de départ et d'arrivée (très spécifique pour buffer).


## Répartition des tâches 

- **Diagramme de Gantt** : Représentation du calendrier de notre projet dans le but de le planifier et d'en avoir un suivi.
- **Données** : Récupération, nettoyage et analyse des données de comptage cyclistes et piétons.
- **Carte intéractive** :  Représentation, sur une carte intéractive, de la prédiction du trafic de vélos à Montpellier sur des périodes données avec des animations pour illustrer le flux de circulation.
- **Vidéo** : Représentation dynamique de l'évolution du trafic de vélos avec des visualisations des points de départ et d'arrivée.
- **Site web** : Gestion et développement d'un site contenant tous les résultats de notre projet : carte intéractive, vidéo prédictive.