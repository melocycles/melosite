import sqlite3

CreateDataBase = sqlite3.connect('MyDataBase.db')

cursor = CreateDataBase.cursor()

def createTable():
    # table user
    cursor.execute('''CREATE TABLE IF NOT EXISTS User
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    role TEXT NOT NULL)''')
    # table vélo
    cursor.execute('''CREATE TABLE IF NOT EXISTS Bike (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bycode TEXT,            --Numéro d identification antivol si existant
                    dateEntre DATE,         --date entré en stock
                    marque TEXT,            --marque du vélo
                    typeVelo TEXT,          --vtc, vtt....
                    tailleRoue TEXT,        --12pouces, 14pouces...
                    tailleCadre TEXT,       --enfant, S, M ...
                    photo1 BLOB,            --photo du vélo
                    photo2 BLOB,            --photo du vélo
                    photo3 BLOB,            --photo du vélo                
                    electrique BIT,         --est ce un vélo électrique
                    origine TEXT,           --don, trouvé, récup...
                    status TEXT,            --en stock, réservé, donné....
                    etatVelo TEXT,          --très bon, moyen, pour pièces....
                    prochaineAction TEXT,   --à vendre, à reparer, à recycler....
                    referent TEXT,          --personne en charge du velo
                    valeur FLOAT,           --valeur en euro
                    destinataireVelo TEXT,  --personne ou entité qui a récuperé le vélo
                    descriptionPublic TEXT, --texte libre affiché sur le site
                    descriptionPrive TEXT,  --aucune idée de l'utilité mais je suis un bon petit soldat
                    dateSortie DATE,        --date de la sortie du stock
                    typeSortie TEXT         --vendu, donné, démonté....
                )''')
    # table modif
    cursor.execute('''CREATE TABLE IF NOT EXISTS Modification(
                   id INTEGER PRIMARY KEY,
                   date DATE,                               --date de la création, est ce utilile?
                   benevole TEXT,                           --le nom du bénévole qui a apporté la
                   suiviModif TEXT,                         --la que sera stocké les modifications au fur et à mesure
                   bikeID INTEGER,                          --id d'entrée de table de la table Bike
                   FOREIGN KEY (BikeID) REFERENCES Bike(id) --permet de récupéré l'id de correspondant dans la table Bike
                   )''')
    
















    
def addEntryUser(username, role):
    cursor.execute('''INSERT INTO User (username, role)
    VALUES (?,?)''',(username, role))
    
def addEntryBike(numeroIdentification, nom, description, marque, status, dateEntre, dateSortie, typeSortie):
    cursor.execute('''INSERT INTO Bike 
                        (numeroIdentification,
                        nom,
                        description,
                        marque,
                        status,
                        dateEntre,
                        dateSortie,
                        typeSortie) 
                    VALUES 
                        (?,?,?,?,?,?,?,?)''', (numeroIdentification, nom, description, marque, status, dateEntre, dateSortie, typeSortie))
createTable()

if 0:
    addEntryUser('Toto','admin')
    addEntryBike('13','velo1','jolie','la pierre','en stock','2024-01-01', 'NULL', 'NULL')
    addEntryBike('2541','velo2','superbe et vert','pegeot', 'donné', '2022-03-05', '2023-01-05', 'donné')
    addEntryBike('1111','velo 3','normal','decathlon', 'en stock', '2023-08-05', 'NULL', 'NULL')

CreateDataBase.commit()

cursor.execute('SELECT * FROM User')
cursor.execute('SELECT * FROM Bike')


cursor.close()