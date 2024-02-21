document.addEventListener("DOMContentLoaded", function () { // quand la page se charge
    // récupération de l'id stocké dans le navigateur. On le transforme en int car il est stocké en string
    const bikeId = parseInt(sessionStorage.getItem("bikeId")); 

        // récupération des élémennts html
    const returnButton = document.getElementById("returnButton");
    const switchButton = document.getElementById("switchButton");

    const modificationTrackingSection = document.getElementById('modificationTrackingSection');
    const bikeInfoSection = document.getElementById('bikeInfoSection');

    const photo1Contener = document.getElementById("photo1");
    const photo2Contener = document.getElementById("photo2");
    const photo3Contener = document.getElementById("photo3");

        // récupération des donnés depuis le backend pour l'onglet info
    fetchData('/api/readBike', {"whoCall" : 'global', "parameters" : {"id": bikeId} }, genererListeCaracteristiques); // récupération des infos générales
    fetchData('/api/readBike', {"whoCall" : 'detail', "parameters" : {"id": bikeId} }, genererListeDetail); // récupération des infos affichés dans détail
    
    fetchData('/api/readModification', {"bikeId" : bikeId}, genereListModificationTracking)


        // gestion des bouttons
    returnButton.addEventListener('click', function() { // bouton retour
        sessionStorage.removeItem("bikeId"); // supprime le bikeId du vélo que l'on consultait
        window.location.href = "/parcourVelo";; // retourne à la page parcourVelo
    });
    switchButton.addEventListener("click", function() {
        switchDisplay()
    })

        // gestion du changement d'image
    photo1Contener.addEventListener("click", function(){ // miniature 1
        changeImage("photo1")
    });
    photo2Contener.addEventListener("click", function(){ // miniature 2
        changeImage("photo2")
    });
    photo3Contener.addEventListener("click", function(){ // miniature 3
        changeImage("photo3")
    });
});


/* genere la liste des caractéristiques de l'onglet info
    est appelé par le callabck de fetchData('/api/readBike', {"whoCall" : 'global', "parameters" : {"id": bikeId} }, genererListeCaracteristiques);
*/
function genererListeCaracteristiques(returnFromFetch) {
    caracteristics = returnFromFetch.result
    
    const photoKey = ["photo1", "photo2", "photo3"]; // pour simplifier le code plus loins
    const listColumnCaracteristics = document.getElementById('columnLeftCaracteristics'); // repère l'ellement html à modifier
    const listColumnValues = document.getElementById("columnRightCaracteristics"); // repère l'ellement html à modifier

    caracteristics.forEach(function(pair) { // parcourt tous les ellements retourné par flask. function(pair) permet de les avoir sous la forme clef valeur
        if (photoKey.includes(pair[0])){
            if(pair[1] !== null){ // Si la clef est "photo1", "photo2" ou "photo3
                var imgElement = document.getElementById(pair[0]); // recupère l'ellement html qui a pour id photoX (1, 2 ou 3)
                imgElement.src = "data:image/png;base64," + pair[1]; // ajout de l'entête
                if (pair[0] === photoKey[0]){ // si c'est photo1 on la met aussi dans grandeImage
                        var imgElement = document.getElementById("largeImage");
                        imgElement.src = "data:image/jpeg;base64," + pair[1]; 
                }
            }
        } else { // ce n'est pas une photo on l'ajoute dans les listes
            // Créez un élément li pour la colonne de gauche (caractéristiques)
            listColumnCaracteristics.appendChild(createLi(pair[0]));

            // Créez un élément li pour la colonne de droite (valeurs)
            if(pair[1]){ // si l'attribut à une valeur on l'ajoute
                var li = createLi(pair[1]);
            } else{
                var li = createLi("."); // sinon on mets un point invisble (blanc) pour que les attributs et valeurs restent allignés
                li.style.color = "white";
            }
            listColumnValues.appendChild(li)
        }
    });
};

/* genere la liste affiché de l'onglet info
    est appelé par le callabck de fetchData('/api/readBike', {"whoCall" : 'detail', "parameters" : {"id": bikeId} }, genererListeDetail);
*/
function genererListeDetail(returnFromFetch) {
    caracteristics = returnFromFetch.result
    // caracteristics est le retour de fetchData
    const listColumnCaracteristics = document.getElementById('columnLeftDetail'); // repère l'ellement html à modifier
    const listColumnValues = document.getElementById("columnRightDetail"); // repère l'ellement html à modifier

    caracteristics.forEach(function(pair) {// parcourt tous les ellements retourné par flask. function(pair) permet de les avoir sous la forme clef value
        // Créez un élément li pour la colonne de gauche (caractéristiques)
        listColumnCaracteristics.appendChild(createLi([pair[0]]));

        // Créez un élément li pour la colonne de droite (valeurs)
        if(pair[1]){ // si l'attribut à une valeur on l'ajoute
            var li = createLi(pair[1]);
        } else{
            var li = createLi("."); // sinon on mets un point invisble (blanc) pour que les attributs et valeurs restent allignés
            li.style.color = "white";
        }
        listColumnValues.appendChild(li)
    });
};  


function genereListModificationTracking(returnFromFetch){
    modificationTracking = returnFromFetch.result[0]
    const listColumnModificationTracking = document.getElementById('modificationTrackingSection'); // repère l'ellement html à modifier
    var phraseToDisplay = ""
    modificationTracking.sort((a, b) => a.timestamp - b.timestamp);

    modificationTracking.forEach(function(object) {// parcourt tous les ellements retourné par flask. function(pair) permet de les avoir sous la forme clef value
        // Créez un élément li pour la colonne de gauche (caractéristiques)
        if(object.fieldModified == "création"){
            phraseToDisplay = `le ${object.dateOfModification} ${object.benevole} a crée le vélo`
        }
        else if(object.fieldModified == ``){
        }
        else{
            phraseToDisplay = `le ${object.dateOfModification} ${object.benevole} a changé ${object.fieldModified} de ${object.oldValue} a ${object.newValue}`
        }
        listColumnModificationTracking.appendChild(createLi(phraseToDisplay))
    });
};


// crée les ellements de liste. Est appelé par genererListeCaracteristiques et genererListeDetail
function createLi(textContent) {
    var liElement = document.createElement('li'); // crée un ellement <li>
    liElement.textContent = textContent; // y ajoute le texte
    return liElement; // le retourne pour qu'il soit injecté dans l'html
}

// change l'image affiché dans le conteneur class="largeImage" lors du click sur une des mininatures
function changeImage(id) {
    var imgElement = document.getElementById("largeImage"); // recupère l'ellement html grandeImage
    var imageToPut = document.getElementById(id).src;   // récupère la photo stocké dans l'image clické
    console.log(imageToPut)
    imgElement.src = imageToPut; // modifie l'html pour afficher la nouvelle image
};


function switchDisplay(){
    let actualStatut = switchButton.textContent;
    
    if(actualStatut == "info"){
        modificationTrackingSection.style.display = 'none'
        bikeInfoSection.style.display = "block"
        switchButton.textContent = 'suiviModif'
    }
    else{
        modificationTrackingSection.style.display = 'flex'
        bikeInfoSection.style.display = "none"
        switchButton.textContent = 'info'
    }
}