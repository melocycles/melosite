//  gère la page de logIn et de logOut. On vérifie quelle page c'est en fonction de l'éxistence du boutton de connection

document.addEventListener('DOMContentLoaded', function () { // au chargement de la page

    const returnButton = document.getElementById('returnButton');
    returnButton.addEventListener('click', function() { // bouton retour
        window.location.href = "/"; // retourne à la page du vélo
    });


        // si le boutton connection  éxiste (aka l'utilisateur est déconnecté) page logIn
    if(document.getElementById("connectButton")){ 
        const connectButton = document.getElementById("connectButton")
        const userNameField = document.getElementById("username")
        const passwordField = document.getElementById("password")
        const showPasswordButton = document.getElementById("showPassword")
        const form = document.getElementById("form")

        form.addEventListener('submit', function (event) {
            event.preventDefault(); // empeche que clicker sur un bouton du formulaire redirige vers une page
        });
        
        connectButton.addEventListener("click", function(){ // boutton connection 
            const formData = {"userName" : userNameField.value, "password" : passwordField.value} // ajout des valeurs du formulaires au formData, envoyé ensuite au backend
            fetchData("/api/logIn", formData, processResponse) // envoie des donnés au backend puis on le traite
        });   
        
        showPasswordButton.addEventListener("click", function(){  
            if (passwordField.type === "password") {
                passwordField.type = "text";
            } else {
                passwordField.type = "password";
            }
        })
    }
    
        // si le boutton connection n'éxiste pas (aka l'utilisateur est connecté) page logOut
    else{ 

        if(document.getElementById('disconnectButton')){ // boutton déconnection
            const disconnectButton = document.getElementById('disconnectButton');
            disconnectButton.addEventListener('click', function() { // bouton déconnection
                document.cookie = "uuid=; expires=Thu, 10 Mai 1896 06:06:18 UTC; path=/;"; // on retire le cookie (en définissant sa date d'expiration dans le passé)
                window.location.href = "/"; // redirection vers la page parcourVelo
                });
            }
        }
        


});


    

function processResponse(response){
    if (response.result == "mauvaise combinaison username/mot de passe"){ // si la combinaison est mauvaise on affiche le popUp d'erreur
        popUp(response.result)
    }else{
        document.cookie = "uuid=" + response.result + "; max-age=" + "3153600000"; // on met le cookie de connexion pour 100ans
        window.location.href = "/" // redirection vers parcourVelo
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