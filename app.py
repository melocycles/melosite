from flask import Flask, abort, jsonify, redirect, render_template, request, url_for
import base64
import os
import json

import info  # contient les infos secètes qu'on ne veux pas exposer sur github
import sqlCRUD

app = Flask(__name__)
app.secret_key = info.APP_SECRET

app.config['SESSION_COOKIE_SAMESITE'] = None  # 'None' signifie que SameSite=None sera utilisé


    ### routes pour l'affichage des pages

# vérifie si l'utilisateur est connecté
def checkCookieUser():
    try:
        cookieUuid = request.cookies.get('uuid') # on essaye de récupérer le cookie
    except:
        cookieUuid = None   # si il n'éxiste pas le cookie est assigné à None

    if cookieUuid == info.USER_UUID: # on compare les uuid
        return True # identique on renvoié true
      
    return False # différent on renvoi false

# vérifie la connexion au compte admin (cf ci dessus)
def checkCookieAdmin():
    try:
        cookieUuid = request.cookies.get('uuid')
    except:
        cookieUuid = None

    if cookieUuid == info.ADMIN_UUID:
        return True
    
    return False

# redirige depuis la site racine vers parcourVélo
@app.route('/')
def redirectToHomePage():
    if checkCookieAdmin():
        return render_template("admin.html")
    elif checkCookieUser:
        return redirect('/parcourVelo')
    else:
        return redirect("/log")


#page avec tous les vélos
@app.route('/parcourVelo') 
def showAllBikes():
    if checkCookieUser() or checkCookieAdmin():
        return render_template('parcourVelo.html')      
    else:
        return redirect("/log")


# page d'un vélo avec ces détails
@app.route('/velo')
def showSingleBike():
    if checkCookieUser():
        return render_template('velo.html')
    elif checkCookieAdmin():
        return render_template('adminVelo.html')
    else:
        return redirect("/log")


# page ajouter un vélo
@app.route('/ajouterVelo')
def addBikePage():
    if checkCookieUser() or checkCookieAdmin():
        return render_template("ajouterVelo.html", dict_form = info.dict_form)
    else:
        abort(418)
        

# page modifier un vélo
@app.route('/modifierVelo')
def modifyBike():
    if checkCookieUser():
        return render_template("modifierVelo.html")
    else:
        abort(418)

# page de login/logut
@app.route("/log")
def log():
    if checkCookieUser() or checkCookieAdmin():
        return render_template("logOut.html")
    else:
        return render_template("logIn.html")

# page d'export vers csv
@app.route("/export")
def export():
    if checkCookieAdmin():
        return render_template("/export.html")
    else:
        abort(418)

# page suiviModif d'un vélo
@app.route("/suiviModif")
def suiviModif():
    if checkCookieAdmin():
        return render_template("/adminVelo.html")
    else:
        abort(418)

@app.route('/alterTable')
def alterTable():
    if checkCookieAdmin():
        return render_template("/alterTable.html")
    else:
        abort(418)


    ### les interractions du site web avec la database

# route pour récupérer les informations sur le/les vélos
@app.route("/api/readBike", methods=["POST"])
def APIreadBike() -> list[dict] | list[list]:
    """Appel la fonction sclCRUD.readbike

        requiert whoCall (str) et parameter(dict). 
        Whocall : "search", "global", "detail", "edit"
        dictOfFilters : {"attibut1" : "valeur1", "attribut2" : "valeur2" ....} (notamment bikeId)

        renvoie une liste de dict si plusieurs vélos sont retournés (1dict = 1vélo)
        renvoie une liste de liste si 1 seul vélo est retourné sous la forme [[attr1, value1], [attr2, value2], ...]

        voir sqlCRUD.readBike pour plus de détail
    """
    data = request.get_json() # récupération des donnés

    # vérification de la présence + récupération de whoCall et parameters
    if 'whoCall' in data and 'parameters' in data:
        whoCall = data['whoCall']
        dicOfFilters = data['parameters']

    # envoie à slCRUD.readbike, on récupère une list[dict] (voir sqlCRUD.readbike pour plus de détail)
    result = sqlCRUD.readBike(whoCall, dicOfFilters)

    # on transforme les photo stické en byte en str car js c'est de la merde
    for bikeIndex in range(len(result)): 
        for i in ["photo1", "photo2", "photo3"]: # on parcourt les photos possibles
            if i in result[bikeIndex] and result[bikeIndex][i] != None: # si une photo est présente
                result[bikeIndex][i] = base64.b64encode(result[bikeIndex][i]).decode('utf-8') # transforme en format jsCompatible

    if whoCall != "search": # il y a un seul vélo dans result
        result = result[0] # on récupère le seul vélo de la liste

        # on transforme le dictionnaire en une liste avec en entré paire les clef et en impaire les valeures. (pourquoi? parceque le js c'est vraiment de la merde)11
        # et que sinon l'ordre d'affichage des attributs n'est pas conservé
        result = [[key, value] for key, value in result.items()]
    else:
        # si il y a plusieurs vélo result est déjà dans le bon format de list[dict] on peut le renvoyer direct
        pass


    return  ({'result': result})




# route pour récupérer les valeurs éxistantes de filtre (aka toutes les marques enregistrés, tous les types de vélo....)
@app.route('/api/getFilterValue', methods=["POST"])
def APIgetFilterValue() -> dict[list]: 
    result = sqlCRUD.getFilterValues()
    return jsonify({'result': result})


# route pour l'ajout d'un vélo
@app.route("/api/addBike", methods=["POST"])
def APIaddbike():
    """Appel la fonctione sqlCRUD.addbike
        requiert dictOfValue qui contient les attributs renseignés par l'utilisateur
        retourne un dictionnaire confirmant le succès de l'opération
        """
    data = request.get_json() # récupération des donnés

    for attribute in data:
        if attribute.startswith("photo"): # on cherche si il y a des photos pour les envoyer dans removeEncoderHeader()
            data[attribute] = base64.b64decode(data[attribute].split(',')[1])
    
    app.logger.info(data)
    
    result = sqlCRUD.addBike(data)
    return result # renvoie une réponse de succès sous forme {"status" : "ok"}


# route pour la modification d'un vélo
@app.route("/api/modifyBike", methods=["POST"])
def APImodifyBike():
    """Appel la fonction sqlCRUD.modifyBike
        requiert dictOdChange (dict) contenant les parmaètres à modifier
    """
    data = request.json # récupération des donnés
    for attribute in data:
        
        if attribute.startswith("photo"): # on cherche si il y a des photos pour les envoyer dans removeEncoderHeader()
            data[attribute] = base64.b64decode(data[attribute].split(',')[1])
    response = sqlCRUD.modifyBike(data)
    print("modify in app response : ",response)
    return response # renvoie une réponse de succès sous forme {"status" : "ok"}


# route pour vérifier lesl log renseigné par l'utilisatuer
@app.route("/api/logIn", methods=["POST"])
def login():
    data = request.json
    if "userName" in data and "password" in data: 
        result = sqlCRUD.checkUser(data["userName"], data["password"])
        
        

        if result["status"]:
            if result["role"] == "user":
                return jsonify({"result" : info.USER_UUID})
            elif result["role"] == "admin":
                return jsonify({"result" : info.ADMIN_UUID})
            else:
                return jsonify({"result" : "erreur dans app.login le role est inconnu"})
        else:
            return jsonify({"result" : "mauvaise combinaison username/mot de passe"})




    ### zone de test, à enlever avant la mise en ligne

# route pour lire la table de modification
@app.route("/api/readModification", methods=["POST"])
def APIreadModification():
    data = request.json # récupération des donnés
    bikeId = data["bikeId"]
    result = sqlCRUD.readModification(bikeId)
    return({'result': result})



# route pour tester la présence d'une ouo plusieurs donnés
@app.route("/api/fetchTest", methods=["POST"])
def APIfetchTest():
    print("\nTEST START\n")
    data = request.json # récupération des donnés

    if "name" in data and "data" in data:
        print("test de : %s"%(data["name"]))
        print("type : %s\n"%(type(data["data"])))
        print("data :\n%s"%(data["data"]))
    else:
        print("FETCHTEST : %s"%(data))
    print("\nTEST END\n")

    return {"status": "OK"}


@app.route("/api/getBikeOut", methods=["POST"])
def getBikeOut():
    data = request.json
    response = sqlCRUD.getBikeOut(data)
    return {"status" : "ok", "csv" : response}

@app.route('/api/config', methods=["POST"])
def get_config():
    config_data = info.JSONCONFIG
    return jsonify(config_data)

@app.route('/api/editConfigFile', methods=["POST"])
def editConfigFile():
    configData = request.json

    if type(configData) == dict: # ajouter une colonne
        num = 0
        for i in info.JSONCONFIG:
            if info.JSONCONFIG[i]["order"] > num:
                num = info.JSONCONFIG[i]["order"]
        configData["order"] = num+1

        jsonToRec = info.JSONCONFIG
        jsonToRec[configData["camelCase"]] = configData
        os.environ['herokuJson'] = json.dumps(jsonToRec)
        print(json.dumps(jsonToRec))

        sqlCRUD.addColumn(configData["camelCase"],configData["entryType"], configData["addRequired"])
        
    else:
        aFaire = "editer multiChoice"
    
    return {"status" : "ok"}


if __name__ == '__main__':
    context = ('server.crt', 'server.key')
    #app.run(debug=True, host='0.0.0.0') # version http
    app.run(ssl_context=context, debug=True, host='0.0.0.0') # version https