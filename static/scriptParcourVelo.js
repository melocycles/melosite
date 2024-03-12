document.addEventListener("DOMContentLoaded", function () { // action lors du changement de la page
        // récupération des élémennts html
    var formContainer = document.getElementById('formContainer');
    var addButton = document.getElementById('addButton');
    var filterButton = document.getElementById('filterButton');
    var cancelButton = document.getElementById('cancelButton');
    var confirmButton = document.getElementById('confirmButton');
    var resetButton = document.getElementById('resetButton');


        // récupération des donnés depuis le backend
    fetchData('/api/readBike', {"whoCall" : 'search', "parameters" : {}}, displayBikes); // récupération de la photo1, la descriptionPublic & l'id puis on les display
    fetchData("/api/getFilterValue", {"whoCall" : "", "parameters" : ""}, addOptionsToSelect); // récupération des valeurs éxistantes dans chacun des paramètres pour ajouter des valeurs de filtre


        // gestion des bouttons
    formContainer.addEventListener('submit', function(event) { 
        event.preventDefault(); // empeche que clicker sur un bouton du formulaire redirige vers une page
    });
    addButton.addEventListener('click', function(){
        window.location.href = "/ajouterVelo"; // envoi vers la page addBike
    });

    filterButton.addEventListener('click', function() { // bouton filtrer
        toggleForm(); // affiche les filtres
    });
    cancelButton.addEventListener('click', function() { // bouton annuler de la page filtre
        hideForm(); // masque le formulaire
    });
    confirmButton.addEventListener('click', function() { // bouton confirmer de la page filtre
        hideForm(); // masque le formulaire
        sendFilter(); // envoi les valeurs de filtre au backend puis affiche les vélos correspondants
    });
    resetButton.addEventListener('click', function () { // boutton reset de la page filtre
        resetSelectOptions(['marque', 'typeVelo', 'tailleRoue', 'tailleCadre', 'electrique', 'etatVelo', 'statusVelo','origine', 'prochaineAction', 'referent', 'destinataireVelo', "id"]); // enlève toutes les valeur de filtre
    });
});



/* affiche/masque le formualaire. En réalité il fait 80% de l'écran en largeur. pour le cacher on l'envoie de sa taille à droite (donc hors de l'écran).
    La ligne overflow-x:hidden;  dans stylesParcourVelo.css empèche le scroll à droite il est donc invisible pour l'utilisateur.
    pour l'afficher l'afficher on le place à droite.
    la ligne transition: 0.5s; dans styleParcoursVelo.css donne l'effet de glissement
*/
function toggleForm() {
    formContainer.style.right = (formContainer.style.right === '0' || formContainer.style.right === '') ? '-80%' : '0';
};
function hideForm() {
    formContainer.style.right = '-80%';
};


// remet toutes les valeurs de filtres à 0
function resetSelectOptions(selectIds) {
    selectIds.forEach(selectId => { // parcourt les filtres
        document.getElementById(selectId).value = 'None'; // assigne la value None à chacun
    });
}


/* Cette fonction gère le filtrage des vélos
     récupère les valeures renseignés (addToFormData) et les ajoute dans formData
     efface les vélo qui étaient affichés
     récupère du backend les vélos correspondants aux filtres
*/
function sendFilter(){
    function addToFormData(elementId) { // vérifie qu'une valeur de filtre a été choisi avant de l'envoyer à flask
        var value = document.getElementById(elementId).value; 
        if (value !== "None" && value != "") {
            if(elementId == "id"){ // éxeption pour id car on veut récupérer une int pas une string
                formData[elementId] = parseInt(value)
            }else{
                formData[elementId] = frenchToBool(value);
            }
        }
    }

    var formData = {};
    // récupération des valeurs de filtres dans formData si elles ne sont pas None
    addToFormData('marque');
    addToFormData('typeVelo');
    addToFormData('tailleRoue');
    addToFormData('tailleCadre');
    addToFormData('electrique');
    addToFormData('etatVelo');
    addToFormData('statusVelo');
    addToFormData('origine');
    addToFormData('prochaineAction');
    addToFormData('referent');
    addToFormData('destinataireVelo');
    addToFormData('id')


    document.getElementById('veloPart').innerHTML = ''; // supprime les vélos affichés
    fetchData('/api/readBike',{"whoCall" : "search", "parameters" : formData}, displayBikes) // récupération des vélos correspodnants aux filtres
};




/* affiche les vélo avec les data récupéré de la base de donné
    est appelé par le callback de fetchData('/api/readBike', {"whoCall" : 'search', "parameters" : {}}, displayBikes); 
*/
function displayBikes(returnFromFetch) {
    bikesData = returnFromFetch.result
    var veloPart = document.getElementById('veloPart'); // récupère le conteneur global des vélo

    bikesData.forEach(function(bike) { // parcourt tous les vélos pour les créer un par un dans la page web
        // crée le conteneur du vélo avec  comme classe veloCadre
        var veloCadre = document.createElement('div'); 
        veloCadre.classList.add('veloCadre');
        
        // ajoute le conteneur de l'image avec comme classe veloImage. Ajoute l'image à l'intérieur
        var veloImage = document.createElement('img'); 
        veloImage.classList.add('veloImage');
        veloImage.src = "data:image/jpeg;base64," + bike.photo1;

        // ajoute le conteneur de la description. Vérifie que la description n'est pas trop longue (cutString) puis l'ajoute
        var descriptionParagraph = document.createElement('p');
        descriptionParagraph.textContent = cutString(bike.title)// cutString(bike.descriptionpublic); // on coupe la description pour qu'elle ne fasse pas plus de deux ligne (cf la fonction)

        // ajoute les 3 ellements précedemment crée à l'html
        veloCadre.appendChild(veloImage);
        veloCadre.appendChild(descriptionParagraph);
        veloPart.appendChild(veloCadre);
        
        veloCadre.addEventListener('click', function() { // ajoute une interraction au click qui renvoie vers la page velo.html avec l'id du vélo
            goToOneBike(bike.id);
        });})


        function cutString(string){ // découpe la description pour que le nom du vélo ne fasse pas plus de 2 lignes et que la découpe se fasse au mot près
            if(string == null){ // si la valeur n'a pas été renseigné on renvoie une string vide
                return ""
            }else if(string.length <30){ // si elle fait déjà moins de 30 caractères on la renvoi telle quelle
                return string
            }else{
                const lastSpaceIndex = string.lastIndexOf(' ', 30); // on trouve le dernier espace dans les 30 premiers caractères
                return string.substring(0, lastSpaceIndex) + "...";
            }
        }
    
        function goToOneBike(bikeId){ // redirige vers la page velo.html
            sessionStorage.setItem("bikeId", bikeId); // enregistre l'id du vélo dans le navigateur web pour que le bon vélo puisse être affiché
            window.location.href = "/velo";
        }
};



/*  ajoute les options possible dans le formulaire de filtre
    est appelé par le callback de fetchData("/api/getFilterValue", {"whoCall" : "", "parameters" : ""}, addOptionsToSelect);
*/
function addOptionsToSelect(returnFromFetch) {

    function addOption(optionsArray, selectElement){
        optionsArray.forEach(function (optionValue) { // parcourt toutes las valeurs éxistantes
            var option = document.createElement("option"); // création d'une option (d'un élément html)
            option.value = booltoFrench(optionValue); // assignation de sa valeur pour le renvoi du formulaire
            option.text = booltoFrench(optionValue); // assignatioin d'un texte
            selectElement.add(option); // ajout de l'ellement

            if(selectElement == statusVeloSelect && option.value == "en stock"){
                option.selected =true
            }
        }
    )};


    result = returnFromFetch.result
        // recupère les ellemeents html où seront placés nos options
    var marqueSelect = document.getElementById("marque");
    var typeVeloSelect = document.getElementById("typeVelo");
    var tailleRoueSelect = document.getElementById("tailleRoue");
    var tailleCadreSelect = document.getElementById("tailleCadre");
    var electriqueSelect = document.getElementById("electrique")
    var etatVeloSelect = document.getElementById("etatVelo");
    var statusVeloSelect = document.getElementById("statusVelo");
    var origineSelect = document.getElementById("origine")
    var prochaineActionSelect = document.getElementById("prochaineAction")
    var referentSelect = document.getElementById("referent")
    var destinataireVeloSelect = document.getElementById("destinataireVelo")


        // pour chaque attributs on ajoute les valeurs possibles
    addOption(result.marque, marqueSelect);
    addOption(result.typeVelo, typeVeloSelect);
    addOption(result.tailleRoue, tailleRoueSelect);
    addOption(result.tailleCadre, tailleCadreSelect);
    addOption(result.electrique, electriqueSelect);
    addOption(result.etatVelo, etatVeloSelect);
    addOption(result.statusVelo, statusVeloSelect);
    addOption(result.origine, origineSelect);
    addOption(result.prochaineAction, prochaineActionSelect);
    addOption(result.referent, referentSelect);
    addOption(result.destinataireVelo, destinataireVeloSelect);
};


