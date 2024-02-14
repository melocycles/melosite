###
### ce fichier sert à stocker les petits utilitaires qui ont une et une seule fonction simple explicité dans le nom
###

def toCamelCase(word):
    """ transforme attributs en plusieur mot en camelCase pour matcher avec le reste du code"""
    dictOfWordToCamelCase = {"dateentre" : "dateEntre", "etatvelo" : "etatVelo", "typevelo" : "typeVelo", "tailleroue" : "tailleRoue", "taillecadre" : "tailleCadre", "prochaineaction" : "prochaineAction", "destinatairevelo" : "destinataireVelo", "descriptionpublic" : "descriptionPublic", "descriptionprive" : "descriptionPrive", "statusvelo" : "statusVelo"}
    if word in dictOfWordToCamelCase:
        return dictOfWordToCamelCase[word]
    return word


def addSpaceBetweenWord(word):
    dictOfWordToSpace = {"dateentre" : "date entré", "etatvelo" : "etat vélo", "typevelo" : "type vélo", "tailleroue" : "taille roue", "taillecadre" : "taille cadre", "prochaineaction" : "prochaine action", "destinatairevelo" : "destinataire vélo", "descriptionpublic" : "description public", "descriptionprive" : "description prive"}

    if word in dictOfWordToSpace:
        return dictOfWordToSpace[word]
    return word

