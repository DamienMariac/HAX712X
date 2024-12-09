Temps et mémoire
================

Nous avons testé les performances de notre code sur :

- **code/MapCrea/CirculationDuJour.py** qui génère une carte intéractive,

- **code/VideoCrea/video.py** qui génère la vidéo.

Pour cela, nous avons utilisé : 

- Le package *memory-profiler* qui permet de surveiller l'utilisation mémoire au niveau des fonctions Python,

- Le package *time* qui permet de mesurer le temps d'exécution de différentes parties de code,

- La commande *mprof* de *memory-profiler* qui lance le profilage et génère les graphiques d'utilisation mémoire.

Nous obtenons alors les deux graphes suivants : 

.. figure:: Image/circudujour.png
   :alt: Graphique
   :width: 600px
   :name: image1

Pour le fichier *CirculationDuJour.py*  on a : 

- Mémoire maximale utilisée : environ 140 Mo 

- Durée totale d'exécution : Environ 5 secondes.

.. figure:: Image/video_finale.png
   :alt: Graphique 2
   :width: 600px
   :name: image2

Pour le fichier *video.py*  on a : 

- Mémoire maximale utilisée : environ 2900 Mo 

- Durée totale d'exécution : environ 230 secondes.
