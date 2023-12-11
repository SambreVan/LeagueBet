from deepdiff import DeepDiff
import json

MAX_LINE_LENGTH = 150


def tronquer_ligne(ligne):
    return (ligne[:MAX_LINE_LENGTH] + "...") if len(ligne) > MAX_LINE_LENGTH else ligne


def charger_json(fichier):
    with open(fichier, "r", encoding="utf-8") as f:
        return json.load(f)


def afficher_differences(diff):
    if not diff:
        print("Aucune différence trouvée.")
        return

    changements_significatifs = False

    for type_diff, details in diff.items():
        if (
            type_diff == "values_changed"
            and len(details) == 1
            and "root['version']" in details
        ):
            continue

        changements_significatifs = True
        print()
        print(f"{type_diff}:")
        for chemin, val in details.items():
            if chemin != "root['version']":
                if type_diff == "values_changed":
                    old_value = val["old_value"]
                    new_value = val["new_value"]
                    ligne = f" - {chemin} : de '{old_value}' à '{new_value}'"
                    print(tronquer_ligne(ligne))
                else:
                    ligne = f" - {chemin} : {val}"
                    print(tronquer_ligne(ligne))

    if not changements_significatifs:
        print("Aucun changement significatif n'a été réalisé.")


# Exemple d'utilisation
nom = "Neeko"
fichier1 = "Json/13.21.1/" + nom + ".json"
fichier2 = "Json/13.22.1/" + nom + ".json"

json1 = charger_json(fichier1)
json2 = charger_json(fichier2)

differences = DeepDiff(json1, json2, ignore_order=True)
afficher_differences(differences)
print()
