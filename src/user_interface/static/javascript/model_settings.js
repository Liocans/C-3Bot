$(document).ready(function() {
    // Fonction qui gère l'affichage des éléments basés sur le modèle sélectionné
    function toggleModelSettings() {
        var selectedModel = $('#modeling').val();

        if (selectedModel === 'BERT') {
            // Cacher les champs spécifiques lorsque BERT est sélectionné
            $('#preprocessor').closest('.col').hide();
            $('#features_extractor').closest('.col').hide();
            $('#hidden_size').closest('.col').hide();
            $('#withoutstopwords').closest('.col').hide();
        } else {
            // Afficher tous les champs lorsque NeuralNet ou d'autres modèles sont sélectionnés
            $('#preprocessor').closest('.col').show();
            $('#features_extractor').closest('.col').show();
            $('#hidden_size').closest('.col').show();
            $('#withoutstopwords').closest('.col').show();
        }
    }

    // Appel initial pour configurer l'affichage correct à la charge de la page
    toggleModelSettings();

    // Événement change lié au sélecteur de modèle
    $('#modeling').on('change', function() {
        toggleModelSettings();
    });
});
