///
/// ce fihcier regroupe les fonctions javascript utilisé à plusieurs endroits dans le programme
/// attention à ne pas nommer de la même manière une fonction dans un autre fichier !
///


/* pour la connexion/déconnexion. Présent sur toutes les pages
*/
document.addEventListener("DOMContentLoaded", function () { // quand la page se charge
    const header = this.getElementById("header")
    var connectionLogo = document.createElement('img');
    connectionLogo.src = 'static/images/connectionLogoWhite.png';
    connectionLogo.id = "connectionLogo";
    var assoLogo = document.createElement('img');
    assoLogo.src = 'static/images/logoHeader.jpg';
    assoLogo.id = "headerLogo";

    const headerButtons = this.getElementById("headerButtons")
    
    header.insertBefore(connectionLogo, headerButtons);
    header.insertBefore(assoLogo, headerButtons);


    const connexionLogo = document.getElementById("connectionLogo")
    connexionLogo.addEventListener("click", function(){
        window.location.href = "/log"
    });

    assoLogo.addEventListener("click", function(){
        window.location.href = "/"
    })

    if (document.querySelector('.autoForm')) {

    }
})

/* utilisé dans tous les fichiés js
   s'occupe d'envoyer et récupérer des donnés au/du backend*/

function fetchData(url, dataToSend, callback) {
    fetch(url, {    // url = nom de la route flask
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', // indique qu'on utilise le format json
        },
        body: JSON.stringify(dataToSend),  // transformation en json
    })

    .then(response => {
        if(response.ok){ // est ok si la requête est un succès (code http 2xx (ex : 200))
            return response.json(); // transforme la réponse en ellement json et envoi data au prochain then
        }else{
            console.log("response not ok !! : ", response)
        }
    })  

    .then(data => {
        callback(data); // appel de la fonction prévu dans callback
    })

    .catch(error => {
        console.error('Erreur de fetchData lors de la récupération des données:', error);
    });
};


function booltoFrench(value){
    // transforme boolean en français pour l'affichage
    if(value == true || value == "True" || value == "true"){return "oui"}
    else if(value == false || value == "False" || value == "false"){return "non"}
    else{return value}
}

function frenchToBool(value){
    // transforme oui/non en bool pour l'enregistrement dans la db
    if(value == "oui" || value == "True" || value == "true"){return true}
    else if(value == "non" || value == "False" || value == "false"){return false}
    else{return value}
}



/* fonction de débugage */
function fetchTest(Sentdata){
    console.log("enter fetchTest")
    fetch("api/fetchTest", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=UTF-8',
        },
        body: JSON.stringify(Sentdata),
    })
    .then(response => {
        if (!response.ok) {
            console.log(response)
            throw new Error('erreur fetchTest : erreur réseau');
        }
        else{
            console.log("la réponse de fetch test est ok")
        }
        
    })

    .catch(error => {
        console.error('erreure dans fetchTest à l\'envoi des données: ', error);
    });

};




// affichage des logos des photos
var svgPath = 'static/images/logoPhoto.svg'; // Chemin relatif vers votre fichier SVG
var logo1 = new Image();
var logo2 = new Image();
var logo3 = new Image();
logo2.src = svgPath;
logo3.src = svgPath;
let logoPositionX = 30;
let logoPositionY = 0;
let logoWidth = 250;
let logoHeight = 150;
logo1.src = svgPath;
let canvas1 = document.getElementById("picture1")
let canvas2 = document.getElementById("picture2")
let canvas3 = document.getElementById("picture")
var context1 = canvas1.getContext('2d');
logo1.onload = function() {context1.drawImage(logo1,  logoPositionX, logoPositionY, logoWidth, logoHeight);}
var context2 = canvas2.getContext('2d');
logo2.onload = function() {context2.drawImage(logo2,  logoPositionX, logoPositionY, logoWidth, logoHeight);}
var context3 = canvas3.getContext('2d');
logo3.onload = function() {context3.drawImage(logo3,  logoPositionX, logoPositionY, logoWidth, logoHeight);}


// gestion de la prise de photo
let capturedPhoto1 = null;
let capturedPhoto2 = null;
let capturedPhoto3 = null;
var photoList = [capturedPhoto1, capturedPhoto2, capturedPhoto3]

for (let i = 1; i <= 3; i++) {
    const canvasButton = document.getElementById('photo' + i); // on récupère les canvas un par un (car dans l'html ils s'appellent canvas1, canvas2 et canvas3)
    const index = i; // on conserve i car on en a besoin dans displayNike() pour enregistrer la photo prise dans photoList

    canvasButton.addEventListener('click', async (ev) => { // lorsque l'on click sur un canvas
        ev.preventDefault(); // empeche que clicker sur un bouton du formulaire redirige vers une page

        // on crée un ellement input qui permet d'utiliser l'appareil photo du téléphonne ()
        const inputElement = document.createElement('input');
        inputElement.type = 'file';
        //inputElement.setAttribute('capture', 'environment'); // a activer si on veut utiliser uniquement l'appareil photo
        inputElement.setAttribute('accept', 'image/*'); // on accepte que des images
        inputElement.click()

        inputElement.addEventListener('input', (event) => { // quand la photo prise
            const file = event.target.files[0]; // on récupère la photo
            if(file && file.name.includes(".heic")){
                // get image as blob url
                let blobURL = URL.createObjectURL(file);
                
                // convert "fetch" the new blob url
                let blobRes = fetch(blobURL).then(res=>{return res.blob()})
                .then(blob=>{return heic2any({blob})})
                .then(imageBlob => {displayPicture(new File([imageBlob], file.name.split(".")[0]+".png"), canvasButton,index)})
                console.log(file.name.split(".")[0]+".png")
            }       
            else if (file) { // on vérifie que le téléphonne nous a bien envoyé une photo
                displayPicture(file, canvasButton, index);// on envoie la photo à displayBike pour l'afficher
            }
        },false);

        // Cliquez sur l'élément input pour ouvrir l'appareil photo
    }, {capture : true}, true);
}

    // enregistre la photo prise dans photoList (pour pouvoir l'envoyer à la database après) + l'affiche sur la page web
    function displayPicture(file, canvas, index) {
        /* file : la photo prise par le téléphonne
        canvas : l'ellement html canvas où sera affiché l'image
        index : le numéro (entre 1 et 3) de la photo
        */
        // file c'est le fichier brut
        const reader = new FileReader();
        reader.readAsDataURL(file); // on charge le fichier
        var img = new Image(); // intialisation de d'une image vide
        
        reader.onload = function (loadedImage) { // Quand le fichier est chargé avec succès
            if (true){
            const fileType = file.type.toLowerCase();

            if (fileType === 'image/tiff' || fileType === 'image/tif') {
                convertTIFFToJPG(loadedImage.target.result).then(jpgDataURL => {
                    img.src = jpgDataURL; // Utiliser l'image JPEG convertie
                    })
                }else if (fileType === 'image/heic') {
                    heic2any(loadedImage.target.result)
                    .then((jpgDataURL) => {
                        console.log(jpgDataURL)
                    })
                    .catch((e) => {
                        console.log(e)
                    })
                }
            }

            img.src = loadedImage.target.result; // on ajoute la photo prise dans l'image crée
    
                const maxWidth = 900;
                const maxHeight = 450;
                var ratioWidth = 1;
                var ratioHeight = 1;
                var ratio = 1;
                let count = true;

                img.onload = function () { // quand l'image est prête
                    if (count) {
                        count = false;
                        // on récupère les dimensions de l'image
                        originalImageWidth = img.width;
                        originalImageHeight = img.height;
                        if (originalImageWidth > maxWidth) { // on vérifie si l'image dépasse la dimension maximale
                            ratioWidth = maxWidth / originalImageWidth;
                        }
                        if (originalImageHeight > maxHeight) { // on vérifie si l'image dépasse la dimension maximale
                            ratioHeight = maxHeight / originalImageHeight;
                        }
                        ratio = Math.min(ratioWidth, ratioHeight); // on récupère le ratio le plus bas pour redimensionner l'image
    
                        // on redimensionne l'image grace au ratio obtenu précedemment
                        canvas.width = img.width * ratio;
                        canvas.height = img.height * ratio;
    
                        // on dessine l'image
                        const context = canvas.getContext('2d');
                        context.drawImage(img, 0, 0, img.width * ratio, img.height * ratio); // on affiche l'image dans le canvas
                        img.src = canvas.toDataURL(); // on récupère l'image redimensionné dans la variable img
                    }
                };
            }
    
            photoList[index - 1] = img; // enregistrement de l'image qui vient d'être prise
        };
    
        function convertTIFFToJPG(dataURL, quality = 0.9) {
            return new Promise((resolve, reject) => {
                if (typeof Tiff === 'undefined') {
                    reject("Tiff.js n'est pas chargé correctement.");
                }
        
                var xhr = new XMLHttpRequest();
                xhr.open('GET', dataURL, true);
                xhr.responseType = 'arraybuffer';
                xhr.onload = function(e) {
                    var tiff = new Tiff({ buffer: xhr.response });
                    var canvas = tiff.toCanvas();
                    var jpgDataURL = canvas.toDataURL('image/jpeg', quality);
                    resolve(jpgDataURL);
                };
                xhr.send();
            });
        }        
        