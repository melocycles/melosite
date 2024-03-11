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
    if(value == true){return "oui"}
    else if(value == false){return "non"}
    else{return value}
}

function frenchToBool(value){
    // transforme oui/non en bool pour l'enregistrement dans la db
    if(value == "oui"){return true}
    else if(value == "non"){return false}
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