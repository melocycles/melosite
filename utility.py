###
### ce fichier sert à stocker les petits utilitaires qui ont une et une seule fonction simple explicité dans le nom
###
import info
jsonConfig = info.JSONCONFIG

def toCamelCase(word):
    """ transforme attributs en plusieur mot en camelCase pour matcher avec le reste du code"""
    for i in jsonConfig:
        if jsonConfig[i]["lowCase"] == word:
            return jsonConfig[i]["camelCase"]


def addSpaceBetweenWord(word):
    for i in jsonConfig:
        if jsonConfig[i]["lowCase"] == word:
            return jsonConfig[i]["withSpace"]
        

def booltoFrench(value):
    # transforme boolean en français pour l'affichage
    if value == True or value == "True" or value == "true":
        return "oui"
    elif value == False or value == "False" or value == "false":
        return "non"
    else:
        return value

def frenchToBool(value):
    # transforme oui/non en bool pour l'enregistrement dans la db
    if value == "oui" or value == "True" or value == "true":
        return True
    elif value == "non" or value == "False" or value == "false":
        return False
    else:
        return value

def numToMonth(value):
    monthDict = {1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin", 7: "Juillet", 8: "Août", 9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"}
    return monthDict[value]