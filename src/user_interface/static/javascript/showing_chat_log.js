			$(document).ready(function() {
				$("#messageArea").on("submit", function(event) {
					event.preventDefault(); // Prevent form submission
					const date = new Date();
					const hour = date.getHours();
					const minute = date.getMinutes();
					const str_time = hour + ":" + minute;
					var rawText = $("#text").val();

					var userHtml = '<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send">' + rawText + '<span class="msg_time">' + str_time + '</span></div> <div class="img_cont_msg"><img src="https://i.ibb.co/d5b84Xw/Untitled-design.png" class="rounded-circle user_img_msg"> </div></div>';
					$("#text").val("");
					$("#messageFormeight").append(userHtml);

					$.ajax({
						data: {
							msg: rawText,
						},
						type: "POST",
						url: "/get",
					}).done(function(data) {
						const botHtmlStart = '<div class="d-flex justify-content-start mb-4"> <div class="img_cont_msg"> <img src="https://i.ibb.co/fSNP7Rz/icons8-chatgpt-512.png" class="rounded-circle user_img_msg"> </div> <div class="msg_cotainer">';
						const botHtmlEnd = '<span class="msg_time">' + str_time + '</span></div></div>';

						// Append the starting HTML
						$("#messageFormeight").append($.parseHTML(botHtmlStart));

						// Select the last message container for appending the response
						var $lastMsgContainer = $("#messageFormeight").children().last().find(".msg_cotainer");

						// Function to simulate typing effect
						function typeMessage(message, index) {
							if (index < message.length) {
								$lastMsgContainer.append(message[index]);
								setTimeout(function() {
									typeMessage(message, index + 1);
								}, 30); // Adjust typing speed here
							} else {
								// Append the time after the message is complete
								$lastMsgContainer.append(botHtmlEnd);
							}
						}

						// Start typing the message
						typeMessage(data, 0);
					});
				});
			});