import os
import json
import pandas as pd
import os
import pandas as pd

def fusion_csv(folder_input, output_file):
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

fusion_csv('data/archives','data/all_archive.csv')
