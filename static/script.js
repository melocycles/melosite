document.addEventListener("DOMContentLoaded", function () { // quand la page se charge
    // Appel à la db pour récupérer les infos du vélos puis les ajouter à l'html
    fetchData('/api/interaction', 'global', { id: 1 }, genererListeCaracteristiques);

    // Appel à la db pour récupérer les infos du vélos puis les ajouter à l'html
    fetchData('/api/interaction', 'detail', { id: 1 }, genererListeDetail);
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

// genere la liste des caractéristiques visible de base + l'affichage des photo. Est appelé après fetchData
function genererListeCaracteristiques(caracteristics) {
    const photoKey = ["photo1", "photo2", "photo3"];
    var listeColonneCaracteristic = document.querySelector('.colonne_gauche_caracreristiques ul'); // repère l'ellement html à modifier
    var listeColonneValues = document.querySelector(".colonne_droite_caracreristiques ul"); // repère l'ellement html à modifier

    caracteristics.forEach(function(pair) { // parcourt tous les ellements retourné par flask. function(pair) permet de les avoir sous la forme clef value
        if (photoKey.includes(pair[0])){
            // Si la clef est "photo1", "photo2" ou "photo3", ajoutez le src correspondant à l'id 
            var imgElement = document.getElementById(pair[0]); // recupère l'ellement html qui a pour id photox (1, 2 ou 3)
            imgElement.src = "data:image/jpeg;base64," + pair[1]; // Utilisez les données binaires en tant que source
            if (pair[0] === photoKey[0]){ // si c'est photo1 on la met aussi dans grandeImage
                   // ajoute l'image principale
                    var imgElement = document.getElementById("grandeImage");
                    imgElement.src = "data:image/jpeg;base64," + pair[1]; 
            }
        } else { // ce n'est pas une photo on l'ajoute dans les listes
            // Créez un élément li pour la colonne de gauche (caractéristiques)
            listeColonneCaracteristic.appendChild(createLi(pair[0]));

            // Créez un élément li pour la colonne de droite (valeurs)
            listeColonneValues.appendChild(createLi(pair[1]));
        }
    });
};

// genere la liste affiché au click du boutton détail
function genererListeDetail(caracteristics) {
    var listeColonneCaracteristic = document.querySelector('.colonne_gauche_detail ul'); // repère l'ellement html à modifier
    var listeColonneValues = document.querySelector(".colonne_droite_detail ul"); // repère l'ellement html à modifier

    caracteristics.forEach(function(pair) {// parcourt tous les ellements retourné par flask. function(pair) permet de les avoir sous la forme clef value
        // Créez un élément li pour la colonne de gauche (caractéristiques)
        listeColonneCaracteristic.appendChild(createLi([pair[0]]));

        // Créez un élément li pour la colonne de droite (valeurs)
        listeColonneValues.appendChild(createLi(pair[1]));
    });
};  

// crée les ellements de listes
function createLi(textContent) {
    var liElement = document.createElement('li'); // crée un ellement <li>
    liElement.textContent = textContent; // y ajoute le texte
    return liElement; // le retourne pour qu'il soit injecté dans l'html
}

// affiche/masque les détails à l'appuie sur le bouton
function afficherDetail() {
    var detailElement = document.getElementById('detail'); // recupère le boutton détail
    var isVisible = (detailElement.style.display === 'flex');

    if (isVisible) {
        // Si les détails sont visibles, faites défiler jusqu'en haut de la page
         window.scrollTo({ top: 0, behavior: 'smooth' }); 

        // Ensuite, ajoutez un délai de 500 millisecondes (ou le délai souhaité) avant de masquer les détails
        setTimeout(function() {
            detailElement.style.display = 'none';
        }, 250);
    } else {
        // Si les détails ne sont pas visibles, faites défiler jusqu'en bas de la page
        detailElement.style.display = 'flex';
        detailElement.scrollIntoView({ behavior: 'smooth', block: 'end', inline: 'nearest' }); // sert à scroll automatiquement mais a prioris les texte ne dépasse pas de l'écran
    }
};


// change l'image affiché dans le conteneur class="grandeImage" grace à la fonction onclick="changeImage() dans l'html
function changeImage(id) {
    var imgElement = document.getElementById("grandeImage"); // recupère l'ellement html grandeImage
    var imageToPut = document.getElementById(id).src;   // récupère la photo stocké dans l'image clické
    imgElement.src = imageToPut; // modifie l'html pour afficher la nouvelle image
};