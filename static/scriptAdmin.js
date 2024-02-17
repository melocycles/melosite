document.addEventListener("DOMContentLoaded", function () { // ci dessous est effectué au chargement de la page
    const bikeButton = document.getElementById('bikeButton');
    const exportButton = document.getElementById("exportButton")


    exportButton.addEventListener('click', function () { // boutton exporter
        window.location.href = "/export"; // redirige vers la page d'export
    });
})