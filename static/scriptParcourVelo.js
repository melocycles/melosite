document.addEventListener("DOMContentLoaded", function () { // quand la page se charge
    // Get the form container element
    var formContainer = document.getElementById('formContainer');

    // Get the header buttons for triggering the form visibility
    var addButton = document.getElementById('addButton');
    var filterButton = document.getElementById('filterButton');
    var cancelButton = document.getElementById('cancelButton');
    var confirmButton = document.getElementById('confirmButton');
    var resetButton = document.getElementById('resetButton');


    fetchData('/api/readBikeJs', 'search', {}, displayBikes); // on récupère la photo1, la descriptionPublic & l'id puis on les display

    // Affiche les valeurs possible de filtre (aka toutes les marques enregistrés, tous les types de vélo....)
    fetchData("/api/getFilterValue", "", "", addOptionsToSelect);
    

    // cette section gère les bouto filter, cancel, confirmation et reset
    formContainer.addEventListener('submit', function(event) { 
        event.preventDefault(); // empeche que clicker sur un bouton du formulaire redirige vers une page
    });
    // ajoute les évenements reliés aux bouttons
    filterButton.addEventListener('click', function() { // au click sur le bouton filtrer
        toggleForm(); // affiche le formulaire
    });
    cancelButton.addEventListener('click', function() { // au click sur le bouton annuler
        hideForm(); // masque le formulaire
    });
    confirmButton.addEventListener('click', function() { // au click sur le bouton confirmer
        hideForm(); // masque le formulaire
        sendFilter(); // envoi les valeurs de filtre
    });
    resetButton.addEventListener('click', function () { // au click sur le boutton reset
        resetSelectOptions(['marque', 'type', 'taille-roues', 'taille-cadre', 'etat-velo']); // enlève toutes les valeur de filtre
    });

    // ...
});


// affiche/masque le formualaire. En réalité il fait 80% de l'écran donc on l'envoie de nsa taille sur la droite (en dehors de l'écran donc)
// la ligne     overflow-x:hidden;  dans stylesParcourVelo.css enmpèche le scroll à droite. C'est un peu la magie de l'informatique
function toggleForm() {
    formContainer.style.right = (formContainer.style.right === '0' || formContainer.style.right === '') ? '-80%' : '0';
};
function hideForm() {
    formContainer.style.right = '-80%';
};

// remet toutes les valeurs de filtres à pas de filtre
function resetSelectOptions(selectIds) {
    selectIds.forEach(selectId => { // parcourt les filtres
        document.getElementById(selectId).value = 'None'; // assigne la value None à chacun
    });
}


//  Supprime les vélo affiché jusquelà. Envoie un requette à flask pour récupérer les vélos correspondant aux filtres.
// Récupère les vélo correspondants et les envoi immédiatement à displayBike
function sendFilter(){
    function addToFormData(property, elementId) { // vérifie qu'une valeur de filtre a été choisi avant de l'envoyer à flask
        var value = document.getElementById(elementId).value;
        if (value !== "None") {
            formData[property] = value;
        }
    }
    var formData = {};
    addToFormData('marque', 'marque');
    addToFormData('typeVelo', 'type');
    addToFormData('tailleRoue', 'taille-roues');
    addToFormData('tailleCadre', 'taille-cadre');
    addToFormData('etatVelo', 'etat-velo');

    document.getElementById('veloPart').innerHTML = ''; // supprime les vélos affichés
    fetchData('/api/readBikeJs', "search", formData, displayBikes)
    // Utilisez Fetch pour envoyer une requête au serveur

};


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
};

// affiche les vélo avec les data récupéré de la base de sonné
function displayBikes(bikesData) {
    var veloPart = document.querySelector('.veloPart'); // récupère le conteneur global des vélo

    bikesData.forEach(function(bike) { // parcourt tous les vélos
        // crée le conteneur du vélo
        var veloCadre = document.createElement('div'); 
        veloCadre.classList.add('veloCadre');
        
        // ajoute l'image
        var veloImage = document.createElement('img'); 
        veloImage.classList.add('veloImage');
        veloImage.src = "data:image/jpeg;base64," + bike.photo1;

        // ajoute la description public
        var descriptionParagraph = document.createElement('p');
        descriptionParagraph.textContent = bike.descriptionpublic;

        // ajoute les 3 ellements ci-dessus à l'html
        veloCadre.appendChild(veloImage);
        veloCadre.appendChild(descriptionParagraph);
        veloPart.appendChild(veloCadre);
        
        veloCadre.addEventListener('click', function() {
            // Redirect to the page of the selected bike
            goToOneBike(bike.id);
        });})
};



function addOptionsToSelect(result) {
    // recupère les ellemeents html où seront placés nos options
    var marqueSelect = document.getElementById("marque");
    var typeSelect = document.getElementById("type");
    var tailleRouesSelect = document.getElementById("taille-roues");
    var tailleCadreSelect = document.getElementById("taille-cadre");
    var etatVeloSelect = document.getElementById("etat-velo");

    // pour chaque type d'option on ajoute les valeurs possibles
    addOption(result.marque, marqueSelect);
    addOption(result.typeVelo, typeSelect);
    addOption(result.tailleRoue, tailleRouesSelect);
    addOption(result.tailleCadre, tailleCadreSelect);
    addOption(result.etatVelo, etatVeloSelect);

    function addOption(optionsArray, selectElement){
        optionsArray.forEach(function (optionValue) { // parcourt toutes las values éxistantes
        var option = document.createElement("option"); // création d'une option (d'un ellement html)
        option.value = optionValue; // assignation de sa valeur pour le renvoi du formulaire
        option.text = optionValue; // assignatioin d'un texte
        selectElement.add(option); // ajout de l'ellement
    })};
};


function goToOneBike(bikeId){
    sessionStorage.setItem("bikeId", bikeId);
    window.location.href = "/velo";
}