$(document).ready(function() {
    $("#modelArea").on("submit", function(event) {
        event.preventDefault();
        var selectedModel = $("#model").val();
        $.ajax({
            data: {
                filename: selectedModel,
            },
            type: "POST",
            url: "/test_chatbot",
        }).done(function(data) {

        });
    });
});