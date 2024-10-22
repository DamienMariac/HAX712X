# Projet de groupe HAX712X (BIKEMAP)

## Description du projet

Notre projet consiste à la réalisation d'un site internet autour de la circulation à vélo dans Montpellier. 
Pour ce faire, nous avons utilisés les données mise à disposition par la Tam.
L'objectif étant de faire une carte interactive predisant le trafic et une vidéo montrant les trajets effectués sur une date donnée.

## Objectif

### Comment prédire le trafique de vélo ?
La circulation depend du jours (la circulation un dimanche n'est pas la meme qu'un mardi). Ainsi on va predire en fonction du jour de la semaine en se basant sur les données des semaines precedantes.

### Comment representé les données ?
On utilise les fichiers (https://data.montpellier3m.fr/dataset/comptages-velo-et-pieton-issus-des-compteurs-de-velo). Les eco compteur donne le nombre de passage à un point donnée. Il faut alors pourvoir interpreter les données afin de les représenter sur une map.
Une autre approche consiste à créer des "buffers" autour de chaque point de mesure (eco compteurs). Un buffer est une zone géographique qui entoure un point jusqu'à une certaine distance. Vous pouvez considérer qu'une route tombe dans l'influence d'un point de mesure si elle intersecte ou touche le buffer de ce point.




## Package utilisé

### Numpy
Nous avons besoin de manipuler des fonctions mathématique, matrices ect... 
Numpy est un package tres souvent utilisé en Datasciences dont nous avons besoin

### Pandas
La bibliothèque Pandas fournit des outils pour lire et écrire des données depuis et vers différents formats, en particulier des fichiers CSV (qui nous intéressent particulièrement). Elle permet aussi un alignement intelligent des données et gestion des données manquantes,
 un alignement des données basé sur des chaînes de caractères, et de trier les données selon divers critères.


### os

### pooch


### Folium
Folium permet de traiter des données en Python et de les visualiser sur une carte Leaflet interactive. On aura besoin de Folium pour tracer les trafiques.


