import os

def fusionner_json(dossier_source, fichier_sortie):
    with open(fichier_sortie, 'w', encoding='utf-8') as fichier_final:
        fichier_final.write("[\n") 
        first = True
        for nom_fichier in os.listdir(dossier_source):
            chemin_fichier = os.path.join(dossier_source, nom_fichier)
            if nom_fichier.endswith('.json') and 'archive' not in nom_fichier:
                with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
                    ligne_json = fichier.readline().strip()
                    if ligne_json:
                        if not first:
                            fichier_final.write(",\n")  
                        first = False
                        fichier_final.write(ligne_json)  
        fichier_final.write("\n]")

    print(f"Tous les fichiers JSON ont été fusionnés dans {fichier_sortie}")

