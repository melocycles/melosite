document.addEventListener("DOMContentLoaded", function () { // ci dessous est effectué au chargement de la page
    const returnButton = document.getElementById('returnButton');
    const submitButton = document.getElementById("submitButton");
    const form = document.getElementById('form');
    const listCheckBox = [document.getElementById("enStock"),document.getElementById("réservé"),document.getElementById("vendu"),document.getElementById("donné"),document.getElementById("recyclé"),document.getElementById("perduVolé")]
    var checkBoxToSend = []

    form.addEventListener('submit', function (event) {
        event.preventDefault(); // empeche que clicker sur un bouton du formulaire redirige vers une page
    });

    returnButton.addEventListener('click', function () { // boutton Retour
        window.location.href = "/"; // retourne à la page parcourVelo
    });

    submitButton.addEventListener('click', function () { // bouton envoyer
            // récupération des valeurs du formulaire
        const inStartDate = document.getElementById("inStartDateInput").value;
        const inEndDate = document.getElementById("inEndDateInput").value;
        const outStartDate =  document.getElementById("outStartDateInput").value;
        const outEndDate =  document.getElementById("outEndDateInput").value;

        checkBoxToSend = [] // remise à zéro de la liste qui contient les valeurs du status des vélos
        if (inStartDate || inEndDate || outStartDate || outEndDate) { // si au moins un élément est renseigné
            for (var element of listCheckBox){
                if(element.checked){
                    checkBoxToSend.push(element.value)
                }
            }
            fetchData("/api/getBikeOut", {"inStartDate" : inStartDate, "inEndDate" : inEndDate, "outStartDate" : outStartDate, "outEndDate" : outEndDate, "bikeStatus" : checkBoxToSend}, downloadCsv); // envoie les donnés à la database
        } 
    });

})

function downloadCsv(data){
    for (var i = 1; i < data.csv.length; i++) { // on parcourt l'object json saufla 1ere ligne (la 1ere ligne est le nom des colonnes)
        data.csv[i][1] = new Date().toISOString().split('T')[0]; // on formate la date en yyyy-mm-dd 
    }
    
    const csvContent = data.csv.map(row => row.join(',')).join('\n'); // on csvise les donnés
    
    var csvToDownload = new Blob([csvContent], {type:'text/csv'}) // Crée un objet Blob contenant les données CSV avec le type MIME 'text/csv'

    var downloadButton = document.getElementById("downloadButton");
    downloadButton.style.display = "block"

    downloadButton.href = URL.createObjectURL(csvToDownload); // met le fichier en lien de téléchargement sur le boutton
    downloadButton.download = "veloExport.csv"; // définit le nom du csv

    downloadButton.addEventListener("click", function(){
        var downloadLink = document.createElement("a");
        downloadLink.href = URL.createObjectURL(csvToDownload);
        downloadLink.download = "file.csv";
        downloadLink.click();
    })
}