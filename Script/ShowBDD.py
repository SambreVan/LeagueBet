import psycopg2

# Paramètres de connexion à la base de données
dbname = "LeagueBet"
user = "Ivan"
password = "r6sOtXPV5ugzD4q9958"
host = "bdd.ilovebeemo.com"
port = 35475
options = "-c client_encoding=UTF8"

try:
    # Connexion à la base de données
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port,
        options=options,
    )
    cur = conn.cursor()

    # Requête SQL pour sélectionner toutes les données de la table champions
    select_query = "SELECT * FROM champions;"

    # Exécution de la requête
    cur.execute(select_query)

    # Récupération des résultats
    rows = cur.fetchall()

    # Affichage des résultats
    for row in rows:
        print(row)

except psycopg2.Error as e:
    print(f"Erreur lors de l'exécution de la requête : {e}")

finally:
    # Fermeture de la connexion à la base de données
    if cur:
        cur.close()
    if conn:
        conn.close()
