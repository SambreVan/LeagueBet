from deepdiff import DeepDiff
import json
import os


def charger_json(fichier):
    with open(fichier, "r", encoding="utf-8") as f:
        return json.load(f)


def afficher_differences(diff):
    # Liste des clés à ignorer

    for type_diff, details in diff.items():
        for chemin in details:
            # Condition supplémentaire pour "root['patchLastChanged']"
            if not "root['patchLastChanged']" in chemin:
                continue

            return True  # Un changement significatif a été trouvé

    return False  # Aucun changement significatif trouvé


def comparer_versions(dossier1, dossier2):
    fichiers1 = {f for f in os.listdir(dossier1) if f.endswith(".json")}
    fichiers2 = {f for f in os.listdir(dossier2) if f.endswith(".json")}
    fichiers_communs = fichiers1.intersection(fichiers2)

    nbr_changements = 0

    for fichier in fichiers_communs:
        chemin1 = os.path.join(dossier1, fichier)
        chemin2 = os.path.join(dossier2, fichier)

        json1 = charger_json(chemin1)
        json2 = charger_json(chemin2)

        differences = DeepDiff(json1, json2, ignore_order=True)

        if afficher_differences(differences):
            nbr_changements += 1
            print(f"Des changements significatifs ont été réalisés dans {fichier}")

    return nbr_changements


# Exemple d'utilisation
dossier1 = "Json/13.22.1"
dossier2 = "Json/13.23.1"

nombre_de_changements = comparer_versions(dossier1, dossier2)
print(
    f"Nombre total de fichiers avec changements significatifs : {nombre_de_changements}"
)
