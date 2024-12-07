import io
import requests
import pandas as pd
import json
import geopandas as gpd

class Data:
    """
    Classe de traitement des données. Permet de télécharger, fusionner et sauvegarder des fichiers de données (CSV, JSON, GeoJSON)
    depuis Google Drive.
    
    :param fichiers_ids: Dictionnaire des ID de fichiers Google Drive, où la clé est le nom du fichier et la valeur est l'ID Google Drive.
    :param output_fichier: Nom du fichier de sortie pour les données fusionnées. Par défaut "output.csv".
    """
    
    def __init__(self, fichiers_ids, output_fichier="output.csv"):
        """
        Initialise la classe DataProcessing avec les paramètres nécessaires.

        :param fichiers_ids: Dictionnaire des fichiers à télécharger et traiter.
        :param output_fichier: Nom du fichier de sortie pour le CSV fusionné.
        """
        self.fichiers_ids = fichiers_ids
        self.output_fichier = output_fichier
        self.data_frames = []

    def telechargement_bd_drive(self, fichier_id):
        """
        Télécharge un fichier depuis Google Drive en utilisant son ID et le charge directement en mémoire.
        La méthode détecte le type de fichier (CSV, JSON, GEOJSON) et le charge en conséquence.

        :param fichier_id: L'ID du fichier à télécharger depuis Google Drive.
        :return: Le contenu du fichier téléchargé sous forme binaire.
        """
        base_url = 'https://drive.google.com/uc?id='
        fichier_url = f"{base_url}{fichier_id}"

        try:
            response = requests.get(fichier_url)
            response.raise_for_status()  # Vérifie que la réponse est OK (status code 200)
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors du téléchargement de {fichier_id}: {e}")
            return None

    def charger_fichier(self, fichier_content, fichier_nom):
        """
        Charge un fichier en DataFrame ou GeoDataFrame en fonction du type de fichier.
        Les fichiers sont traités en mémoire sans être enregistrés localement.

        :param fichier_content: Le contenu du fichier téléchargé (binaire).
        :param fichier_nom: Le nom du fichier, utilisé pour déterminer son type (CSV, JSON, GeoJSON).
        :return: Un DataFrame ou GeoDataFrame si le fichier est valide, sinon None.
        """
        extension = fichier_nom.split('.')[-1].lower()

        if extension == 'csv':
            return pd.read_csv(io.BytesIO(fichier_content)) 
        elif extension == 'json':
            data = json.loads(fichier_content.decode('utf-8'))
            return pd.json_normalize(data)  
        elif extension == 'geojson':
            return gpd.read_file(io.BytesIO(fichier_content)) 
        else:
            print(f"Extension non prise en charge : {extension}")
            return None

    def fusionner_fichiers(self):
        """
        Fusionne tous les fichiers téléchargés depuis Google Drive en un seul DataFrame.

        :return: Un DataFrame fusionné de tous les fichiers téléchargés, ou None si aucun fichier valide.
        """
        for fichier_nom, fichier_id in self.fichiers_ids.items():
            fichier_content = self.telechargement_bd_drive(fichier_id)
            if fichier_content:
                df = self.charger_fichier(fichier_content, fichier_nom)
                if df is not None:
                    self.data_frames.append(df)
                    print(f"Fichier ajouté pour fusion : {fichier_nom}")

        if self.data_frames:
            fusion_df = pd.concat(self.data_frames, ignore_index=True, sort=False)
            return fusion_df
        else:
            print("Aucun fichier valide à fusionner.")
            return None

    def sauvegarder_csv(self, df):
        """
        Sauvegarde le DataFrame fusionné dans un fichier CSV localement.

        :param df: Le DataFrame fusionné à sauvegarder.
        """
        df.to_csv(self.output_fichier, index=False)
        print(f"Fichier sauvegardé sous : {self.output_fichier}")

    def executer(self):
        """
        Cette méthode coordonne l'exécution de toutes les actions de traitement des données.

        Elle télécharge, fusionne et sauvegarde les fichiers traités en un seul CSV.
        """
        fusion_df = self.fusionner_fichiers()
        
        if fusion_df is not None:
            self.sauvegarder_csv(fusion_df)
