$(document).ready(function() {
    $.ajax({
        type: "GET",
        url: "/get_models", // Assume this endpoint now returns JSON string directly
    }).done(function(jsonString) {
        // Parse the JSON string received from the server
        var data = JSON.parse(jsonString);
        // Iterate over each intent in the intents array
        $.each(data.models, function(key, model) {
            // For each intent, create a new row in the table
            var newRow = $("<tr></tr>");
            newRow.append("<td class='w-10'>" + model.name + "</td>");

            $.each(model.parameters, function(key, parameter) {
                if(typeof parameter == "boolean"){
                    parameter = parameter ? "YES":"NO"
                }
                newRow.append($("<td class='w-10'>"+  parameter +"</td>"))
            });
            newRow.append($("<td class='w-10'>"+  model.status +"</td>"))
            // Append the new row to the table
            $(".intent_table tbody").append(newRow);
        });
    });
});