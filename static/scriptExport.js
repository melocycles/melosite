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
        const outStartDate =  document.getElementById("outStartDateInput").value;
        const outEndDate =  document.getElementById("outEndDateInput").value;

        checkBoxToSend = [] // remise à zéro de la liste qui contient les valeurs du status des vélos
        if (outStartDate || outEndDate) { // si au moins un élément est renseigné
            for (var element of listCheckBox){
                if(element.checked){
                    checkBoxToSend.push(element.value)
                }
            }
            fetchData("/api/getBikeOut", {"outStartDate" : outStartDate, "outEndDate" : outEndDate, "bikeStatus" : checkBoxToSend}, downloadCsv); // envoie les donnés à la database
        } 
    });

})


function downloadCsv(data){
    qt csvContent = data.csv.map(row => row.join(',')).join('\n'); // on csvise les donnés
    
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