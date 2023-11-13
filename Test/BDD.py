import psycopg2
from psycopg2 import OperationalError


def creer_connexion(host_name, port, user_name, user_password, db_name):
    """Crée une connexion au serveur PostgreSQL.
    :param host_name: nom de l'hôte ou adresse IP du serveur PostgreSQL.
    :param port: port du serveur PostgreSQL.
    :param user_name: nom d'utilisateur PostgreSQL.
    :param user_password: mot de passe PostgreSQL.
    :param db_name: nom de la base de données à laquelle se connecter.
    :return: objet de connexion ou None.
    """
    connexion = None
    try:
        connexion = psycopg2.connect(
            host=host_name,
            port=port,
            user=user_name,
            password=user_password,
            dbname=db_name,
        )
        print("Connexion à la base de données PostgreSQL réussie")
    except OperationalError as e:
        print(f"L'erreur '{e}' est survenue")

    return connexion


# Remplacez les valeurs suivantes par vos informations de connexion
host = "bd.ilovebeemo.com"
port = 35475
user = "Test"
password = "Ivan44119"
database = "LeagueBet"

# Créer une connexion à la base de données
conn = creer_connexion(host, port, user, password, database)

# Assurez-vous de fermer la connexion une fois que vous avez fini
if conn is not None:
    conn.close()
