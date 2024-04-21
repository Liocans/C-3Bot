$(document).ready(function() {
    $.ajax({
        type: "GET",
        url: "/load_intents", // Assume this endpoint now returns JSON string directly
    }).done(function(jsonString) {
        // Parse the JSON string received from the server
        var data = JSON.parse(jsonString);

        // Iterate over each intent in the intents array
        $.each(data.intents, function(key, intent) {
            // For each intent, create a new row in the table
            var newRow = $("<tr></tr>");
            newRow.append("<td class='w-25'>" + intent.tag + "</td>");

            // Convert patterns array into an unordered list
            var patternsList = $("<ul></ul>");
            $.each(intent.patterns, function(i, pattern) {
                patternsList.append("<li>" + pattern + "</li>");
            });
            newRow.append($("<td class='w-25'></td>").append(patternsList));

            // Convert responses array into an unordered list
            var responsesList = $("<ul></ul>");
            $.each(intent.responses, function(i, response) {
                responsesList.append("<li>" + response + "</li>");
            });
            newRow.append($("<td class='w-25'></td>").append(responsesList));

            // If there's a function associated, add it, otherwise just an empty cell
            newRow.append("<td class='w-25'>" + (intent.function ? intent.function : "None") + "</td>");

            // Append the new row to the table
            $(".intent_table tbody").append(newRow);
        });
    });
});
