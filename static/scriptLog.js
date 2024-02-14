//  gère la page de logIn et de logOut. On vérifie quelle page c'est en fonction de l'éxistence du boutton de connection

document.addEventListener('DOMContentLoaded', function () { // au chargement de la page

    const returnButton = document.getElementById('returnButton');
    returnButton.addEventListener('click', function() { // bouton retour
        window.location.href = "/parcourVelo"; // retourne à la page du vélo
    });

    if(document.getElementById("connectButton")){ // si le boutton connection  éxiste (aka l'utilisateur est déconnecté) page logIn
        const connectButton = document.getElementById("connectButton")
        const userNameField = document.getElementById("username")
        const passawordField = document.getElementById("password")
        const form = document.getElementById("form")

        form.addEventListener('submit', function (event) {
            event.preventDefault(); // empeche que clicker sur un bouton du formulaire redirige vers une page
        });
        
        connectButton.addEventListener("click", function(){ // boutton connection 
            const formData = {"userName" : userNameField.value, "password" : passawordField.value} // ajout des valeurs du formulaires au formData, envoyé ensuite au backend
            fetchData("/api/logIn", formData, processResponse) // envoie des donnés au backend puis on le traite
        });
    
    }else{ // si le boutton connection n'éxiste pas (aka l'utilisateur est connecté) page logOut

        if(document.getElementById('disconnectButton')){ // boutton déconnection
            const disconnectButton = document.getElementById('disconnectButton');
            disconnectButton.addEventListener('click', function() { // bouton déconnection
                document.cookie = "uuid=; expires=Thu, 10 Mai 1896 06:06:18 UTC; path=/;"; // on retire le cookie (en définissant sa date d'expiration dans le passé)
                window.location.href = "/parcourVelo"; // redirection vers la page parcourVelo
                });
            }
        }

});

function processResponse(response){
    if (response.result == "mauvaise combianaison username/mot de passe"){ // si la combinaison est mauvaise on affiche le popUp d'erreur
        popUp(response.result)
    }else{
        document.cookie = "uuid=" + response.result + "; max-age=" + "3153600000"; // on met le cookie de connexion pour 100ans
        window.location.href = "/parcourVelo" // redirection vers parcourVelo
    }
}

function popUp(textToAdd){
    const popUp = document.getElementById('popUp');
    var popUpText = document.getElementById('popUpText')

    // Afficher le pop-up
    popUp.classList.remove('hidden');
    popUpText.textContent = textToAdd;
    
    // Attendre 5 secondes puis cacher le pop-up en fondu
    setTimeout(function() {
        popUp.classList.add('hidden');
    }, 5000);
}