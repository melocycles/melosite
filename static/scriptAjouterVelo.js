    // déclaration à la racine car utilisé à plusieurs endroits.
    let requiredFields
    let allAttributes
        
    // C'est là que seront stocké les photos prises. On les stock dans une liste pour y accéder plus simplement
    
    // récupération des canvas où seront affichés les photos sur la page  
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
            addBike()
        });

    }, false);

    /* ajoute le vélo à la base de donné
            est appelé par le boutton valider    
        */
    function addBike(){
        var formData = {}; // on définit le vélo comme en stock de base
    
        // on parcourt les 3 photos dans photoList. Si une photo a été prise on l'ajoute dans formData
        for (let i = 0; i < photoList.length; i++) {
            if (photoList[i] !== null) {
                formData[`picture${i + 1}`] = photoList[i].src;
            }
        }
        // crée le dictionnaire à envoyer à sqlCRUD.py
        for (const attribute of listeAttributes) { // parcourt tous les ellements qui peuvent être rensignés
    
            if (document.getElementById(attribute).value !== "") { // si l'utilisateur a renseigné une valeur            
                if(attribute == "valeur"){ // si l'attribut est valeur on le transforme en float (aka nombre à virgules)
                    formData[attribute] = parseInt(document.getElementById(attribute).value)
    
                }else if(attribute == "dateEntre"){ // si l'attribut est la date on la formate
                    let dateValue = new Date(document.getElementById(attribute).value);
                    const formattedDate = new Date(dateValue).toISOString().split('T')[0]; // formate sous la forme yyyy-mm-dd
                    formData[attribute] = formattedDate
                    
                }else{ // sinon on l'ajoute sans avoir à la préparer (car c'est une string (aka chaine de caractère))
                    formData[attribute] = frenchToBool(document.getElementById(attribute).value); // on assigne à l'attribut sa valeur 
                }
            }
        }
1
        // envoi deu formulaire au backend pour l'enregistrement dans la database pui redirection vers la apge parcoursVelo
        fetchData('/api/addBike', formData, window.location.href = '/ajouterVelo');
    };