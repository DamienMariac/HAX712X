import os
import json
import pandas as pd
import os
import pandas as pd

def fusion_csv(folder_input, output_file):
    """
    Fusionne tous les fichiers CSV d'un dossier donné en un seul fichier CSV de sortie.

    Cette fonction parcourt tous les fichiers dans le dossier spécifié, vérifie si le fichier est un fichier CSV
    (ayant l'extension '.csv'), puis charge chaque fichier CSV en un DataFrame Pandas. Les DataFrames sont ensuite
    concaténés pour créer un DataFrame unique sous format CSV.

    :param folder_input :
        Le chemin vers le dossier contenant les fichiers CSV à fusionner.
    :param output_file : 
        Le chemin vers le dossier contenant les fichiers CSV à fusionner
    """
    data = []
    
    for file_name in os.listdir(folder_input):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_input, file_name)
            
            df = pd.read_csv(file_path)
            data.append(df)
            print(f"Fichier ajouté pour fusion : {file_name}")
    
    # fusionne les DataFrames dans un seul
    fusion_df = pd.concat(data, ignore_index=True)
    
    fusion_df.to_csv(output_file, index=False)
    print(f"Fichier fusionné enregistré sous : {output_file}")

