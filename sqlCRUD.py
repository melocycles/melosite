import psycopg2
from datetime import date

def checkEntryType(errorMessage:int, dictionary:dict) -> list[str]:
    """vérifie que le type de la donné correspond bien au type attendu. Crée un message d'erreur en fonction de l'endroit où la fonctionaété appelé.

        dictionary est un dictionnaire contenant les attributs et les valeurs à vérifier sous la forme {"marque" : "shimano"}

        errorMesssage est en fonction de la fonction d'origine:
        1 : addBike
        2 : modifyBike
        """
    dictExpectedType = {"bycode":str, "dateEntre":str, "marque":str, "typeVelo":str, "tailleRoue":str, "tailleCadre":str, "photo1":bytes, "photo2":bytes, "photo3":bytes, "electrique":bool, "origine":str, "status":str, "etatVelo":str, "prochaineAction":str, "referent":str, "valeur":float, "destinataireVelo":str, "descriptionPublic":str, "descriptionPrive":str, "dateSortie":str, "typeSortie":str}
    listError = []

    for key, value in dictionary.items(): # on parcour le dictionnaire
        if type(value) != dictExpectedType[key] and value != None: # si la valeur n'est pas celle attendu et n'est pas None (valeur non renseigné)
            if errorMessage == 1:
                # éxemple:                   bycode        est  "erreur de saisie" (un     str                  ) alors qu'il devrait être un         int 
                listError.append(f"{key} est {value} (un {type(value)}) alors qu'il devrait être un {dictExpectedType[key]}")
            elif errorMessage == 2:
                listError.append(f"{key} est du mauvais type : {type(value)} au lieu de {dictExpectedType[key]}. valeur entré : {value}")
            
    return listError


def checkIsItAColumn(potentialColumn:str) -> bool:
    """vérifie que potentialColumn est bien une des colonnes de la table de la base de donné"""
    listAttributesName = ["bycode", "dateEntre", "marque", "typeVelo", "tailleRoue", "tailleCadre", "photo1", "photo2", "photo3", "electrique", "origine", "status", "etatVelo", "prochaineAction", "referent", "valeur", "destinataireVelo", "descriptionPublic", "descriptionPrive", "dateSortie", "typeSortie"]
    if potentialColumn in listAttributesName:
        return True
    return False


def addBike(userName : str, dictOfValue):
    """crée un vélo dans la base de donné Bike et une ligne de mémoire dans la table Modification
    
        userName est le nom de l'utilisateur qui crée le vélo. Il est utilisé pour créer l'entré du vélo dans la table Modification

        dictOfValue est un dictionnaire contenant les attributs et les valeurs du vélo sous la forme {"marque" : "shimano"}
    """

    # vérifie que les entrés soient du bon type
    typeCheck = checkEntryType(1, dictOfValue)
    if typeCheck: # si il y a des erreurs stop et renvoie de l'erreur sous forme d'un liste de string
        return typeCheck
    
    # on vérifie que les attributs nécessaires soient remplis sinon on n'ajoute pas le vélo.
    listAttributesRequired = ["dateEntre", "origine", "status", "referent"]
    for attribute in listAttributesRequired:
        if attribute not in dictOfValue:
            return "%s est nécessaire veuillez le renseigner"
    # On remplit ceux non nécessaire et manquant par None
    listAttributesName = ["bycode", "marque", "typeVelo", "tailleRoue", "tailleCadre", "photo1", "photo2", "photo3", "electrique", "etatVelo", "prochaineAction", "valeur", "destinataireVelo", "descriptionPublic", "descriptionPrive", "dateSortie", "typeSortie"]
    for attribute in listAttributesName:
        if attribute not in dictOfValue:
            dictOfValue[attribute] = None

    
    # Connexion à la base de données
    connection = psycopg2.connect(
        host="localhost",
        database="melodb",
        user="postgres",
        password="mdp"
    )

    cursor = connection.cursor() # création du curseur

    # ajout du vélo dans la base de donné Bike
    cursor.execute("INSERT INTO Bike (bycode, dateEntre, marque, typeVelo, tailleRoue, tailleCadre, photo1, photo2, photo3, electrique, origine, status, etatVelo, prochaineAction, referent, valeur, destinataireVelo, descriptionPublic, descriptionPrive, dateSortie, typeSortie) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id",
                   (dictOfValue["bycode"], dictOfValue["dateEntre"], dictOfValue["marque"], dictOfValue["typeVelo"], dictOfValue["tailleRoue"], dictOfValue["tailleCadre"], dictOfValue["photo1"], dictOfValue["photo2"], dictOfValue["photo3"], dictOfValue["electrique"], dictOfValue["origine"], dictOfValue["status"], dictOfValue["etatVelo"], dictOfValue["prochaineAction"], dictOfValue["referent"], dictOfValue["valeur"], dictOfValue["destinataireVelo"], dictOfValue["descriptionPublic"], dictOfValue["descriptionPrive"], dictOfValue["dateSortie"], dictOfValue["typeSortie"]))
    
    bike_id = cursor.fetchone()[0] #on récupère l'id du vélo qui a été crée
    # ajout du vélo dans la table Modification
    cursor.execute("INSERT INTO Modification (date, benevole, suiviModif, BikeID) VALUES (%s, %s, %s, %s)",
                   (date.today(), userName , f"le {date.today()} {userName} à crée le vélo", bike_id)) # envoie de la requette à la base de donné
    
    connection.commit() # éxécution des requette
    connection.close()



def modifyBike(userName : str, bikeID : int, dictOfChange):
    """Modifie un ou plusieurs attribut d'un vélo et enregistre le/les changements dans la table Modification
    
        userName est le nom de l'utilisateur qui crée le vélo. Il est utilisé pour créer l'entré du vélo dans la table Modification

        dictOfChange est un dictionnaire contenant les attributs et les valeurs à modifier sous la forme {"marque" : "shimano"}
    """
    # vérifie que les entrés soient du bon type
    typeCheck = checkEntryType(2, dictOfChange)
    if typeCheck: # si il y a des erreurs stop et renvoie de l'erreur sous forme d'un liste de string
        return typeCheck
    
    
    # Connexion à la base de données
    connection = psycopg2.connect(
        host="localhost",
        database="melodb",
        user="postgres",
        password="mdp"
    )

    cursor = connection.cursor() # création du curseur

    for key, value in dictOfChange.items():
        if checkIsItAColumn(key): # on vérifie que la clef est bien une colonne de la table de la base de donné
            # on récupère d'abord l'ancienne valeur de l'attribut pour l'enregistrer dans la table de Modification
            cursor.execute("SELECT {} FROM Bike WHERE id = %s".format(key), (bikeID,))
            result = cursor.fetchone() # on récupère la valeur qui nous intéresse
            oldValue = result[0] 

            cursor.execute("UPDATE Bike SET {} = %s WHERE id = %s".format(key), (value, bikeID)) # format car on ne peut pas passer le nom d'une colonne avec "?"

            # ajout de la modificatoin dans la table Modification
            cursor.execute("SELECT suiviModif FROM Modification WHERE bikeID = %s", (bikeID,)) # sélectionne le suivid de modif du vélo correspondant
            result = cursor.fetchone() # récupère le suivi de modif
            currentSuiviModif = result[0] 
            newInformation = f"{currentSuiviModif}\nle {date.today()} {userName} à modifié {key} de {oldValue} à {value}" # ajoute la modif qui vient d'être faite aux précédentes
            cursor.execute("UPDATE Modification SET suiviModif = %s WHERE bikeID = %s", (newInformation, bikeID)) # remplace le suivi de modif par celui update
            connection.commit() # effectue les mise à jour

    connection.close()# récupère le suivi de modif



def readBike(dictOfFilter : dict = None) -> list[dict]:
    """retourne la liste des vélos correspondant aux critères, si pas de critère retourne tout
        retourne une liste de dictionnaires. Les dictionnaires sont les caractéristique des vélos

        dictoOfFilter = {"marque : "shimao", "tailleCadre" : "L" ...}        
    """

    # Connexion à la base de données
    connection = psycopg2.connect(
        host="localhost",
        database="melodb",
        user="postgres",
        password="mdp"
    )
    cursor = connection.cursor()

    if dictOfFilter == None: # si il n'y a pas de filtre afficher tous les vélos
        sqlQuerry = 'SELECT * FROM Bike'

    else: # si il y a au moins un filtre préparer la requette
        sqlQuerry = 'SELECT * FROM Bike WHERE ' # requette de base
        conditions = []
        for key, value in dictOfFilter.items():
            conditions.append(f"{key} = '{value}'") # marque = "shimano"

        # Ajout des conditions à la requête si des filtres sont présents
        if conditions:
            sqlQuerry += " AND ".join(conditions) #transforme la liste crée au dessus en requette SQL 
    
    cursor.execute(sqlQuerry) # éxécute la requette
    result = cursor.fetchall() # on récupère les vélos qui nous intéresse sous forme de liste

    connection.close()
    
    for i in result:
        print(i)

    return result 


def deleteBike(userName:str, bikeID:int) -> None:
    # message d'avertissement
    print("Attention tu vas supprimer un vélo de la base de donné, es tu sur? y/n")
    if input() != 'y':
        print("\nsupression annulé")
        return
    
    print("Veux tu ajouter un commentaire? Vide pour non")
    commentaire = input()

    # Connexion à la base de données
    connection = psycopg2.connect(
        host="localhost",
        database="melodb",
        user="postgres",
        password="mdp"
    )
    cursor = connection.cursor()

    # envoie de la requette à la base de donné
    cursor.execute("DELETE FROM Bike WHERE id = %s", (bikeID,))
    
    # ajout de la modificatoin dans la table Modification
    cursor.execute("SELECT suiviModif FROM Modification WHERE bikeID = %s", (bikeID,)) # sélectionne le suivid de modif du vélo correspondant
    result = cursor.fetchone() # récupère le suivi de modif
    currentSuiviModif = result[0] 
    newInformation = f"{currentSuiviModif}\nle {date.today()} {userName} à supprimer le vélo en précisnat {commentaire}" # ajoute la modif qui vient d'être faite aux précédentes
    cursor.execute("UPDATE Modification SET suiviModif = %s WHERE bikeID = %s", (newInformation, bikeID)) # remplace le suivi de modif par celui update
    connection.commit() # effectue la mise à jour