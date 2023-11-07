import mysql.connector
from mysql.connector import Error


def creer_connexion(host_name, user_name, user_password, db_name):
    """Crée une connexion au serveur MySQL.
    :param host_name: nom de l'hôte ou adresse IP du serveur MySQL.
    :param user_name: nom d'utilisateur MySQL.
    :param user_password: mot de passe MySQL.
    :param db_name: nom de la base de données à laquelle se connecter.
    :return: objet de connexion ou None.
    """
    connexion = None
    try:
        connexion = mysql.connector.connect(
            host=host_name, user=user_name, passwd=user_password, database=db_name
        )
        print("Connexion à la base de données MySQL réussie")
    except Error as e:
        print(f"L'erreur '{e}' est survenue")

    return connexion


# Remplacez les valeurs suivantes par vos informations de connexion
host = "127.0.0.1"
user = "root"
password = ""
database = "mediadb"

# Créer une connexion à la base de données
conn = creer_connexion(host, user, password, database)

# Assurez-vous de fermer la connexion une fois que vous avez fini
if conn is not None and conn.is_connected():
    conn.close()
