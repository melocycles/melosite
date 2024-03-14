import csv
import json
import logging
import os
from datetime import date, datetime
from hashlib import sha256

import psycopg2

import utility


def getConnection():
    database_url = os.environ.get("DATABASE_URL", "postgres://postgres:mdp@localhost/melodb")
    
    try:
        return psycopg2.connect(host="localhost",database="melodb",user="postgres",password="mdp")
    except:
        return psycopg2.connect(database_url, sslmode='require')


def checkEntryType(errorMessage:int, dictionary:dict) -> list[str]:
    """vérifie que le type de la donné correspond bien au type attendu. Crée un message d'erreur en fonction de l'endroit où la fonctionaété appelé.

        dictionary est un dictionnaire contenant les attributs et les valeurs à vérifier sous la forme {"marque" : "shimano"}

        errorMesssage est en fonction de la fonction d'origine:
        1 : addBike
        2 : modifyBike, readBike
        """
    dictExpectedType = {"id":int, "benevole" : str, "title" : str, "bycode":str, "dateEntre":str, "marque":str, "typeVelo":str, "tailleRoue":str, "tailleCadre":str, "photo1":bytes, "photo2":bytes, "photo3":bytes, "electrique":bool, "origine":str, "statusVelo":str, "etatVelo":str, "prochaineAction":str, "referent":str, "valeur":float, "destinataireVelo":str, "descriptionPublic":str, "descriptionPrive":str, "dateSortie":str, "typeSortie":str}
    listError = []

    for key, value in dictionary.items(): # on parcour le dictionnaire
        if type(value) != dictExpectedType[key] and value != None: # si la valeur n'est pas celle attendu et n'est pas None (valeur non renseigné)
            if key == "valeur" and type(value) == int:  # js = caca pas capable de faire un float correctement
                pass
            elif errorMessage == 1: # erreur venant de addBike
                # éxemple:        bycode est "input" (un     str      ) alors qu'il devrait être un         int 
                listError.append(f"{key} est  (un {type(value)}) alors qu'il devrait être un {dictExpectedType[key]}")
            elif errorMessage == 2: # erreur venant de modifyBike ou readBike
                listError.append(f"{key} est du mauvais type : {type(value)} au lieu de {dictExpectedType[key]}. valeur entré : {value}")
            
    return listError


def checkIsItAColumn(potentialColumn:str) -> bool:
    """vérifie que potentialColumn est bien une des colonnes de la table de la base de donné"""
    listAttributesName = ["bycode", "benevole", "dateEntre", "marque", "typeVelo", "tailleRoue", "tailleCadre", "photo1", "photo2", "photo3", "electrique", "origine", "statusVelo", "etatVelo", "prochaineAction", "referent", "valeur", "destinataireVelo", "descriptionPublic", "descriptionPrive", "dateSortie", "typeSortie"]
    if potentialColumn in listAttributesName:
        return True
    return False


def addBike(dictOfValue):
    """crée un vélo dans la base de donné Bike et une ligne de mémoire dans la table Modification
    
        userName est le nom de l'utilisateur qui crée le vélo. Il est utilisé pour créer l'entré du vélo dans la table Modification

        dictOfValue est un dictionnaire contenant les attributs et les valeurs du vélo sous la forme {"marque" : "shimano"}
    """
    # vérifie que les entrés soient du bon type
    typeCheck = checkEntryType(1, dictOfValue)
    if typeCheck: # si il y a des erreurs on arrête le programme et renvoie l'erreur sous forme d'un liste de string
        return typeCheck
    
    # on vérifie que les attributs nécessaires soient remplis sinon on n'ajoute pas le vélo.
    listAttributesRequired = ["dateEntre", "origine", "statusVelo", "benevole", "title"]
    for attribute in listAttributesRequired:
        if attribute not in dictOfValue:
            return "%s est nécessaire veuillez le renseigner"
        
    # On remplit les attributs non nécessaires n'ayant pas de valeur par None
    listAttributesName = ["bycode", "referent", "marque", "typeVelo", "tailleRoue", "tailleCadre", "electrique", "etatVelo", "prochaineAction", "valeur", "destinataireVelo", "descriptionPublic", "descriptionPrive", "dateSortie", "typeSortie", "photo1", "photo2", "photo3"]
    for attribute in listAttributesName:
        if attribute not in dictOfValue:
            dictOfValue[attribute] = None

    # Connexion à la base de données
    connection = getConnection()
    cursor = connection.cursor() # création du curseur

    # ajout du vélo dans la base de donné Bike
    query = (f"INSERT INTO Bike (bycode, dateEntre, title, marque, typeVelo, tailleRoue, tailleCadre, electrique, origine, statusVelo, etatVelo, prochaineAction, referent, valeur, destinataireVelo, descriptionPublic, descriptionPrive, dateSortie, typeSortie, photo1, photo2, photo3) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id")
    values =(
        dictOfValue['bycode'],
        dictOfValue['dateEntre'],
        dictOfValue['title'],
        dictOfValue['marque'],
        dictOfValue['typeVelo'],
        dictOfValue['tailleRoue'],
        dictOfValue['tailleCadre'],
        dictOfValue['electrique'],
        dictOfValue['origine'],
        dictOfValue['statusVelo'],
        dictOfValue['etatVelo'],
        dictOfValue['prochaineAction'],
        dictOfValue['referent'],
        dictOfValue['valeur'],
        dictOfValue['destinataireVelo'],
        dictOfValue['descriptionPublic'],
        dictOfValue['descriptionPrive'],
        dictOfValue['dateSortie'],
        dictOfValue['typeSortie'],
        psycopg2.Binary(dictOfValue["photo1"]),
        psycopg2.Binary(dictOfValue["photo2"]),
        psycopg2.Binary(dictOfValue["photo3"])
    )
    logging.info(query)
    logging.info(values)
    cursor.execute(query, values)
    bike_id = cursor.fetchone()[0] #on récupère l'id du vélo qui a été crée pour l'enregistrer dans la table modification (on la récupère car à la fin de la query il y a RETURNING id)

    suiviModifData ={
        "dateOfModification" : date.today().isoformat(),
        "timestamp" : datetime.now().isoformat(),
        "benevole" : dictOfValue["benevole"],
        "fieldModified" : "création",
        "oldValue" : None,
        "newValue" : None
    }
    jsonObject = json.dumps(suiviModifData)
    query = f"INSERT INTO Modification (BikeID, suiviModifJSON) VALUES (%s, array[%s::jsonb])"
    values =(bike_id, jsonObject)

    # ajout du vélo dans la table Modification
    cursor.execute(query, values) # envoie de la requette à la base de donné

    connection.commit() # éxécution des requette
    connection.close()

    return {"status": "OK"}


def modifyBike(dictOfChange):
    """Modifie un ou plusieurs attribut d'un vélo et enregistre le/les changements dans la table Modification
    
        userName est le nom de l'utilisateur qui crée le vélo. Il est utilisé pour créer l'entré du vélo dans la table Modification

        dictOfChange est un dictionnaire contenant les attributs et les valeurs à modifier sous la forme {"marque" : "shimano"}
    """

    # vérifie que les entrés soient du bon type
    typeCheck = checkEntryType(2, dictOfChange)
    if typeCheck: # si il y a des erreurs stop et renvoie de l'erreur sous forme d'un liste de string
        return typeCheck
    
    
    # Connexion à la base de données
    connection = getConnection()

    cursor = connection.cursor() # création du curseur
    for key, value in dictOfChange.items():
        if checkIsItAColumn(key) and key != "benevole": # on vérifie que la clef est bien une colonne de la table de la base de donné
            # on récupère d'abord l'ancienne valeur de l'attribut pour l'enregistrer dans la table de Modification
            cursor.execute("SELECT {} FROM Bike WHERE id = %s".format(key), (dictOfChange["id"],))
            result = cursor.fetchone() # on récupère la valeur qui nous intéresse
            oldValue = result[0] 

            if key == "tailleRoue":
                print("\n\nHERE")
                print("modification value = ", value)
                print("/HERE\n\n")

            cursor.execute("UPDATE Bike SET {} = %s WHERE id = %s".format(key), (value, dictOfChange["id"])) # format car on ne peut pas passer le nom d'une colonne avec "?"

            # ajout de la modificatoin dans la table Modification
            cursor.execute("SELECT suiviModifJSON FROM Modification WHERE bikeID = %s", (dictOfChange["id"],)) # sélectionne le suivid de modif du vélo correspondant
            
            # récupère le suivi de modif
            result = cursor.fetchone() 
            currentSuiviModif = result[0]

            if "photo" in key:
                if oldValue:
                    suiviModifData ={
                        "dateOfModification" : date.today().isoformat(),
                        "benevole" : dictOfChange["benevole"],
                        "fieldModified" : key,
                        "oldValue" : True,
                        "nexValue" : True
                    }
                else:
                    suiviModifData ={
                        "dateOfModification" : date.today().isoformat(),
                        "benevole" : dictOfChange["benevole"],
                        "fieldModified" : key,
                        "oldValue" : False,
                        "nexValue" : True
                    }
            else:
                suiviModifData ={
                    "dateOfModification" : date.today().isoformat(),
                    "timestamp" : datetime.now().isoformat(),
                    "benevole" : dictOfChange["benevole"],
                    "fieldModified" : key,
                    "oldValue" : oldValue,
                    "newValue" : value
                }

            newSuiviModif = json.dumps(suiviModifData)
            query = f"UPDATE Modification SET suiviModifJSON = array_append(suiviModifJSON, %s::jsonb) WHERE bikeID = %s"
            values = (newSuiviModif, dictOfChange["id"])

            
            cursor.execute(query, values) # remplace le suivi de modif par celui update
            connection.commit() # effectue les mise à jour

    connection.close()# récupère le suivi de modif

    return {"status": "OK"}


def readBike(whoCall : str, dictOfFilters : dict = None) -> list[dict]:
    """ Whocall : "search", "global", "detail", "edit"
        dictOfFilters : {"attibut1" : "valeur1", "attribut2" : "valeur2" ....} (notamment bikeId)
    
        SELECT 1 FROM Bike WHERE 2
        whoCall gère le 1 et prend soit la valeur:
            "search" page recherche vélo
            "global" page vélo caractères globaux
            "detail" page vélo info caché pour les utilisateurs readOnly
            "edit"   page modification d'un vélo

        dicOfFilters gère le 2, cad {"marque = "shimano"} pour la gestion des filtre sur la page de recherche de vélo
            ou bien {"id" : bikeId} pour la page de détail

        search : photo1, title, id
        global : marque, type, taille de roue, taille du cadre, photo1, photo2, photo3, statusVelo, état, valeur, descriptionPublic, id
        detail : bycode, origine, prochaine action, référent, destinataire, descriptionPrive
        edit   : tous les ellements
    """

    # on sélectionne les attrtibuts à renvoyer en fonction de l'endroit où à lieux l'appel
    if whoCall == "search":
        caracteristicToReturn = "photo1, title, id"
    elif whoCall == "global":
        caracteristicToReturn = "marque, typeVelo, tailleRoue, tailleCadre, photo1, photo2, photo3, statusVelo, etatVelo, electrique, descriptionPublic"
    elif whoCall == "detail":
        caracteristicToReturn = "bycode, origine, prochaineAction, referent, valeur, destinataireVelo, descriptionPrive, id"
    elif whoCall == "edit":
        caracteristicToReturn = "*"
    elif whoCall == "title":
        caracteristicToReturn = "title"
    else:
        print("Error in whoCall")
        return "Error in whoCall" # !! gestion d'erreur non implémenté !!

    
    # vérifie que les entrés soient du bon type
    if dictOfFilters != None: # si il y a un/des filtres OU que l'on sélectionne un seul vélo
        typeCheck = checkEntryType(2, dictOfFilters)
        if typeCheck: # si il y a des erreurs stop et renvoie de l'erreur sous forme d'un liste de string
            print("sqlCRUD error in typeCheck : %s"%(dictOfFilters))
            return typeCheck
    
    
    # préparationd de la requette SQL
    sqlQuerry = "SELECT %s FROM Bike "%(caracteristicToReturn)


    if dictOfFilters: # si il y a au moins un filtre, sinon la requêtte est prete
        sqlQuerry += 'WHERE ' # requette de base
        conditions = []
        for key, value in dictOfFilters.items():
            conditions.append(f"{key} = '{value}'") # marque = "shimano"

        # Ajout des conditions à la requête si des filtres sont présents
        if conditions:
            sqlQuerry += " AND ".join(conditions) #transforme la liste crée au dessus en requette SQL 
    

    # Connexion à la base de données
    connection = getConnection()

    cursor = connection.cursor()
    cursor.execute(sqlQuerry) # éxécute la requette
    result = cursor.fetchall()
    print("sqlCRUD ligne 271 : ", result)
    connection.close()
    rows = []

    for row in result:
        columns = [desc[0] for desc in cursor.description]

        if whoCall == "global" or whoCall == "detail":
            for i in range(len(columns)):
                columns[i] = utility.addSpaceBetweenWord(columns[i]) # on ajoute des espaces pour l'affichage sur la page web
        elif whoCall == "edit":
            for i in range(len(columns)):
                columns[i] = utility.toCamelCase(columns[i]) # on le transforme en camelCase car la base de donné est caseLess et que le code est camelCase

        row_dict = dict(zip(columns, row)) # on met les colonne dans l'ordre pour avoir le bon ordre d'affichage
        rows.append(row_dict)


    if whoCall == "edit":
        print("SQLCRUD ligne 290 : ",row_dict["tailleRoue"])

    return rows


def getBikeOut(dictOfValues):
    """"""
    columnsLabel = "bycode, dateEntre, marque, typeVelo, tailleRoue, tailleCadre, electrique, origine, statusVelo, etatVelo, referent, valeur, destinataireVelo, descriptionPublic, descriptionPrive, dateSortie, typeSortie"
    returnValues = [("bycode", "dateEntre", "marque", "typeVelo", "tailleRoue", "tailleCadre", "electrique", "origine", "statusVelo", "etatVelo", "referent", "valeur", "destinataireVelo", "descriptionPublic", "descriptionPrive", "dateSortie", "typeSortie",)]

    query = "SELECT %s FROM bike WHERE 1=1"%(columnsLabel)
    values = []
    conditions = []


    if dictOfValues["inStartDate"]:
        conditions.append("dateentre >= %s")
        values.append(dictOfValues["inStartDate"])
    if dictOfValues["inEndDate"]:
        conditions.append("dateentre <= %s")
        values.append(dictOfValues["inEndDate"])
    if dictOfValues["outStartDate"]:
        conditions.append("datesortie >= %s")
        values.append(dictOfValues["outStartDate"])
    if dictOfValues["outEndDate"]:
        conditions.append("datesortie <= %s")
        values.append(dictOfValues["outEndDate"])

    # Ajout des conditions à la requête si des paramètres ont été renseignés
    if conditions:
        query += " AND " + " AND ".join(conditions)

    if dictOfValues["bikeStatus"]:
        status_clause = " OR ".join(["statusVelo = %s" for _ in dictOfValues["bikeStatus"]])
        values.extend(dictOfValues["bikeStatus"])
        query += " AND (" + status_clause + ")"

    connection = getConnection()

    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    results = cursor.fetchall()
    connection.close()

    for i in results:
        returnValues.append(i)
    
    returnValues = tuple(returnValues)

    return returnValues

   
def getFilterValues() -> dict[list]:
    """" Retoure toutes les valeurs des attributs filtrables. Permet de rendre dynamique les options de filtres
        listAttributes = ["marque", "typeVelo", "tailleRoue", "tailleCadre", "etatVelo"]
    """
    listAttributes = ["marque", "typeVelo", "tailleRoue", "tailleCadre", "electrique", "etatVelo", "statusVelo", "origine", "prochaineAction", "referent", "destinataireVelo", "id"]
    dictReturn = {"marque" : [], "typeVelo" : [], "tailleRoue" : [], "tailleCadre" : [], "electrique" : [], "etatVelo" : [], "statusVelo" : [], "origine" : [], "prochaineAction" : [], "referent" : [], "destinataireVelo" : [], "id" : []}
    dictSort = {"typeVelo" : ["VTT", "Vélo de route", "VTC", "BMX", "cargo", "pliant"], "tailleCadre" : ["enfant", "XS", "S", "M", "L", "XL", "XXL"], "etatVelo" : ["très bon", "moyen", "mauvais", "pour pièces"], "statusVelo" : ["en stock", "réservé", "vendu", "donné", "recyclé", "perdu"], "origine" : ["don", "trouvé", "achat", "récup", "déchetterie"], "prochaineAction" : ["à vendre", "à donner", "à démonter", "à recycler", "à réparer"]}
    

    # Connexion à la base de données
    connection = getConnection()

    cursor = connection.cursor()
    for attribut in listAttributes: # parcourt les attributs
        cursor.execute( "SELECT %s From bike" %(attribut)) # création de la requette qui sélectionne toutes les valeur un attribut après l'autre
        result = cursor.fetchall()
        for valueTupple in result: # on parcourt le résultat qui est une liste de tupple
            if valueTupple[0] not in dictReturn[attribut] and valueTupple[0] != None and valueTupple[0] != "": # on vérifie que c'est la première occurence 
                dictReturn[attribut].append(valueTupple[0]) # si oui on l'enregistre
        if attribut in dictSort:
            indexOfelement = lambda x: dictSort[attribut].index(x)
            dictReturn[attribut].sort(key = indexOfelement)

    connection.close()

    return dictReturn


def checkUser(userName, password):
    """ Vérifie si la combianaison username/password corrépsond à celle dans la base de donné.
        userName et password viennent de la page de logIn   """
    hashingMachine = sha256(password.encode("utf8")).hexdigest() # hashage du mot de passe car il n'est pas conservé en clair
    userName = userName.lower() # on enlève les majuscules

        # connection à la data base
    connection = getConnection()

         # on récupère le hash du mot de passse enregistré
    cursor = connection.cursor()
    query = "SELECT password FROM member WHERE username = '%s';"%(userName)
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        result = result[0] # résulte[0] est le hash du mot de passe


    if result == hashingMachine: # si les hash correspondent
        query = "SELECT role FROM member WHERE username = '%s';"%(userName) # on récupère le role de l'utillisateur
        cursor.execute(query)
        result = cursor.fetchone()[0]
        connection.close()

        return {"status" : True, "role" : result} # on retourne la réussite + le role
    
    else:
        return {"status" : False, "role" : None}  # on retourne l'échec


### !! old pas encore imlplémenté !!
def deleteBike(userName:str, bikeID:int) -> None:
    # message d'avertissement
    print("Attention tu vas supprimer un vélo de la base de donné, es tu sur? y/n")
    if input() != 'y':
        print("\nsupression annulé")
        return
    
    print("Veux tu ajouter un commentaire? Vide pour non")
    commentaire = input()

    # Connexion à la base de données
    connection = getConnection()
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

### /!!

###!! uniquement pour intéragir avec le terminal, pas encore implémenté !!
def readModification(bikeID):
    # préparationd e la requette SQL
    sqlQuerry = f"SELECT suiviModifJSON FROM modification WHERE bikeID = {bikeID}"

    # Connexion à la base de données
    connection = getConnection()

    cursor = connection.cursor()
    cursor.execute(sqlQuerry) # éxécute la requette
    result = cursor.fetchone()

    connection.close()

    return(result)
### /!!
