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
                    uuid CHAR(36) NOT NULL             --uuid associé au compte
                   )''')            

    # table vélo
    cursor.execute('''CREATE TABLE IF NOT EXISTS Bike (
                    id SERIAL PRIMARY KEY NOT NULL, --Id interne à la base de donné, obligatoire
                    bycode VARCHAR(12),             --Numéro d identification antivol si existant
                    dateEntre DATE NOT NULL,        --date entré en stock
                    dateSortie DATE,                --date de la sortie du stock
                    marque VARCHAR(20),             --marque du vélo
                    typeVelo VARCHAR(20),           --vtc, vtt....
                    tailleRoue VARCHAR(10),         --12pouces, 14pouces...
                    tailleCadre VARCHAR(6),         --enfant, S, M ...
                    photo1 BYTEA,                   --photo du vélo
                    photo2 BYTEA,                   --photo du vélo
                    photo3 BYTEA,                   --photo du vélo                
                    electrique BOOLEAN,             --est ce un vélo électrique
                    origine VARCHAR(11) NOT NULL,   --don, trouvé, récup...
                    statusVelo VARCHAR(17) NOT NULL,--en stock, réservé, donné....
                    etatVelo VARCHAR(11),           --Très bon, moyen, mauvais, pour pièces
                    prochaineAction VARCHAR(10),    --à vendre, à reparer, à recycler....
                    referent VARCHAR(30),           --personne en charge du velo
                    valeur FLOAT,                   --valeur en euro
                    destinataireVelo TEXT,          --personne ou entité qui a récuperé le vélo
                    descriptionPublic TEXT,         --texte libre affiché sur le site
                    descriptionPrive TEXT,          --aucune idée de l'utilité mais je suis un bon petit soldat
                    typeSortie VARCHAR(7)           --vendu, donné, démonté....
                )''')

    # table modif
    cursor.execute('''CREATE TABLE IF NOT EXISTS Modification(
                   id SERIAL PRIMARY KEY NOT NULL,          --Id interne à la base de donné, obligatoire
                   bikeID INTEGER NOT NULL,                 --id d'entrée de table de la table Bike
                   suiviModifJSON JSONB[] NOT NULL             --la que sera stocké les modifications au fur et à mesure
                   )''')
    
    connection.commit()

    # fermeture de la connection
    cursor.close()
    connection.close()