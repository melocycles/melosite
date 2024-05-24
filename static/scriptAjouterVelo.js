    // déclaration à la racine car utilisé à plusieurs endroits.
let requiredFields
let listeAttributes
let allAttributes
const listSatutOutOfStock = ["vendu", "donné", "démonté", "recyclé", "perdu"]

fetchData("api/config", {}, getConfig) 
    
// C'est là que seront stocké les photos prises. On les stock dans une liste pour y accéder plus simplement
let capturedPhoto1 = null;
let capturedPhoto2 = null;
let capturedPhoto3 = null;
var photoList = [capturedPhoto1, capturedPhoto2, capturedPhoto3]

// récupération des canvas où seront affichés les photos sur la page
let canvas1 = document.getElementById("photo1")
let canvas2 = document.getElementById("photo2")
let canvas3 = document.getElementById("photo3")



document.addEventListener("DOMContentLoaded", function () { // ci dessous est effectué au chargement de la page
        // récupération des élémennts html
    const formContainer = document.getElementById('formContainer');
    const returnButton = document.getElementById('returnButton');
    const submitButton = document.getElementById("confirmButton");

    formContainer.addEventListener('submit', function (event) {
        event.preventDefault(); // empeche que clicker sur un bouton du formulaire redirige vers une page
    });

    returnButton.addEventListener('click', function () { // boutton Retour
        window.location.href = "/"; // retourne à la page parcourVelo
    });


    submitButton.addEventListener('click', function () { // vérifie que "dateEntre", "origine", "benevole" sont bien renseigné avant d'enregistrer le vélo
        const missingFields = requiredFields.filter(field => !document.getElementById(field).value);

        if (missingFields.length == 0) { // si il ne manque pas de donné nécessaire

            if(document.getElementById("statutVelo").value == "en stock" ){ // si le vélo est en stock on part dans addBike()
                    addBike()
            }else if(listSatutOutOfStock.includes(document.getElementById("statutVelo").value)){ // sinon ça veut dire qu'il est sorti du stock
                if(confirm("attention avec cette valeur de statut vélo le vélo sera considéré comme sorti du stock !")){ // on demande à l'utilisateur si il veut vraiment que le vélo soit sorti du stock
                    addBike()
                }
            }
        } 
    });


        // affichage des logos 

    var svgPath = 'static/images/logoPhoto.svg'; // Chemin relatif vers votre fichier SVG
    var logo1 = new Image();
    var logo2 = new Image();
    var logo3 = new Image();

    let logoPositionX = 30;
    let logoPositionY = 0;
    let logoWidth = 250;
    let logoHeight = 150;
    logo1.src = svgPath;
    logo2.src = svgPath;
    logo3.src = svgPath;
    
        // dessine les logos dans les canvas image
    var context1 = canvas1.getContext('2d');
    logo1.onload = function() {context1.drawImage(logo1,  logoPositionX, logoPositionY, logoWidth, logoHeight);}
    var context2 = canvas2.getContext('2d');
    logo2.onload = function() {context2.drawImage(logo2,  logoPositionX, logoPositionY, logoWidth, logoHeight);}
    var context3 = canvas3.getContext('2d');
    logo3.onload = function() {context3.drawImage(logo3,  logoPositionX, logoPositionY, logoWidth, logoHeight);}
    


        // gestion de la prise des photos

    for (let i = 1; i <= 3; i++) {
        const canvasButton = document.getElementById('photo' + i); // on récupère les canvas un par un (car dans l'html ils s'appellent canvas1, canvas2 et canvas3)
        const index = i; // on conserve i car on en a besoin dans displayNike() pour enregistrer la photo prise dans photoList


        canvasButton.addEventListener('click', async (ev) => { // lorsque l'on click sur un canvas
            ev.preventDefault(); // empeche que clicker sur un bouton du formulaire redirige vers une page

            // on crée un ellement input qui permet d'utiliser l'appareil photo du téléphonne ()
            const inputElement = document.createElement('input');
            inputElement.type = 'file';
            //inputElement.setAttribute('capture', ''); // a activer si on veut utiliser uniquement l'appareil photo
            inputElement.setAttribute('accept', 'image/*'); // on accepte que des images
            inputElement.click()

            inputElement.addEventListener('input', (event) => { // quand la photo prise
                const file = event.target.files[0]; // on récupère la photo
                if (file) { // on vérifie que le téléphonne nous a bien envoyé une photo
                    displayPicture(file, canvasButton, index);// on envoie la photo à displayBike pour l'afficher
                }
            },false);

            // Cliquez sur l'élément input pour ouvrir l'appareil photo
        }, {capture : true}, true);
    }

}, false);

function getConfig(returnFromFetch){
    const returnFromFetchArray = Object.entries(returnFromFetch);
    returnFromFetchArray.sort((a, b) => a[1].order - b[1].order);
    objects = Object.fromEntries(returnFromFetchArray);

    requiredFields = Object.keys(objects).filter(key => objects[key].addRequired);
    listeAttributes = Object.keys(objects).filter(key => objects[key].addBike)

    addField()
}

// enregistre la photo prise dans photoList (pour pouvoir l'envoyer à la database après) + l'affiche sur la page web
function displayPicture(file, canvas, index) {
    /* file : la photo prise par le téléphonne
       canvas : l'ellement html canvas où sera affiché l'image
       index : le numéro (entre 1 et 3) de la photo
    */
   function resize(width, height){
    const maxWidth = 800;
    const maxHeight = 600;
    var ratioWidth = 1;
        var ratioHeight = 1;
        var ratio = 1;
        if (width > maxWidth){ // on vérifie si l'image dépasse la dimension maximale
            ratioWidth = maxWidth/width
        }if(height > maxHeight){ // on vérifie si l'image dépasse la dimension maximale
            ratioHeight = maxHeight/height
        }
        ratio = Math.min(ratioWidth, ratioHeight) // on récupère le ratio le plus bas pour redimensionner l'image
        return([width*ratio, height*ratio])
   }

   function isFormatAuthorized(format){
    let authorizedFormat = ["png;", "jpeg", "jpg;", "webp", "jpeg"]
    if(authorizedFormat.includes(format)){return true}
    
    return false
   }

    const reader = new FileReader();
    reader.readAsDataURL(file); // on charge le fichier
    var img = new Image(); // intialisation de d'une image vide
    reader.onload = function (loadedImage) { // Quand le fichier est chargé avec succès
        //console.log(loadedImage)     

        img.src = loadedImage.target.result; // on ajoute la photo prise dans l'image crée
        let count = true

        if(!isFormatAuthorized(loadedImage.explicitOriginalTarget.result.substring(11,15))){
            //console.log("prout")
            //const { Image } = require('image-js');
            //Image.load(img.src).then(tiffImage => {})
        }

        img.onload = function () { // quand l'image est prête1
            if(count){
                count = false;
                // on récupère les dimensions de l'image
                originalImageWidth = img.width;
                originalImageHeight = img.height;
                
                [canvas.width,canvas.height] = resize(img.width,img.height)

                // on dessine l'image
                const context = canvas.getContext('2d');
                context.drawImage(img, 0, 0, canvas.width, canvas.height); // on affiche l'image dans le canvas
                img.src  = canvas.toDataURL('image/jpeg');
            

            // on récupère l'image redimensionné dans la variable img (dans img.src)  
            } // fin if count
        }; // fin img.onload
        
    } // fin reader.onload
    
        photoList[index - 1] = img; // enregistrement de l'image qui vient d'être prise
    }; // fin siplayPicture



    /* ajoute le vélo à la base de donné
        est appelé par le boutton valider    
    */
function addBike(){
    var formData = {}; // on définit le vélo comme en stock de base

    // on parcourt les 3 photos dans photoList. Si une photo a été prise on l'ajoute dans formData
    for (let i = 0; i < photoList.length; i++) {
        if (photoList[i] !== null) {
            formData[`photo${i + 1}`] = photoList[i].src;
        }
    }

    // crée le dictionnaire à envoyer à sqlCRUD.py
    for (const attribute of listeAttributes) { // parcourt tous les ellements qui peuvent être rensignés

        if (document.getElementById(attribute).value !== "") { // si l'utilisateur a renseigné une valeur 
            let currentAttributValue = document.getElementById(attribute).value
            if(attribute == "valeur"){ // si l'attribut est valeur on le transforme en float (aka nombre à virgules)
                formData[attribute] = parseInt(currentAttributValue)

            }else if(attribute == "dateEntre"){ // si l'attribut est la date on la formate
                let dateValue = new Date(currentAttributValue);
                const formattedDate = new Date(dateValue).toISOString().split('T')[0]; // formate sous la forme yyyy-mm-dd
                formData[attribute] = formattedDate
                
            }else if(attribute == "statutVelo" && listSatutOutOfStock.includes(currentAttributValue)){ // le vélo est sorti du stock
                formData["dateSortie"] = formData["dateEntre"] 
            }else{ // sinon on l'ajoute sans avoir à la préparer (car c'est une string (aka chaine de caractère))
                formData[attribute] = frenchToBool(currentAttributValue); // on assigne à l'attribut sa valeur 
            }
        }
    }

    // envoi deu formulaire au backend pour l'enregistrement dans la database pui redirection vers la apge parcoursVelo
    //fetchData('/api/addBike', formData, window.location.href = '/parcourVelo');
};


function addField(){
    function textInput(){
        // <input type="text" id="title" name="titre" required />
        const newInput = document.createElement("input")
        newInput.setAttribute("id", objects[currentAttribut]["camelCase"]);
        newInput.setAttribute("name", objects[currentAttribut]["lowCase"]);
        newInput.setAttribute("type", objects[currentAttribut]["entryType"][1]);

        if(requiredFields.includes(currentAttribut)){
            newInput.setAttribute("required", "");
        }
        formContainer.insertBefore(newInput, lastButtons);
    }
    function textAreaInput(){
        const newInput = document.createElement("textarea")
        newInput.setAttribute("id", objects[currentAttribut]["camelCase"]);
        newInput.setAttribute("name", objects[currentAttribut]["camelCase"]);
        newInput.setAttribute("rows", "4");
        formContainer.insertBefore(newInput, lastButtons);
    }
    function selectInput(){
        const newInput = document.createElement("select")
        newInput.setAttribute("id", objects[currentAttribut]["camelCase"]);
        newInput.setAttribute("name", objects[currentAttribut]["camelCase"]);

        if(requiredFields.includes(currentAttribut)){
            newInput.setAttribute("required", "");
        }
        var emptyOption = document.createElement("option");
        emptyOption.setAttribute("value", "");
        newInput.appendChild(emptyOption);
        
        for(item of objects[currentAttribut]["values"]){
            var option = document.createElement("option");
            option.setAttribute("value", item);
            option.textContent = item
            newInput.appendChild(option);
        }
        formContainer.insertBefore(newInput, lastButtons);

    }

    const lastButtons = document.getElementById("confirmButton")
    
    for(currentAttribut of listeAttributes){
        
        const newLabel = document.createElement('label');
        newLabel.setAttribute('for', currentAttribut);
        newLabel.textContent = objects[currentAttribut].withSpace + ":";

        if(requiredFields.includes(currentAttribut)){
            newLabel.innerHTML += (" <b>*</b>");
        }
        formContainer.insertBefore(newLabel, lastButtons);

        switch (objects[currentAttribut]["entryType"][0]){
            case "input":
                returnedHTML = textInput();
                break
            case "textarea":
                returnedHTML = textAreaInput();
                break
            case "select":
                returnedHTML = selectInput();
                break
        }
       
    }
}
