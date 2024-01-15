import sqlite3
from datetime import date

def checkEntryType(errorMessage:int, dictionary:dict) -> list[str]:
    """vérifie que le type de la donné correspond bien au type attendu. Crée un message d'erreur en fonction de l'endroit où la fonctionaété appelé.
        1 : addBike
        2 : modifyBike
        """
    dictExpectedType = {"bycode":str, "dateEntre":str, "marque":str, "typeVelo":str, "tailleRoue":str, "tailleCadre":str, "photo1":bytes, "photo2":bytes, "photo3":bytes, "electrique":bool, "origine":str, "status":str, "etatVelo":str, "prochaineAction":str, "referent":str, "valeur":float, "destinataireVelo":str, "descriptionPublic":str, "descriptionPrive":str, "dateSortie":str, "typeSortie":str}
    listError = []
    for key, value in dictionary.items():
        if type(value) != dictExpectedType[key] and value != None:
            if errorMessage == 1:
                # éxemple:                   bycode        est  "erreur de saisie" (un     str                  ) alors qu'il devrait être un         int 
                listError.append(f"{key} est {value} (un {type(value)}) alors qu'il devrait être un {dictExpectedType[key]}")
            elif errorMessage == 2:
                listError.append(f"{key} est du mauvais type : {type(value)} au lieu de {dictExpectedType[key]}. valeur entré : {value}")
            
    return listError

def addBike(userName : str, dictOfValue):
    """crée un vélo dans la base de donné Bike et une ligne de mémoire dans la table Modification"""

    # vérifie que les entrés soient du bon type
    typeCheck = checkEntryType(1, dictOfValue)
    if typeCheck: # si il y a des erreurs stop et renvoie de l'erreur sous forme d'un liste de string
        return typeCheck
    
    # ajout du vélo dans la base de donné Bike
    connection = sqlite3.connect("MyDataBase.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Bike (bycode, dateEntre, marque, typeVelo, tailleRoue, tailleCadre, photo1, photo2, photo3, electrique, origine, status, etatVelo, prochaineAction, referent, valeur, destinataireVelo, descriptionPublic, descriptionPrive, dateSortie, typeSortie) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                   (dictOfValue["bycode"], dictOfValue["dateEntre"], dictOfValue["marque"], dictOfValue["typeVelo"], dictOfValue["tailleRoue"], dictOfValue["tailleCadre"], dictOfValue["photo1"], dictOfValue["photo2"], dictOfValue["photo3"], dictOfValue["electrique"], dictOfValue["origine"], dictOfValue["status"], dictOfValue["etatVelo"], dictOfValue["prochaineAction"], dictOfValue["referent"], dictOfValue["valeur"], dictOfValue["destinataireVelo"], dictOfValue["descriptionPublic"], dictOfValue["descriptionPrive"], dictOfValue["dateSortie"], dictOfValue["typeSortie"]))
    connection.commit()

    # ajout d'une entré pour le vélo danas la table Modification
    bike_id = cursor.lastrowid #on récupère l'id du vélo qui a été crée
    cursor.execute("INSERT INTO Modification (date, benevole, suiviModif, BikeID) VALUES (?, ?, ?, ?)",
                   (date.today(), userName , f"le {date.today()} {userName} à crée le vélo", bike_id))
    connection.commit()
    connection.close()


def modifyBike(userName : str, bikeID : int, dictOfChange):
    """Modifie un ou plusieurs attribut d'un vélo et enregistre le/les changements dans la table Modification"""
    # vérifie que les entrés soient du bon type
    typeCheck = checkEntryType(2, dictOfChange)
    if typeCheck: # si il y a des erreurs stop et renvoie de l'erreur sous forme d'un liste de string
        return typeCheck

    connection = sqlite3.connect("MyDataBase.db")
    cursor = connection.cursor()

    # on update toutes les valeurs modifié par l'utilisateur
    for key, value in dictOfChange.items():
        # on récupère d'abord l'ancienne valeur de l'attribut pour la phrase de suivis de modif dans la table de Modification
        cursor.execute("SELECT {} FROM Bike WHERE id = ?".format(key), (bikeID,))
        result = cursor.fetchone() # voir dessous
        oldValue = result[0] 

        cursor.execute("UPDATE Bike SET {} = ? WHERE id = ?".format(key), (value, bikeID)) # format car on ne peut pas passer le nom d'une colonne avec "?"
        connection.commit() # effectue la mise à jour

        # ajout de la modificatoin dans la table Modification
        cursor.execute("SELECT suiviModif FROM Modification WHERE bikeID = ?", (bikeID,)) # sélectionne le suivid de modif du vélo
        result = cursor.fetchone() # voir dessous
        currentSuiviModif = result[0] # récupère le suivi de modif
        newInformation = f"{currentSuiviModif}\nle {date.today()} {userName} à modifié {key} de {oldValue} à {value}" # ajoute la modif aux précédentes
        cursor.execute("UPDATE Modification SET suiviModif = ? WHERE bikeID = ?", (newInformation, bikeID)) # remplace le suivi de modif par celui update
        connection.commit() # effectue la mise à jour

    connection.close()



def readBike(attributeFitler : list = None):
    """retourne la liste des vélos correspondant aux critères, si pas de critère retourne tout"""
    connection = sqlite3.connect("MyDataBase.db")
    cursor = connection.cursor()

    if not attributeFitler: # pas de critère de filtre on les renvoi tous
        cursor.execute("SELECT * FROM Bike")

    sql_query = 'SELECT * FROM Bike WHERE 1=1'
    conditions = []

    
    result = cursor
