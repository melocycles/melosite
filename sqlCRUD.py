import sqlite3
from datetime import date

def addUser(name, role):
    """ajoute un utilisateur à la base donné"""
    connection = sqlite3.connect('MyDataBase.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO User (username, role) VALUES (?, ?)",
                (name, role))
    connection.commit()
    connection.close()

def addBike(numeroIdentification, nom, description, marque, status, dateEntre):
    """ajoute un vélo à la base de donné & crée son avatar de modification"""
    connection = sqlite3.connect("MyDataBase.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Bike (numeroIdentification, nom, description, marque, status, dateEntre) VALUES (?,?,?,?,?,?)",
                   (numeroIdentification, nom, description, marque, status, dateEntre))
    connection.commit()

    bike_id = cursor.lastrowid
    cursor.execute("INSERT INTO Modification (date, benevole, information, BikeID) VALUES (?, ?, ?, ?)",
               (date.today(), user["name"] , f"le {date.today()} {user['name']} à crée le vélo", bike_id))
    
    connection.commit()
    connection.close()

def displayBike(filters = None, filtersValue = None):
    """affiche les vélo de la base de donné. filter & filterValues permet de chercher selon un critère spécifique"""
    connection = sqlite3.connect('MyDataBase.db')
    cursor = connection.cursor()

    print(f"SELECT * FROM Bike WHERE {filters} = {filtersValue}")
    if filters == None: # afficher tout
        cursor.execute("SELECT * FROM Bike")
    elif filters == "date":
        cursor.execute("SELECT * FROM Bike WHERE dateEntre BETWEEN ? AND ?", (filtersValue[0], filtersValue[1]))

    else:
        # Générer la partie WHERE de la requête en fonction des filtres fouris
        cursor.execute(f"SELECT * FROM Bike WHERE {filters} = {filtersValue}")#, (filters, filtersValue))

    # Exécuter la requête avec les valeurs des filtres
    results = cursor.fetchall()

    for row in results:
        print(f"ID: {row[0]}, "
        f"Numero d'identification: {row[1]}, "
        f"Nom: {row[2]}, "
        f"Description: {row[3]}, "
        f"Marque: {row[4]}, "
        f"Status: {row[5]}, "
        f"Date d'entrée: {row[6]}, "
        f"Date de sortie: {row[7]}, "
        f"Type de sortie: {row[8]}")

    connection.close()
    print("\n")

def displayModification(bikeID):
    connection = sqlite3.connect('MyDataBase.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT information FROM Modification WHERE BikeID = {bikeID}")
    results = cursor.fetchall()
    print(results[0][0])

def modifyBike(bikeID, label):
    if label: # si label n'est pas None aka ce n'est pas juste pour éditer la table des modifications
        connection = sqlite3.connect('MyDataBase.db')
        cursor = connection.cursor()

        print("\nnouvelle valeur:") # nouvelle valeur pour la table Bike
        newValue = input()
        cursor.execute(f"SELECT {label} FROM Bike WHERE id = {bikeID}")
        oldValue = cursor.fetchone()
        oldValue = oldValue[0] #récupère le texte
        cursor.execute(f"UPDATE Bike SET {label} = '{newValue}' WHERE id = {bikeID}")
        connection.commit()
        
        # ajout de la modificatoin dans la table Modification
        cursor.execute(f"SELECT information FROM Modification WHERE bikeID = {bikeID}") # sélectionne le suivid de modif du vélo
        result = cursor.fetchone() # récupère le suivi de modif
        currentInformation = result[0]
        newInformation = f"{currentInformation}\nle {date.today()} {user['name']} à modifié {label} de {oldValue} à {newValue}" # ajoute la modif aux précédentes
        cursor.execute("UPDATE Modification SET information = ? WHERE bikeID = ?", (newInformation, bikeID)) # remplace le suivi de modif par celui update

        # Valider la mise à jour
        connection.commit()
        connection.close()

        

    else: #l'utilisateur ajoute une modif libre
        connection = sqlite3.connect('MyDataBase.db')
        cursor = connection.cursor()
        cursor.execute(f"SELECT information FROM Modification WHERE bikeID = {bikeID}")
        print("\nque veux tu ajouter dans le suivi de modification?")
        modifToAdd = f"le {date.today()} {user['name3']} a indiqué : " + input()
        result = cursor.fetchone() # récupère le suivi de modif
        currentInformation = result[0]
        newInformation = f"{currentInformation}\n{modifToAdd}"
        cursor.execute("UPDATE Modification SET information = ? WHERE bikeID = ?", (newInformation, bikeID)) # remplace le suivi de modif par celui update
        connection.commit()
        connection.close()


user = {"name" : "Louis", "role" : "admin"}

while True:
    if 0: #vider les bases de donné Bike et Modification
        connection = sqlite3.connect('MyDataBase.db')
        cursor = connection.cursor()

        # Utiliser la requête DELETE pour supprimer tous les vélos
        cursor.execute("DELETE FROM Bike")

        # Valider la suppression
        connection.commit()
        cursor.execute("DELETE FROM Modification")
        connection.commit()
        connection.close()
        break

    print("\nque faire?\n1.ajouter un vélo\n2.modifier un vélo\n3.afficher les vélos\n4.afficher les modifications d'un vélo")
    choice = input()
    if choice == "1": # ajouter vélo
        numeroIdentification = input("numeroIdentification")
        nom = input("nom")
        description = input("description")
        marque = input("marque")
        status = input("status")
        dateEntre = input("date")
        addBike(numeroIdentification, nom, description, marque, status, dateEntre)
        numeroIdentification, nom, description, marque, status, dateEntre = "","","","","",""


    if choice == "2": # modifier un vélo
        #afficher les vélo pour avoir le numéro d'id
        displayBike()
        print("\nquel vélo modifier (ID)")
        choiceID = input()
        
        print("\nmodifier\n1.description\n2.status\n3.seulement entrer réparation")
        dicoActionModify = {"1":"description", "2":"status", "3":None}
        choiceAction = dicoActionModify[input()]
        modifyBike(choiceID,choiceAction)


    if choice == "3": # afficher vélo
        print("\nafficher:\n1.tout\n2.filtrer")
        choiceToutOuFiltrer = input()

        if choiceToutOuFiltrer == "1": # tout afficher
            displayBike()

        elif choiceToutOuFiltrer == "2": # filtrer
            print("\nfiltrer par\n1.status\n2.date d'entré\n3.date de sortie")
            dicoFilter = {"1":"status","2":"dateEntre","3":"dateSortie"}
            choiceFiltre = dicoFilter[input()]

            if choiceFiltre != "status": # par date
                print("\ndate de debute")
                choiceStartDate = input()
                print("\ndate de fin")
                choiceEndDate = input()
                choiceFiltre = "date"
                choiceFiltreValue = [choiceStartDate, choiceEndDate] 

            else: # filtrer par status
                print(f'\nvoir les vélo:\n1.en stock\n2.vendu\n3.donné')
                dicoFilterValue = {"1":"'en stock'", "2":"'vendu'", "3":"'donné'"}
                choiceFiltreValue = dicoFilterValue[input()]
            
            displayBike(choiceFiltre, choiceFiltreValue)

    
    if choice == "4":
        displayBike()
        print("\nquel vélo?")
        choiceID = input()
        displayModification(choiceID)