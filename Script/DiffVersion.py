from deepdiff import DeepDiff
import json
import os

def charger_json(fichier):
    with open(fichier, 'r') as f:
        return json.load(f)

def afficher_differences(diff):
    # Retourne True s'il y a des changements significatifs
    if not diff:
        return False

    for type_diff, details in diff.items():
        if type_diff == 'values_changed' and len(details) == 1 and "root['version']" in details:
            return False
    return True

def comparer_versions(dossier1, dossier2):
    # Lister tous les fichiers dans les deux dossiers
    fichiers1 = {f for f in os.listdir(dossier1) if f.endswith('.json')}
    fichiers2 = {f for f in os.listdir(dossier2) if f.endswith('.json')}

    # Comparer seulement les fichiers qui existent dans les deux dossiers
    fichiers_communs = fichiers1.intersection(fichiers2)

    for fichier in fichiers_communs:
        chemin1 = os.path.join(dossier1, fichier)
        chemin2 = os.path.join(dossier2, fichier)

        json1 = charger_json(chemin1)
        json2 = charger_json(chemin2)

        differences = DeepDiff(json1, json2, ignore_order=True)

        if afficher_differences(differences):
            print(f"Des changements significatifs ont été réalisés dans {fichier}")

# Exemple d'utilisation
dossier1 = 'Json/13.21.1'
dossier2 = 'Json/13.22.1'

comparer_versions(dossier1, dossier2)
