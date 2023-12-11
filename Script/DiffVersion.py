from deepdiff import DeepDiff
import json
import os


def charger_json(fichier):
    with open(fichier, "r", encoding="utf-8") as f:
        return json.load(f)


def afficher_differences(diff):
    cles_interessees = ["root['abilities']", "root['stats']"]
    changement_cles_interessees = False
    changement_patchLastChanged = False

    for type_diff, details in diff.items():
        for chemin in details:
            # Exclut les changements dans les entrées "notes" de 'root['abilities']'
            if "['notes']" in chemin and "root['abilities']" in chemin:
                continue

            # Vérifie si le changement est dans 'root['abilities']' ou 'root['stats']'
            if any(cle in chemin for cle in cles_interessees):
                changement_cles_interessees = True

            #   Vérifie si le changement est dans 'root['patchLastChanged']'
            # if "root['patchLastChanged']" in chemin:
            #     changement_patchLastChanged = True

    # Retourne True seulement si les deux conditions sont remplies
    return changement_cles_interessees and changement_patchLastChanged


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
