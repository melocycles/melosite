from flask import Flask, render_template, request, jsonify
import sqlCRUD
import base64
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('velo.html')

# Route pour la manipulation des données depuis le frontend
@app.route('/api/interaction', methods=['POST'])

def interaction():
    # on récupère les info depuis le js
    data = request.get_json()

    if 'whoCall' in data and 'parameters' in data: # check que la requette du js contient bien tout ce qu'il faut
        whoCall = data['whoCall']           # assignation des variable
        dicOfFilters = data['parameters']   # idem
                          
    # on récupère les information sur le vélo
    result = sqlCRUD.readBike(whoCall, dicOfFilters)

    # on transforme les byte en str car js c'est de la merde
    for i in ["photo1", "photo2", "photo3"]:
        if i in result:
            result[i] = base64.b64encode(result[i]).decode('utf-8')

    # on transforme le dictionnaire en une liste avec en entré paire les clef et en impaire les valeures. (pourquoi? parceque le js c'est vraiment de la merde)
    orderedResult = [[key, value] for key, value in result.items()]

    # on envoie cette liste au javasctipt
    return jsonify({'result': orderedResult})
    
if __name__ == '__main__':
    app.run(debug=True)
