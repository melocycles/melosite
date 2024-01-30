from flask import Flask, render_template, request, jsonify, session, json, redirect, url_for
import sqlCRUD
import base64
app = Flask(__name__)
app.secret_key = 'test'
app.config['SESSION_COOKIE_SAMESITE'] = None  # 'None' signifie que SameSite=None sera utilisé

# ce qui s'affiche quand on se connecte au serveur (la page où l'on voit tous les vélos)
@app.route('/')
def index():
    return render_template('parcourVelo.html')

# page où un seul vélo s'affiche
@app.route('/velo')
def show_bike_page():
    return render_template('velo.html')

@app.route("/api/readBikeJs", methods=["POST"])
def readBikeJs() -> list[dict] or list[list]:
    """Appel la fonction sclCRUD.readbike
        requiert whoCall (str) et parameter(dict). 
        renvoie une liste de dict si plusieurs vélos sont retournés (1dict = 1vélo)
        renvoie une liste de liste si 1 seul vélo est retourné sous la forme [[attr1, value1], [attr2, value2], ...]
    """
    # on récupère les info depuis le js
    data = request.get_json()

    if 'whoCall' in data and 'parameters' in data: # check que la requette du js contient bien tout ce qu'il faut
        whoCall = data['whoCall']           # assignation des variable
        dicOfFilters = data['parameters']   # idem
                          
    # on récupère les information sur le vélo
    result = sqlCRUD.readBike(whoCall, dicOfFilters)

    # on transforme les byte en str car js c'est de la merde
    for bikeIndex in range(len(result)): # parcourt tous les vélos
        for i in ["photo1", "photo2", "photo3"]: # on parcourt les photos possibles
            if i in result[bikeIndex]: # si une photo est présente
                result[bikeIndex][i] = base64.b64encode(result[bikeIndex][i]).decode('utf-8') # transforme en format jsCompatible

    if whoCall != "search": # un seul vélo a été renvoyé
        result = result[0] # on récupère le seul vélo de la liste

        # on transforme le dictionnaire en une liste avec en entré paire les clef et en impaire les valeures. (pourquoi? parceque le js c'est vraiment de la merde)11
        # et que sinon l'ordre d'affichage n'est pas conservé
        result = [[key, value] for key, value in result.items()]
    # on envoie cette liste au javasctipt

    return jsonify({'result': result})

# renvoie les valeurs possible de filtre (aka toutes les marques enregistrés, tous les types de vélo....)
@app.route('/api/getFilterValue', methods=["POST"])
def getFilterValue():
    result = sqlCRUD.getAttributesValues()
    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
