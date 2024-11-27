# BikeMap

## Description

Le projet BikeMap pour objectif d’analyser les flux cyclistes dans la ville à partir de données issues des trajets VéloMagg, des comptages cyclistes, ainsi que des informations cartographiques d’OpenStreetMap.

Les résultats de cette analyse seront présentés sur un site web interactif permettant aux utilisateurs d'avoir des infromations sur le trafic sur des jours donnés. Grâce à une carte prédictive, ils pourront planifier leurs trajets en fonction de l’intensité du trafic prévu.

## Site web
Vous pouvez consulter le site web du projet ici : [BikeMap](https://damienmariac.github.io/HAX712X/)

## Guide d'installation 

#### 1. Pré-requis :
- Python 3.12
- Git
- Quarto
- Anaconda (optionnel)

#### 2. Clonage du dépot GitHub : 
   
``` python
git clone https://github.com/DamienMariac/HAX712X.git
cd HAX712X
```
#### 3. Installation des packages nécessaires : 

Remarque : Nous vous conseillons de créer un environnement virtuel (avec Conda ou virtual-env par exemple) afin de garder un contrôle simple sur les dépendances installées. 
Voici un exemple de la procédure à suivre avec conda : 

``` python
conda create --name bike-map-env python=3.12
conda activate bike-map-env
```
Enfin vous pouvez installer les packages avec la commande suivante : 
``` python
pip install -r requirements.txt
```

#### 4. Lancement du site web avec Quarto : 
``` python
quarto preview
```

## Auteurs
- [Damien Mariac](https://github.com/DamienMariac/)
- [Julien Ollier](https://github.com/JulienOllier)
- [Abdoul-El Sawadogo](https://github.com/Kader43)
- [Marine Germain](https://github.com/mgermain12)

## Licence  
Ce projet est sous licence MIT. 
Consultez le fichier [LICENSE](LICENSE) pour plus d’informations.  
