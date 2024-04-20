// script.js
document.addEventListener('DOMContentLoaded', function () {
    var taillePopulationContainer = document.getElementById('taillePopulationContainer');
    var nbrGenerationsContainer = document.getElementById('nbrGenerationsContainer');
    var tauxMutationContainer = document.getElementById('tauxMutationContainer');
    var nbrFourmisContainer = document.getElementById('nbrFourmisContainer');

    var radioButtons = document.querySelectorAll('input[name="algorithme"]');

    radioButtons.forEach(function (radioButton) {
        radioButton.addEventListener('change', function () {
            if (this.value === 'genetique') {
                // Afficher les champs spécifiques à l'algorithme génétique
                taillePopulationContainer.style.display = 'flex';
                nbrGenerationsContainer.style.display = 'flex';
                tauxMutationContainer.style.display = 'flex';
                nbrFourmisContainer.style.display = 'none';
            } else if (this.value === 'Algo_Fourmis') {
                // Afficher les champs spécifiques à l'algorithme des loups gris
                taillePopulationContainer.style.display = 'none';
                nbrGenerationsContainer.style.display = 'none';
                tauxMutationContainer.style.display = 'none';
                nbrFourmisContainer.style.display = 'flex';
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    // Récupérer le bouton et ajouter un gestionnaire d'événements
    const commencerBtn = document.getElementById('commencerBtn');
    commencerBtn.addEventListener('click', function () {
        // Récupérer les valeurs des champs
        const capaciteBin = parseInt(document.getElementById('capacité-bin').value);
        const dimensionsObjets = JSON.parse(document.getElementById('dimensions').value).map(Number);

        // Récupérer la valeur de l'algorithme sélectionné
        const algorithmeSelectionne = document.querySelector('input[name="algorithme"]:checked').id;
        let parametres = {};

        if (algorithmeSelectionne === 'genetique') {
            parametres.taillePopulation = parseInt(document.getElementById('Taille population').value);
            parametres.nbrGenerations = parseInt(document.getElementById('Nombres générations').value);
            parametres.tauxMutation = parseFloat(document.getElementById('Taux mutation').value);
            console.log("Données envoyées au serveur :", parametres);
            console.log("Données envoyées au serveur :", dimensionsObjets);

        } else if (algorithmeSelectionne === 'Algo_Fourmis') {
            parametres.nombre_Fourmis = parseInt(document.getElementById('Nombres de fourmis').value);
            console.log("Données envoyées au serveur :", parametres);
            

        } else {
            console.error('Algorithme non pris en charge.');
            return;
        }

        fetch(`/run-algorithm/${algorithmeSelectionne}`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        capaciteBin: capaciteBin,
        dimensionsObjets: dimensionsObjets,
        parametres
    }),
})

        .then(response => response.json())
        .then(resultat => {
            // Vérifier si resultat.solution existe et est un tableau
            if (resultat.solution && Array.isArray(resultat.solution)) {
                // Afficher les résultats dans votre structure HTML
                const nbrElement = document.querySelector('.nbr-bin span');
                const affichage1Element = document.querySelector('.affichage1');
        
                // Afficher le nombre de boîtes utilisées dans le premier bloc
                nbrElement.textContent = `Nombre de bacs : ${resultat.nombre_boites_utilisees}`;
        
                // Vous devrez personnaliser cette partie selon le format de vos résultats
                // Par exemple, si resultat.solution contient un tableau de boîtes, vous pouvez le parcourir et l'afficher.
                /*resultat.solution.forEach((boite, index) => {
                    const boiteDiv = document.createElement('div');
                    boiteDiv.textContent = `Boîte ${index + 1}: [${boite.map(objet => objet[0]).join(', ')}]`;
                    affichage1Element.appendChild(boiteDiv);
                });*/
        
                // Afficher la disposition des objets dans le deuxième bloc
                const dispositionElement = document.querySelector('.disposition .affichage1 span');
                dispositionElement.textContent = `Liste des bins : \n${JSON.stringify(resultat.solution)}`;
        
                console.log(`Résultats de l'algorithme ${algorithmeSelectionne}:`, resultat);
            } else {
                console.error('Erreur lors de la récupération des résultats de l\'algorithme. La solution n\'est pas un tableau.');
            }
        })
        .catch(error => console.error('Erreur lors de l\'appel API:', error));
        
    });
});

function genererGraphe() {
    var image = document.getElementById('graphe');
    fetch('/generer_graphe')
        .then(response => {
            if (response.ok) {
                document.getElementById('graphe').src = '/graph_image';
            } else {
                console.error('Erreur lors de la génération du graphe');
            }
        })
        .catch(error => console.error('Erreur :', error));
        image.style.display = "block";
}

$(document).ready(function () {
    $("#enregistrer-db-btn").click(function (event) {
        event.preventDefault(); // Empêcher le comportement par défaut du lien

        // Récupérer les valeurs des champs de formulaire
        var nbrObjets = $("#nbr_objets").val();
        var capaciteBin = $("#capacite-bin").val();
        var dimensions = $("#dimensions").val();

        // Créer un objet contenant les données à envoyer
        var formData = {
            nbr_objets: nbrObjets,
            capacite_bin: capaciteBin,
            dimensions: dimensions
        };

        // Envoyer les données au serveur Flask via une requête AJAX
        $.ajax({
            type: "POST",
            url: "/enregistrer-donnees", // L'URL de la route Flask pour enregistrer les données
            data: formData, // Les données à envoyer au serveur
            success: function (response) {
                // Traiter la réponse du serveur si nécessaire
                console.log(response);
            },
            error: function (error) {
                // Gérer les erreurs
                console.error("Erreur lors de l'envoi des données :", error);
            }
        });
    });
});
