document.addEventListener('DOMContentLoaded', function () {
    
    const returnButton = document.getElementById('returnButton');
    const submitButton = document.getElementById("confirm");

    formContainer.addEventListener('submit', function (event) {
        event.preventDefault(); // empeche que clicker sur un bouton du formulaire redirige vers une page
    });
    returnButton.addEventListener('click', function() { // au click sur le bouton retour
        window.location.href = "/velo";; // retourne à la page parcourVelo
    });

    submitButton.addEventListener('click', function () {
        const requiredFields = ["dateEntre", "origine", "referent", "status"];
        const missingFields = requiredFields.filter(field => !document.getElementById(field).value);

        if (missingFields.length == 0) { // si il ne manque pas de donné nécessaire
            updateBike(); // envoie les donnés renseigné à la database
        } 

    });


    var bikeId = parseInt(sessionStorage.getItem("bikeId"));
    fetchData('/api/readBikeJs', 'edit', { id: bikeId }, fillForm);

});


// Fonction requette AJAX vers falsk
function fetchData(url, whoCall, parameters, callback) {
    fetch(url, {    // url = api/nomDeLaFonctionDansFlask
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', // indique qu'on va récupérer du json
        },
        body: JSON.stringify({
            whoCall: whoCall,       // paramètres attendu par la fonction flask
            parameters: parameters, // idem
        }),
    })
    .then(response => response.json())  // transforme la réponse en ellement json
    .then(data => {
        if (data && data.result) { // si il y a bien des donnés qui ont été renvoyés
            callback(data.result); // appel de la fonction prévu (aka générer les <li>)
        }
    })
    .catch(error => {
        console.error('Erreur lors de la récupération des données:', error);
    });
}

function fillForm(formData) {
    //console.log(formData)
    formData.forEach(function(attribute) {
        var element = document.getElementById(attribute[0]);
        if (element) {
            if (element.type === 'checkbox') {
                element.checked = attribute[1];
                console.log("checkbox²")
            } else if (element.type === 'date') {
                // Formater la date au format YYYY-MM-DD
                var formattedDate = new Date(attribute[1]).toISOString().split('T')[0];
                element.value = formattedDate;
            } else {
                element.value = attribute[1];
            }
        }
        
    })
}

function updateBike(){
    var formData = {"id" : parseInt(sessionStorage.getItem("bikeId"))};
    const listeAttributes = ["referent", "dateEntre", "status", "origine", "etatVelo", "marque", "typeVelo", "tailleRoue", "tailleCadre", "bycode", "electrique", "prochaineAction", "valeur", "destinataireVelo", "descriptionPublic", "descriptionPrive"]
    
    // crée le dictionnaire à envoyer à sqlCRUD.py
    for (const attribute of listeAttributes) { // parcourt tous les ellements qui peuvent être rensignés
        if (document.getElementById(attribute).value !== "") { // si il y a une valeur
            
            if(attribute == "electrique"){ // si l'attribut est ellectrique on le transforme en boolean
                if(document.getElementById(attribute).value == "true"){
                    formData[attribute] = true
                }else{
                    formData[attribute] = false
                }
            } else if(attribute == "valeur"){ // si l'attribut est valeur on le transforme en float
                formData[attribute] = parseFloat(document.getElementById(attribute).value)

            } else{ // sinon on l'ajoute jsute (string)
                formData[attribute] = document.getElementById(attribute).value; // on assigne à l'attribut sa valeur 
            }
        }
    }

    // Envoie des données au backend Flask en utilisant fetch
    fetch('/api/modifyBikeJs', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=UTF-8',
        },
        body: JSON.stringify(formData),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('erreur scriptModifierVelo : erreur réseau');
        }
        return response.json();
    })
    .then(data => {
        window.location.href = "/velo"; // si tout c'est bien passé redirection vers la page du vélo
    })
    .catch(error => {
        console.error('erreur scriptModifierVelo l\'envoi des données: ', error);
    });

}