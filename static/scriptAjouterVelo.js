    // déclaration à la racine car utilisé à plusieurs endroits.
    let requiredFields
    let listeAttributes
    let allAttributes
    fetchData("api/config", {}, getConfig) 
        
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
            const missingFields = requiredFields.filter(field => !document.getElementById(field).value);
            
            const inDateEntry = document.getElementById("dateEntre").value
            const outDateEntry = document.getElementById("dateSortie").value
            const stautVeloEntry = document.getElementById("statutVelo").value
            const listOfOutReason = ["vendu", "donné", "démonté", "recyclé", "perdu"]
            const listOfInReason = ["en stock","réservé"]
            
            if (outDateEntry === "" && listOfOutReason.includes(stautVeloEntry)){
                window.alert("une date de sortie doit être renseigné avec le statut " + stautVeloEntry);
            }else if (outDateEntry !== "" && listOfInReason.includes(stautVeloEntry)){
                window.alert("la date de sortie ne peut pas être précisé avec le statut " + stautVeloEntry);
            }else if (outDateEntry !== "" && outDateEntry < inDateEntry){
                window.alert("la date de sortie est posterieur à la date d'entrée")
            }
            else if (missingFields.length == 0) { // si il ne manque pas de donné nécessaire
                addBike(); // envoie les donnés à la database
            } 
        });
    
    
            // affichage des logos 
    

    


        
            // dessine les logos dans les canvas image

    
    
            // gestion de la prise des photos
    
        
    
    }, false);
    
    function getConfig(returnFromFetch){
        const returnFromFetchArray = Object.entries(returnFromFetch);
        returnFromFetchArray.sort((a, b) => a[1].order - b[1].order);
        objects = Object.fromEntries(returnFromFetchArray);
    
        requiredFields = Object.keys(objects).filter(key => objects[key].addRequired);
        listeAttributes = Object.keys(objects).filter(key => objects[key].addBike)
    
        addField()
    }
    
    
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
        console.log(formData)
        // envoi deu formulaire au backend pour l'enregistrement dans la database pui redirection vers la apge parcoursVelo
        fetchData('/api/addBike', formData, window.location.href = '/parcourVelo');
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