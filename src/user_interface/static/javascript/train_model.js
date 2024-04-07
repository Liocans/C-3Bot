$(document).ready(function() {
    $("#modelArea").on("submit", function(event) {
        event.preventDefault();
        var formData = JSON.stringify($("#modelArea").serializeArray());
        $.ajax({
            data: {
                data_forms: formData,
            },
            type: "POST",
            url: "/train_model",
        }).done(function(data) {

        });
    });
});