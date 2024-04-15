$(document).ready(function() {
    $("#messageArea").on("submit", function(event) {
        event.preventDefault(); // Prevent form submission
        const date = new Date();
        const hour = date.getHours();
        const minute = date.getMinutes();
        const str_time = hour + ":" + minute;
        var rawText = $("#message_text").val();

        var userHtml = '<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send">' + rawText + '<span class="msg_time">' + str_time + '</span></div> <div class="img_cont_msg"><img src="https://i.ibb.co/d5b84Xw/Untitled-design.png" class="rounded-circle user_img_msg"> </div></div>';
        $("#message_text").val("");
        $("#messageFormeight").append(userHtml);

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
                            $lastMsgContainer.append(" ");
                            resolve(); // Resolve the promise once the message is fully typed
                        }
                    }
                    typeChar(0);
                });
            }

            async function typeAllMessages(data) {
                for (const item of data) {
                    await typeMessage(item); // Wait for each message to be typed out before continuing
                }
                $lastMsgContainer.append(botHtmlEnd);
            }

            typeAllMessages(data);

        });
    });
});