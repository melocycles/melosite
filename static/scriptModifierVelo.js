        // déclaration à la racine car utilisé à plusieurs endroits

    let requiredFields
    let listeAttributes
    fetchData("api/config", {}, getConfig) 


    var photoList = [];
    var memoire = {};
    // récupération du bikeId
    const bikeId = parseInt(sessionStorage.getItem("bikeId"));
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
            const missingFields = requiredFields.filter(field => !document.getElementById(field).value); // vérfie que les 4 requiredFields ne sont pas vides

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
                updateBike(); // envoie les donnés renseigné à la database
            }
        });
    });

    function getConfig(returnFromFetch){
        const returnFromFetchArray = Object.entries(returnFromFetch);
        returnFromFetchArray.sort((a, b) => a[1].order - b[1].order);
        objects = Object.fromEntries(returnFromFetchArray);

        requiredFields = Object.keys(objects).filter(key => objects[key].addRequired);
        listeAttributes = Object.keys(objects).filter(key => objects[key].addBike);

        addField()
    }


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
                }else if (element.type === 'date' && attribute[1] !== null) {
                    // Formater la date au format YYYY-MM-DD
                    const formattedDate = new Date(attribute[1]).toISOString().split('T')[0];
                    memoire[attribute[0]] = formattedDate  
                    element.value = formattedDate;
                }else if (attribute[0].includes("photo")) {
                    photoList.push(attribute[1]);
                }else {
                    element.value = booltoFrench(attribute[1]);
                    }
            }
            
        })
        addPicture(photoList)
    }


    /* Envoie les nouvelles valeures au backend pour les enregistrer
    */
    function updateBike(){
        var formData = {"id" : bikeId}; // crée le dictionnaire à envoyer à sqlCRUD.py
        
            // vérifie si les photos dans les <img> de l'html sont différentes de celles de la mémoire
        for (let i = 0; i < photoList.length; i++) { 
            if (photoList[i] !== null && memoire[`photo${i + 1}`] != photoList[i]) {
                formData[`photo${i + 1}`] = photoList[i]; // si elles sont différentes on les ajoute aux donnés à update
            }
        }
        formData["benevole"] = document.getElementById("benevole").value

            // ajouts des attributs ayant été modifié au dictionnaire formData. On vérifie si un élément à été modifié dans hasTheValueChange()
        for (const attribute of listeAttributes) { // parcourt tous les ellements du formulaire
                if(attribute == "electrique"){ // si l'attribut est ellectrique on le transforme en boolean
                    //hasTheValueChange(attribute, booltoFrench(document.getElementById(attribute).value))
                    hasTheValueChange(attribute, frenchToBool(document.getElementById(attribute).value)); // on assigne à l'attribut sa valeur 
                } else if(attribute == "valeur"){ // si l'attribut est valeur on le transforme en float
                    hasTheValueChange(attribute, parseFloat(document.getElementById(attribute).value))

                }else{ // sinon on l'ajoute jsute (string)
                    hasTheValueChange(attribute, document.getElementById(attribute).value); // on assigne à l'attribut sa valeur 
                }
        }
        
        // Envoie des données au backend
        fetchData('/api/modifyBike', formData, window.location.href = "/velo")

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
                    if(file.name.endsWith(".heic") || file.name.endsWith(".heif")){
                        // get image as blob url
                        let blobURL = URL.createObjectURL(file);
                        
                        // convert "fetch" the new blob url
                        let blobRes = fetch(blobURL).then(res=>{return res.blob()})
                        .then(blob=>{return heic2any({blob})})
                        .then(imageBlob => {displayPicture(new File([imageBlob], file.name.split(".")[0]+".png"), canvasButton,index)})
                        console.log(file.name.split(".")[0]+".png")
                    }       
                    else{ // on vérifie que le téléphonne nous a bien envoyé une photo
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
                // on récupère le binaire de la photo puis on la stock dans photoList
                // const imageData = loadedImage.target.result;
                // photoList[index - 1] = imageData;
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
                    photoList[index - 1] = img.src
                    const context = canvas.getContext('2d');
                    context.drawImage(img, 0, 0, img.width*ratio, img.height*ratio); // on affiche l'image dans le canvas
                };
            };
        }
    }

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
                option.setAttribute("value", booltoFrench(item));
                option.textContent = booltoFrench(item)
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
