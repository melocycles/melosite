    // déclaration à la racine car utilisé à plusieurs endroits
var photoList = [];
var memoire = {};
// récupération du bikeId
const bikeId = parseInt(sessionStorage.getItem("bikeId"));

document.addEventListener('DOMContentLoaded', function () {
    
        // récupération des élémennts html
    const returnButton = document.getElementById('returnButton');
    const submitButton = document.getElementById("confirmButton");

    // récupération des donnés depuis le backend
    fetchData('/api/readBike', {"whoCall" : 'edit', "parameters" : { id: bikeId }}, fillForm);


    formContainer.addEventListener('submit', function (event) {
        event.preventDefault(); // empeche que clicker sur un bouton du formulaire redirige vers une page
    });
    returnButton.addEventListener('click', function() { // bouton retour
        window.location.href = "/velo";; // retourne à la page du vélo
    });

    submitButton.addEventListener('click', function () { // bouton valider
        const requiredFields = ["dateEntre", "origine", "benevole", "statusVelo"];
        const missingFields = requiredFields.filter(field => !document.getElementById(field).value); // vérfie que les 4 requiredFields ne sont pas vides

        if (missingFields.length == 0) { // si il ne manque pas de donné nécessaire
            updateBike(); // envoie les donnés renseigné à la database
        }
    });
});


/* rempli le formulaire avec les informations du vélo enregistré dans la database
    est appelé par le callabck de fetchData('/api/readBike', {"whoCall" : 'edit', "parameters" : { id: bikeId }}, fillForm);
*/
function fillForm(returnFromFetch) {
    formData = returnFromFetch.result
    // formSata est le retour de fetchData
    formData.forEach(function(attribute) { // parcourt tous les attributs renvoyé par le backend
        var element = document.getElementById(attribute[0]); // on récupère l'élément html correspondant
        
        if (element) { // on vérifie que l'élément éxiste
            if(element.type != "date"){ // il faut enregistrer la date à part car elle a besoin d'être formatté sous forme yyyy-mm-dd
                memoire[attribute[0]] = attribute[1]
            }
            if (element.type === 'checkbox') { // pas utilisé pour l'instant, je le laisse pour que l'implémentation de chackbox soit plus simple
                element.checked = attribute[1];
            } else if (element.type === 'date') {
                // Formater la date au format YYYY-MM-DD
                const formattedDate = new Date(attribute[1]).toISOString().split('T')[0];
                memoire[attribute[0]] = formattedDate   
                element.value = formattedDate;
            } else if (attribute[0].includes("photo")) {
                photoList.push(attribute[1]);
            }else {
                element.value = attribute[1];
            }
        } 
        
    })
    addPicture(photoList)
}


/* Envoie les nouvelles valeures au backend pour les enregistrer
*/
function updateBike(){
    var formData = {"id" : bikeId}; // crée le dictionnaire à envoyer à sqlCRUD.py
    const listeAttributes = ["benevole", "referent", "dateEntre", "statusVelo", "origine", "etatVelo", "marque", "typeVelo", "tailleRoue", "tailleCadre", "bycode", "electrique", "prochaineAction", "valeur", "destinataireVelo", "descriptionPublic", "descriptionPrive"]
    
        // vérifie si les photos dans les <img> de l'html sont différentes de celles de la mémoire
    for (let i = 0; i < photoList.length; i++) { 
        if (photoList[i] !== null && memoire[`photo${i + 1}`] != photoList[i]) {
            formData[`photo${i + 1}`] = photoList[i]; // si elles sont différentes on les ajoute aux donnés à update
        }
    }

        // ajouts des attributs ayant été modifié au dictionnaire formData. On vérifie si un élément à été modifié dans hasTheValueChange()
    for (const attribute of listeAttributes) { // parcourt tous les ellements du formulaire
            if(attribute == "electrique"){ // si l'attribut est ellectrique on le transforme en boolean
                if(document.getElementById(attribute).value == "true"){
                    hasTheValueChange(attribute, true)
                }else if(document.getElementById(attribute).value == "false"){
                    hasTheValueChange(attribute, false)
                }
            } else if(attribute == "valeur"){ // si l'attribut est valeur on le transforme en float
                hasTheValueChange(attribute, parseFloat(document.getElementById(attribute).value))

            }else{ // sinon on l'ajoute jsute (string)
                hasTheValueChange(attribute, document.getElementById(attribute).value); // on assigne à l'attribut sa valeur 
            }
    }
    

    // Envoie des données au backend
    fetchData('/api/modifyBike', formData,  window.location.href = "/velo")

    function hasTheValueChange(attribut, value){
        if(attribut == "valeur" && isNaN(parseFloat(value))){ // si l'attribut est valeur et que value n'est pas un nombre value devient null
            value = null
        }else if(value === ""){ // pour tous les autres attributs si value est vide value devient null
            value = null
        };
        
        if(memoire[attribut] != value){ // on assigne la valeur à formData pour l'envoyer au backend
            formData[attribut] = value
        }

    }
}


    /* affiche les images dans les canvas si elles sont présentes sinon affiche les logos. Gère le click sur les canvas pour changer les photos
        est appellé par fillForm()
    */
function addPicture(photoList){
    // photoList est envoyé par fillForm() contient les images envoyé par le backend
    const canvasList = [document.getElementById("photo1"), document.getElementById("photo2"), document.getElementById("photo3")]
    const cadreList = [new Image(),new Image(),new Image()]
    var svgPath = 'static/images/logoPhoto.svg'; // Chemin relatif vers votre fichier SVG
    let logoPositionX = 30;
    let logoPositionY = 0;
    let logoWidth = 250;
    let logoHeight = 150;

        // on mets les images dans les canvas, si il n'y a pas d'images on met le logo
    for (let i = 0; i <= 2; i++) {
        const index = i
        if(photoList[i]){
            firstImageload(index)
        }else{
            displayLogo(index)
        }
    }

    
        // gestion de la prise des photos
    for (let i = 1; i <= 3; i++) { // on parcourt les canvas un par un
        const canvasButton = canvasList[i-1]; // on récupère les canvas un par un (car dans l'html ils s'appellent canvas1, canvas2 et canvas3)
        const index = i; // on conserve i car on en a besoin dans displayBike() pour enregistrer la photo prise dans photoList

        canvasButton.addEventListener('click', async (ev) => { // lorsque l'on click sur un canvas
            ev.preventDefault(); // on empèche le comportement par défaut qui ne nous interesse pas

            // on crée un ellement input qui permet d'utiliser l'appareil photo du téléphonne
            const inputElement = document.createElement('input');
            inputElement.type = 'file';
            //inputElement.setAttribute('capture', 'environment'); // a activer si on veut utiliser uniquement l'appareil photo
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

        // est appelé plus tot dans addPicture() affiche le logo dans canvasX
    function displayLogo(i){
        var context = canvasList[i].getContext('2d');
        cadreList[i].src = svgPath
        cadreList[i].onload = function() {context.drawImage(cadreList[i],  logoPositionX, logoPositionY, logoWidth, logoHeight);}
    }

        // est appelé plus tot dans addPicture() affiche la photo venant du backend dans canvasX
    function firstImageload(i){
        var context = canvasList[i].getContext('2d');
        cadreList[i].src = "data:image/jpeg;base64," + photoList[i]
        cadreList[i].onload = function(){ context.drawImage(cadreList[i], 0, 0, canvasList[i].width, canvasList[i].height);}
    }
    

    // enregistre la photo prise dans photoList (pour pouvoir l'envoyer à la database après) + l'affiche sur la page web
    function displayPicture(file, canvas, index) {     
    /* file : la photo prise par le téléphonne
       canvas : l'ellement html canvas où sera affiché l'image
       index : le numéro (entre 1 et 3) de la photo
    */
        const reader = new FileReader();
        reader.readAsDataURL(file); // on charge le fichier
        
        reader.onload = function (loadedImage) { // Quand le fichier est chargé avec succès

            // on récupère le binaire de la photo puis on la stock dans photoList
            const imageData = loadedImage.target.result;
            photoList[index - 1] = imageData;
            
            const img = new Image(); // intialisation de d'une image vide
            const maxWidth = 600;
            var ratioWidth = 1;
            var ratioHeight = 1;
            var ratio = 1;
            img.src = loadedImage.target.result; // on ajoute la photo prise dans l'image crée
            img.onload = function () { // quand l'image est prête
                    // on récupère les dimensions de l'image
                originalImageWidth = img.width;
                originalImageHeight = img.height;
                if (originalImageWidth > maxWidth){ // on vérifie si l'image dépasse la dimension maximale
                    ratioWidth = maxWidth/originalImageWidth
                }if(originalImageHeight > maxWidth){ // on vérifie si l'image dépasse la dimension maximale
                    ratioHeight = maxWidth/originalImageHeight
                }
                ratio = Math.min(ratioWidth, ratioHeight) // on récupère le ratio le plus bas pour redimensionner l'image

                    // on redimensionne l'image grace au ratio obtenu précedemment
                canvas.width = img.width*ratio;
                canvas.height = img.height*ratio;

                    // on dessine l'image
                const context = canvas.getContext('2d');
                context.drawImage(img, 0, 0, img.width*ratio, img.height*ratio); // on affiche l'image dans le canvas
            };
        };
    }
}