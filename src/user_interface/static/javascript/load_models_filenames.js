$(document).ready(function() {
    $.ajax({
        type: "GET",
        url: "/load_models_filenames", // Assume this endpoint now returns JSON string directly
    }).done(function(jsonString) {
        var select = $('#model');
        select.empty(); // Clear the old options
        jsonString.forEach(function(file) {
            select.append($('<option></option>').attr('value', file).text(file));
        });
    });
});