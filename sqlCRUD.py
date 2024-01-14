import sqlite3
from datetime import date
def addBike(userName : str, bycode : int = None, dateEntre : date = None, marque : str = None, typeVelo : str = None, tailleRoue : str = None, tailleCadre : str = None, photo1 : bytes = None, photo2 : bytes = None, photo3 : bytes = None, electrique : bool = None, origine : str = None, status : str = None, etatVelo : str = None, prochaineAction : str= None, referent : str = None, valeur : float = None, destinataireVelo : str = None, descriptionPublic : str = None, descriptionPrive : str = None, dateSortie : date = None, typeSortie : str = None):
    """crée un vélo dans la base de donné Bike et une ligne de mémoire dans la table Modification"""
    
    def checkEntry():
        """Verifie que les entrés correspondent au type attendu"""
        # !!! modifie bien les trois listes en prenant garde à l'ordre !!!
        listExpectedType = [int,  str,       str,    str,      str,        str,         bytes,  bytes,  bytes,  bool,       str,     str,    str,      str,             str,      float,  str,              str,               str,              date,       str ]
        listAttributes = [bycode, dateEntre, marque, typeVelo, tailleRoue, tailleCadre, photo1, photo2, photo3, electrique, origine, status, etatVelo, prochaineAction, referent, valeur, destinataireVelo, descriptionPublic, descriptionPrive, dateSortie, typeSortie]
        listAttributesName = ["bycode", "dateEntre", "marque", "typeVelo", "tailleRoue", "tailleCadre", "photo1", "photo2", "photo3", "electrique", "origine", "status", "etatVelo", "prochaineAction", "referent", "valeur", "destinataireVelo", "descriptionPublic", "descriptionPrive", "dateSortie", "typeSortie"]
        listError = []
        if 1: # vérification de l'intégrité des listes
            expectedLen = 21 # nombre d'ellement dans la liste d'attribut.
            if len(listAttributes) != len(listExpectedType) or len(listAttributes) != len(listAttributesName):
                listError.append("Erreur dans sqlCRUD.py addBike() checkEntry(): listAttributes, listExpectedType et listAttributesName ne correspondent pas")
                return(listError)
            if len(listAttributes) != expectedLen or len(listExpectedType) != expectedLen or len(listAttributesName) !=expectedLen:
                listError.append("Erreur dans sqlCRUD.py addBike() checkEntry(): des ellements on été ajoutés sans modifier le gestionnaire d'erreur, c'est pas jojo")
                return(listError)
        
        for i in range(len(listAttributes)):
            if listExpectedType[i] != type(listAttributes[i]) and listAttributes[i] != None:
                # éxemple:                   bycode        est  "erreur de saisie" (un     str                  ) alors qu'il devrait être un         int 
                listError.append(f"{listAttributesName[i]} est {listAttributes[i]} (un {type(listAttributes[i])}) alors qu'il devrait être un {listExpectedType[i]}")
        
        if len(listError) == 0:
            return None
        else:
            return listError

    # vérifie que les entrés soient du bon type
    typeCheck = checkEntry()
    if typeCheck: # si il y a des erreurs
        # gérer l'erreur
        return typeCheck
    
    # ajout du vélo dans la base de donné Bike
    connection = sqlite3.connect("MyDataBase.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Bike (bycode, dateEntre, marque, typeVelo, tailleRoue, tailleCadre, photo1, photo2, photo3, electrique, origine, status, etatVelo, prochaineAction, referent, valeur, destinataireVelo, descriptionPublic, descriptionPrive, dateSortie, typeSortie) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                   (bycode, dateEntre, marque, typeVelo, tailleRoue, tailleCadre, photo1, photo2, photo3, electrique, origine, status, etatVelo, prochaineAction, referent, valeur, destinataireVelo, descriptionPublic, descriptionPrive, dateSortie, typeSortie))
    connection.commit()

    # ajout d'une entré pour le vélo danas la table Modification
    bike_id = cursor.lastrowid #on récupère l'id du vélo qui a été crée
    cursor.execute("INSERT INTO Modification (date, benevole, suiviModif, BikeID) VALUES (?, ?, ?, ?)",
                   (date.today(), userName , f"le {date.today()} {userName} à crée le vélo", bike_id))
    connection.commit()
    connection.close()


def modifyBike(userName : str, bikeID : int, listAttribute : list, listNewValue : list):
    """Modifie un ou plusieurs attribut d'un vélo et enregistre le/les changements dans la table Modification"""
    def checkEntry(attribute, newValue):
        dictAttributeToType = {'bycode' : str, 'dateEntre' : date, 'marque' : str, 'typeVelo' : str, 'tailleRoue' : str, 'tailleCadre' : str, 'photo1' : bytes, 'photo2' : bytes, 'photo3' : bytes, 'electrique' : bool, 'origine' : str, 'status' : str, 'etatVelo' : str, 'prochaineAction' : str, 'referent' : str, 'valeur' : float, 'destinataireVelo' : str, 'descriptionPublic' : str, 'descriptionPrive' : str, 'dateSortie' : date, 'typeSortie' : date}
        if type(newValue) != dictAttributeToType[attribute]:
            return([dictAttributeToType[attribute]])
        return None

    listError = []
    for i in range(len(listAttribute)):  #" checkError"
            typeCheck = checkEntry(listAttribute[i], listNewValue[i])
            if typeCheck: # si le type d'attribut ne correspond pas
                listError.append(f"{listAttribute[i]} est du mauvais type : {type(listNewValue[i])} au lieu de {typeCheck}). valeur entré : {listNewValue[i]}")

    if listError: # si il y a des ptoblèmes dans les entrés ne pas aller plus loin
        return listError
    

    connection = sqlite3.connect("MyDataBase.db")
    cursor = connection.cursor()

    # on update toutes les valeurs modifié par l'utilisateur
    for i in range(len(listAttribute)):
        # on récupère d'abord l'ancienne valeur de l'attribut pour l'enregistrer dans la table de Modification
        cursor.execute("SELECT {} FROM Bike WHERE id = ?".format(listAttribute[i]), (bikeID,))
        result = cursor.fetchone() # voir dessous
        oldValue = result[0] 

        cursor.execute("UPDATE Bike SET {} = ? WHERE id = ?".format(listAttribute[i]), (listNewValue[i], bikeID)) # format car on ne peut pas passer le nom d'une colonne avec "?"
        connection.commit() # effectue la mise à jour

        # ajout de la modificatoin dans la table Modification
        cursor.execute("SELECT suiviModif FROM Modification WHERE bikeID = ?", (bikeID,)) # sélectionne le suivid de modif du vélo
        result = cursor.fetchone() # voir dessous
        currentSuiviModif = result[0] # récupère le suivi de modif
        newInformation = f"{currentSuiviModif}\nle {date.today()} {userName} à modifié {listAttribute[i]} de {oldValue} à {listNewValue[i]}" # ajoute la modif aux précédentes
        cursor.execute("UPDATE Modification SET suiviModif = ? WHERE bikeID = ?", (newInformation, bikeID)) # remplace le suivi de modif par celui update
        connection.commit() # effectue la mise à jour

    connection.close()



def readBike(attributeFitler : list = None):
    """retourne la liste des vélos correspondant aux critères, si pas de critère retourne tout"""
    connection = sqlite3.connect("MyDataBase.db")
    cursor = connection.cursor()

    if not attributeFitler: # pas de critère de filtre
        cursor.execute("SELECT * FROM Bike")
    
    
    result = cursor
