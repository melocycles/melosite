let listeAttributes
let listeAttributesName
let listSelectName


fetchData("api/config", {}, getConfig) 
const addSelectValueButton = document.getElementById("addSelectValueButton")
const addSelectValueSection = document.getElementById("addSelectValueSection")
const addAColumnButton = document.getElementById("addAColumnButton")
const addAColumnSection = document.getElementById("addAColumnSection")
const modifyAColumnButton = document.getElementById("modifyAColumnButton")
const modifyAColumnSection = document.getElementById('modifyAColumnSection')
const listDisplayableElement = [addSelectValueSection, addAColumnSection, modifyAColumnSection]

addSelectValueButton.addEventListener("click", function(event){
    for (let element of listDisplayableElement) {
        if (element.style.display !== "none") {
            element.style.display = "none";
        }
    }
    addSelectValueSection.style.display = "inline"
    fillSelect()
})

addAColumnButton.addEventListener("click", function(event){
    for (let element of listDisplayableElement) {
        if (element.style.display !== "none") {
            element.style.display = "none";
        }
    }
    addAColumnSection.style.display = "inline"
    createForm()
})

modifyAColumnButton.addEventListener("click", function(event){
    for (let element of listDisplayableElement) {
        if (element.style.display !== "none") {
            element.style.display = "none";
        }
    }
    modifyAColumnSection.style.display = "inline"
    createListColumn()
})


function getConfig(returnFromFetch){ // récupère les info de la varibale d'environement de config
    const returnFromFetchArray = Object.entries(returnFromFetch);
    returnFromFetchArray.sort((a, b) => a[1].order - b[1].order);
    listeAttributes = Object.fromEntries(returnFromFetchArray);

    listeAttributesName = Object.keys(listeAttributes);
    listSelectName = Object.keys(listeAttributes).filter(key => listeAttributes[key].entryType[0] === "select")
}

function addTextInput(formToAdd, name = ""){ // ajoute un élément textInput à la page
    var input = document.createElement('input');
    input.value = name
    input.className = "multiChoiceInput" + formToAdd.id
    formToAdd.appendChild(input)
}
function addButton(formToAdd){ // crès le boutton pour ajouter un textInput & gère les actions du boutton
    var button = document.createElement("button")
    button.innerHTML = "+"
    button.id = "addInputButton"    
    button.style.width = "40%"
    button.style.margin = "0.5rem auto"
    button.style.padding = "0.2rem 0"

    button.addEventListener("click", function(event){
        button.remove()
        addTextInput(formToAdd)
        addButton(formToAdd)
    })

    formToAdd.appendChild(button)
}


//#region Ajouter une valeur
const existingAttribut = document.getElementById("existingAttribut")
const topForm = document.getElementById("topForm")
topForm.addEventListener('submit', function (event) {
    event.preventDefault(); // empeche que clicker sur un bouton du formulaire redirige vers une page
});
const addAttributButton = document.getElementById("addAttribut")
addAttributButton.addEventListener('click', function (event) {
    bottomForm.innerHTML = ""; 
    editSelect(existingAttribut.value); // empeche que clicker sur un bouton du formulaire redirige vers une page
});
function fillSelect(){ // premier élément d'ajout de valeur de select
    for(i of listSelectName){
        var option = document.createElement('option');
        option.value = i;
        option.text = i;
        existingAttribut.appendChild(option);
        }
}

function editSelect(attributToEdit){ 
    

    const bottomForm = document.getElementById("bottomForm")
    const submitButtonFromAddValue = document.createElement("button")
    submitButtonFromAddValue.className = "submitButton"
    submitButtonFromAddValue.style.marginBottom = "1rem"
    submitButtonFromAddValue.innerHTML = "valider"
    bottomForm.appendChild(submitButtonFromAddValue)


    bottomForm.addEventListener('submit', function (event) {
        event.preventDefault(); // empeche que clicker sur un bouton du formulaire redirige vers une page
    });

    submitButtonFromAddValue.addEventListener("click", function(event){
        var listNewAttributes = []
        for (var i = 0; i < bottomForm.length; i++) {
            // Vérifier si l'élément est un champ de saisie
            if (bottomForm[i].type !== "input" && bottomForm[i].value !== "") {
              listNewAttributes.push(bottomForm[i].value)
            }
          }
          sendEditConfigFile(listNewAttributes)
    })


    for(i of listeAttributes[attributToEdit]["values"]){ // on crée déjà les premiers éléments avec les valeurs éxistantes
        addTextInput(bottomForm, i)
    }

    addButton(bottomForm)

}
//#endregion

//#region Ajouter colonne
const addForm = document.getElementById("addForm")
const entryTypeDiv = document.getElementById("entryTypeDiv")
const submitAddAColumn = document.getElementById("submitAddAColumn")

addForm.addEventListener('submit', function (event) {
    event.preventDefault(); // empeche que clicker sur un bouton du formulaire redirige vers une page
});

submitAddAColumn.addEventListener('click', function(event){
    function toCamelCase(word){
        // Diviser la phrase en mots
        var mots = word.split(' ');
        
        // Convertir chaque mot en minuscules sauf le premier
        for (var i = 1; i < mots.length; i++) {
            mots[i] = mots[i].charAt(0).toUpperCase() + mots[i].slice(1);
        }
        
        // Concaténer les mots pour former le résultat
        var resultat = mots.join('');
        
        return resultat;
        }

    function toLowCase(word){
        // Diviser la phrase en mots
        word = word.toLowerCase()
        var mots = word.split(' ');        
        return mots.join('');
    }
    
    dictOftype = {'["input", "text"]' : "str", '["textarea", ""]' : "str", '["select", ""]' : "str", '["input", "number"]' : "int", '["input", "date"]' : "str"}
    var name = document.getElementById("name").value
    var entryTypeSelect = document.getElementById("entryTypeSelect").value
    var global= document.getElementById("global").checked
    var detail= document.getElementById("detail").checked
    var filter= document.getElementById("filter").checked
    var addRequired= document.getElementById("addRequired").checked
    var inputs = document.querySelectorAll('.multiChoiceInputinputDiv');
    values = []

    inputs.forEach(function(input) {
        values.push(input.value);
    });

    jsonToREturn = {
    "type" : dictOftype[entryTypeSelect], 
    "len" : 0,
    "global" : global,
    "detail" : detail,
    "search" : false,
    "title" : false,
    "filter" : filter,
    "addRequired" : addRequired,
    "addBike" : true,
    "withSpace" : name,
    "lowCase" : toLowCase(name),
    "camelCase" : toCamelCase(name),
    "values" : values,
    "edit" : true,
    "order" : "",
    "entryType" : JSON.parse(entryTypeSelect)
    }
    sendEditConfigFile(jsonToREturn)
});

function createForm(){
    var entryTypeSelect = document.getElementById("entryTypeSelect");

    // Écoutez l'événement de changement sur le menu déroulant
    entryTypeSelect.addEventListener("change", function() {
        var selectedOption = entryTypeSelect.options[entryTypeSelect.selectedIndex];
        var selectedValue = selectedOption.value;

        var testInputDiv = document.getElementById("inputDiv")
        if(testInputDiv){testInputDiv.remove()}

        if (selectedValue === '["select", ""]') {
            var inputDiv = document.createElement("div")
            inputDiv.id = "inputDiv"
            inputDiv.className = "addTextInput"
            entryTypeDiv.parentNode.insertBefore(inputDiv, entryTypeDiv.nextSibling);
            addTextInput(inputDiv)
            addTextInput(inputDiv)
            addButton(inputDiv)
        }
});
    dictNewColumnAttributes = {
        "name" : "",
        "type" : ["str", "bytes", "bool", "int"], 
        "len" : "none",
        "global" : Boolean,
        "detail" : Boolean,
        "search" : Boolean,
        "title" : Boolean,
        "filter" : Boolean,
        "addRequired" : Boolean,
        "addBike" : Boolean,
        "withSpace" : "",
        "lowCase" : "",
        "camelCase" : "",
        "values" : [],
        "edit" : Boolean,
        "order" : "none",
        "entryType" : []
    }
    listNewColumnAttributesName = ["type","len","global","detail","search","title","filter","addRequired","addBike","withSpace","lowCase","camelCase","values","edit","order","entryType"]
    }
    

//#endregion

//#region modifier colonne ?a supprimer?
function createListColumn(){
    modifyAColumnSection.innerHTML =  "<h4>Modifier une colonne</h4>"
    const dictColumnType = {
        "texte court" : {
            "postgreName" : "VARCHAR",
            "secondEntry" : true,
            "secondEntryType" : "number",
            "secondentryLabel" : "nombre de caractères max"
        },
        "texte long" : {
            "postgreName" : "TEXT",
            "secondEntry" : false,
            "secondEntryType" : "",
            "secondentryLabel" : ""
        },
        "date" : {
            "postgreName" : "DATE",
            "secondEntry" : false,
            "secondEntryType" : "",
            "secondentryLabel" : ""
        },
        "ouinon" : {
            "postgreName" : "BOOLEAN",
            "secondEntry" : false,
            "secondEntryType" : "",
            "secondentryLabel" : ""
        },
        "nombre" : {
            "postgreName" : "INTEGER",
            "secondEntry" : false,
            "secondEntryType" : "",
            "secondentryLabel" : ""
        },
    }

    for(currentAttribute of listeAttributesName){
        var parentDiv = document.createElement("div")
        parentDiv.classList.add("parentDiv")
    
        var columnName = document.createElement("input")
        columnName.value = currentAttribute
        columnName.style.marginLeft = "1rem"

        var columnType = document.createElement("select")
        columnType.style.marginLeft = "1rem"

        for(currentColumnType in dictColumnType){
            var option = document.createElement('option');
            option.value = dictColumnType[currentColumnType]["postgreName"];
            option.text = currentColumnType;
            columnType.appendChild(option);
        }

        modifyAColumnSection.appendChild(parentDiv)
        parentDiv.appendChild(columnName)
        parentDiv.appendChild(columnType)
    }

    const submitButtonFromModifyColumn = document.createElement("button")
    submitButtonFromModifyColumn.innerHTML = "confirmer"
    submitButtonFromModifyColumn.style.margin = "1rem"
    submitButtonFromModifyColumn.style.marginLeft = "2rem"

    modifyAColumnSection.appendChild(submitButtonFromModifyColumn)

    submitButtonFromModifyColumn.addEventListener("click", function(event){
        var columnNameAndType = {}
        for (var i = 0; i < modifyAColumnSection.children.length; i++) {
            var currentParentdiv = modifyAColumnSection.children[i]
            // Vérifier si l'élément est un champ de saisie
            if(currentParentdiv.tagName !== "H4" && currentParentdiv.value !== ""){
              columnNameAndType[currentParentdiv.children[0].value] = currentParentdiv.children[1].value
            }
        }

        console.log(columnNameAndType)  

    })
}
//#endregion


//#region edit config file
function sendEditConfigFile(jsonObject){
    function callbackTest(){}

    fetchData('/api/editConfigFile', jsonObject, callbackTest)
}
//#endregion
