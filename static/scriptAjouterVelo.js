let capturedPhoto = null;

document.addEventListener("DOMContentLoaded", function () { // ci dessous est effectué au chargement de la page
    // gère les bouttons retour, annuler, valider
    const formContainer = document.getElementById('formContainer');
    const returnButton = document.getElementById('returnButton');
    const submitButton = document.getElementById("confirm");
    const photoButtonContenair = document.getElementById("pohtoButtonContener")

    formContainer.addEventListener('submit', function (event) {
        event.preventDefault(); // empeche que clicker sur un bouton du formulaire redirige vers une page
    });
    photoButtonContenair.addEventListener('click', function (event){
        event.preventDefault();
    }); 
    returnButton.addEventListener('click', function () {
        window.location.href = "/"; // retourne à la page parcourVelo
    });

    submitButton.addEventListener('click', function () {
        const requiredFields = ["dateEntre", "origine", "referent"];
        const missingFields = requiredFields.filter(field => !document.getElementById(field).value);

        if (missingFields.length == 0) { // si il ne manque pas de donné nécessaire
            addBike(); // envoie les donnés renseigné à la database
        } 

    });


    // prendre la photo
    video = document.getElementById('video');
    activeCamerabutton = document.getElementById('activeCamera');


// Supposons que vos boutons aient des ID consécutifs photoButton1, photoButton2, photoButton3
    for (let i = 1; i <= 3; i++) {
        const takePictureButton = document.getElementById('photoButton' + i);
        const takePictureCanvas = document.getElementById('canvas' + i);
        if(i != 1){
            takePictureButton.disabled = true
        };

        takePictureButton.addEventListener('click', (ev) => {
            const index = i
            const nextButtonIndex = i + 1;

            takepicture(i);
            video.style.display = 'none';

            if (nextButtonIndex <= 3) {
                const nextButton = document.getElementById('photoButton' + nextButtonIndex);
                nextButton.disabled = false;
            }

            // Ajoutez ici le reste du code que vous souhaitez exécuter lors du clic sur n'importe lequel des boutons
        });
    }

    activeCamerabutton.addEventListener( // au click pour démarer la prise de la photo
        "click",
        (ev) => {
            // Demander l'accès à la caméra dès que l'utilisateur clique sur "Prendre une photo"
            navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
                .then((stream) => { // si l'autorisation est accordé
                    video.style.display = 'block';
                    video.srcObject = stream;

                    // Ajoutez un événement de suivi pour mettre à jour la vidéo en temps réel
                    video.addEventListener('loadedmetadata', () => {
                        video.play();
                    });
                })
                .catch((error) => {
                    console.error('Erreur lors de l\'accès à la caméra: ', error);
                });
            ev.preventDefault();
        },
        false,
    );
  

    function takepicture(photoId) { // prend la photo
        const canvas = document.getElementById('canvas' + photoId); // Obtenez le canvas correspondant au photoId
        const context = canvas.getContext('2d');
        const width = video.videoWidth;
        const height = video.videoHeight;

        canvas.width = width;
        canvas.height = height;

        context.drawImage(video, 0, 0, width, height); // dessine la photo prise dans le canvas

        video.srcObject.getTracks().forEach(track => track.stop()); // arrete le flux vidéo

        const data = canvas.toDataURL('image/jpeg'); // Convertit le contenu du canevas en une URL de données au format PNG

        if(photoId==1){
            capturedPhoto1 = data;
        }else if(photoId==2){
            capturedPhoto2 = data
        }else if(photoId==3){
            capturedPhoto3 = data
        }
        
    }

}, false);

function addBike(){
    // !!!!!!!!! ajouter photo !!!!!!!!!!!!!!! (manque le bicode sur la page aussi)
    const photoList = [capturedPhoto1, capturedPhoto2, capturedPhoto3]
    var formData = {"status" : "en stock"};
    for (let i = 0; i < photoList.length; i++) {
        if (photoList[i] !== null) {
            formData[`photo${i + 1}`] = photoList[i];
        }
    }
    
    const listeAttributes = ["referent", "dateEntre", "origine", "etatVelo", "marque", "typeVelo", "tailleRoue", "tailleCadre", "bycode", "electrique", "prochaineAction", "valeur", "destinataireVelo", "descriptionPublic", "descriptionPrive"]
    
    // crée le dictionnaire à envoyer à sqlCRUD.py
    for (const attribute of listeAttributes) { // parcourt tous les ellements qui peuvent être rensignés
        if (document.getElementById(attribute).value !== "") { // si il y a une valeur
            
            if(attribute == "electrique"){ // si l'attribut est ellectrique on le transforme en boolean
                if(document.getElementById(attribute).value == "True"){
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
    fetch('/api/addBikeJS', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=UTF-8',
        },
        body: JSON.stringify(formData),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('erreur scriptAjouterVelo : erreur réseau');
        }
        return response.json();
    })
    .then(data => {
        window.location.href = '/'; // si tout c'est bien passé redirection vers la page parcurVelo
    })
    .catch(error => {
        console.error('erreur scriptAjouterVelo l\'envoi des données: ', error);
    });

};
