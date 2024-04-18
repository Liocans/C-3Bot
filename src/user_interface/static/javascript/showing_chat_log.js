$(document).ready(function() {
    $("#messageArea").on("submit", function(event) {
        event.preventDefault(); // Prevent form submission
        const date = new Date();
        const hour = date.getHours();
        const minute = date.getMinutes();
        const str_time = hour + ":" + minute;
        var rawText = $("#message_text").val();
        var htmlText = rawText
        // Temporarily replace code blocks with placeholders
        const codeBlocks = [];
        const placeholder = "%%%CODE_BLOCK%%%";
        htmlText = htmlText.replace(/```(.*?)\n(.*?)```/gs, function(match, p1, p2) {
            codeBlocks.push(p2);
            return placeholder;
        });

        // Replace newlines in the rest of the text with HTML line breaks
        htmlText = htmlText.replace(/\n/g, '<br>');
        // Reinsert code blocks with proper HTML formatting
        htmlText = htmlText.replace(new RegExp(placeholder, 'g'), function() {
            const code = codeBlocks.shift(); // Get the first element from the codeBlocks array
            const lines = code.split('\n'); // Split the code into individual lines
            let formattedCode = ''; // Initialize a variable to store the formatted code
            // Wrap each line in <code> tags and append it to the formattedCode variable
            lines.forEach(line => {
                formattedCode += '<code>' + line.replace(/</g, '&lt;').replace(/>/g, '&gt;') + '</code><br>';
            });
            return '<pre>' + formattedCode + '</pre>'; // Wrap the entire code block in <pre> tags
        });

        var userHtml = '<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send">' + htmlText + '<span class="msg_time">' + str_time + '</span></div> <div class="img_cont_msg"><img src="https://i.ibb.co/d5b84Xw/Untitled-design.png" class="rounded-circle user_img_msg"> </div></div>';
        $("#message_text").val("");
        $("#messageFormeight").append(userHtml);
        document.getElementById('message_text').dispatchEvent(new Event("input"));

        $.ajax({
            data: {
                msg: rawText,
            }, 
            type: "POST",
            url: "/get_response",
        }).done(function(data) {
            const botHtmlStart = '<div class="d-flex justify-content-start mb-4"> <div class="img_cont_msg"> <img src='+window.static_logo+' class="rounded-circle user_img_msg"> </div> <div class="msg_cotainer">';
            const botHtmlEnd = '<span class="msg_time">' + str_time + '</span></div></div>';

            // Append the starting HTML
            $("#messageFormeight").append($.parseHTML(botHtmlStart));

            // Select the last message container for appending the response
            var $lastMsgContainer = $("#messageFormeight").children().last().find(".msg_cotainer");

            // Function to simulate typing effect
            function typeMessage(message) {
                return new Promise((resolve) => {
                    function typeChar(index) {
                        if (index < message.length) {
                            $lastMsgContainer.append(message[index]);
                            setTimeout(() => typeChar(index + 1), 40); // Adjust typing speed here
                        } else {
                            resolve(); // Resolve the promise once the message is fully typed
                        }
                    }
                    typeChar(0);
                });
            }

            async function typeAllMessages(data) {
                for (const item of data) {
                    if (!Array.isArray(item)) {
                        await typeMessage(item); // Wait for each message to be typed out before continuing
                    } else {
                        $lastMsgContainer.append("<br>");
                        await typeMessage(item[0]);
                        let listHtml = "<ul>";
                        for (const item_error of item[1]) {
                            listHtml += "<li>";
                            listHtml += item_error;
                            listHtml += "</li>";
                        }
                        listHtml += "</ul><br>";
                        $lastMsgContainer.append(listHtml);
                    }
                }
                $lastMsgContainer.append(botHtmlEnd);
            }


            typeAllMessages(data);
        });
    });
});