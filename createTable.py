import psycopg2

def createTable():
    # Connexion à la base de données
    connection = psycopg2.connect(
        host="localhost",
        database="melodb",
        user="postgres",
        password="mdp"
    )

    # création du curseur
    cursor = connection.cursor()

    # table user
    cursor.execute('''CREATE TABLE IF NOT EXISTS Member
                   (id SERIAL PRIMARY KEY NOT NULL,       --Id interne à la base de donné, obligatoire
                    username VARCHAR(30) UNIQUE NOT NULL, --Nom d'utilisateur
                    password CHAR(64) NOT NULL,           --mot de passe de l'utilisateur
                    role VARCHAR(6) NOT NULL,             --Role (admin, readOnly, user)
                    uuid CHAR(36) NOT NULL                --uuid associé au compte
                   )''')            

    # table vélo
    cursor.execute('''CREATE TABLE IF NOT EXISTS Bike (
                    id SERIAL PRIMARY KEY NOT NULL,     --Id interne à la base de donné, obligatoire
                    bicycode VARCHAR(12),               --Numéro d identification antivol si existant
                    entry_daye DATE NOT NULL,           --date entré en stock
                    exit_date DATE,                     --date de la sortie du stock
                    brand VARCHAR(20),                  --marque du vélo
                    bike_type VARCHAR(20),              --vtc, vtt....
                    wheel_size VARCHAR(15),             --12pouces, 14pouces...
                    frame_size VARCHAR(6),              --enfant, S, M ...
                    is_electric BOOLEAN,                --est ce un vélo électrique
                    origine VARCHAR(11) NOT NULL,       --don, trouvé, récup...
                    bike_status VARCHAR(17) NOT NULL,   --en stock, réservé, donné....
                    bike_state VARCHAR(11),             --Très bon, moyen, mauvais, pour pièces
                    next_action VARCHAR(10),            --à vendre, à reparer, à recycler....
                    ref VARCHAR(30),                    --personne en charge du velo
                    values FLOAT,                       --valeur en euro
                    bike_dest TEXT,                     --personne ou entité qui a récuperé le vélo
                    public_desc TEXT,                   --texte libre affiché sur le site
                    private_desc TEXT,                  --aucune idée de l'utilité mais je suis un bon petit soldat
                    name VARCHAR(25),                   --Nom affiché dans parcour vélo
                    exit_type VARCHAR(25)               --vendu, donné, démonté....
                )''')

    # table photo
    cursor.execute('''CREATE TABLE IF NOT EXISTS Pictures(
                   id SERIAL PRIMARY KEY NOT NULL,          --Id interne à la base de donné, obligatoire
                   bikeID INTEGER NOT NULL,                 --id d'entrée de table de la table Bike
                   name VARCHAR(70) NOT NULL,               --nom de l'image
                   is_principal BOOL NOT NULL,              --est ce que c'est la photo principal
                   data BYTEA                               --champ modifié
                   )''')

    # table modif
    cursor.execute('''CREATE TABLE IF NOT EXISTS Modification(
                   id SERIAL PRIMARY KEY NOT NULL,          --Id interne à la base de donné, obligatoire
                   bikeID INTEGER NOT NULL,                 --id d'entrée de table de la table Bike
                   timestamp datetime.datetime NOT NULL,    --date de modification
                   volunteer VARCHAR(70) NOT NULL,          --bénévole faisant la modif
                   modified_field VARCHAR(70) NOT NULL,     --champ modifié
                   old_value VARCHAR(150) NOT NULL,         --ancienne valeur
                   new_value VARCHAR(150) NOT NULL          --nouvelle valeur
                   )''')
    
    connection.commit()

    # fermeture de la connection
    cursor.close()
    connection.close()