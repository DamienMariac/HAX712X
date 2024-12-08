Guide d'installation du projet 
==============================

1. **Pré-requis :**

   - Python 3.12

   - Git

   - Quarto

   - Anaconda (optionnel)


2. **Clonage du dépôt GitHub :**

   Commencez par cloner le dépôt GitHub avec la commande suivante :

   .. code-block:: python

      git clone https://github.com/DamienMariac/HAX712X.git
      cd HAX712X
      

3. **Installation des packages nécessaires :**

   **Remarque** : Il est recommandé de créer un environnement virtuel (par exemple avec Conda ou virtual-env) pour garder un contrôle simple sur les dépendances installées.

   Exemple avec Conda :

   .. code-block:: python

      conda create --name bike-map-env python=3.12
      conda activate bike-map-env

   Ensuite, vous pouvez installer les packages nécessaires en utilisant la commande suivante :

   .. code-block:: python

      pip install -r requirements.txt