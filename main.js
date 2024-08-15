$(document).ready(function () {
    // Event listener for the send button
    $('#send_button').on('click', function (e) {
        e.preventDefault();
        let userMessage = $('#msg_input').val().trim();
        
        if (userMessage !== "") {
            // Display the user message
            showUserMessage(userMessage);
            $('#msg_input').val('');

            // Send the message to the backend
            $.ajax({
                url: 'http://127.0.0.1:5000/chat',  // Correct endpoint for backend
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ "message": userMessage }),
                success: function (response) {
                    // Display the bot's response
                    showBotMessage(response.reply);
                },
                error: function (xhr, status, error) {
                    // Handle errors
                    showBotMessage("Sorry, I couldn't process your request.");
                }
            });
        }
    });

    // Handle pressing "Enter" key
    $('#msg_input').keydown(function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            $('#send_button').click();
        }
    });
});

// Function to display user messages
function showUserMessage(message) {
    renderMessageToScreen({
        text: message,
        message_side: 'right',
    });
}

// Function to display bot messages
function showBotMessage(message) {
    renderMessageToScreen({
        text: message,
        message_side: 'left',
        is_html: true  // Add this flag to indicate that HTML should be rendered
    });
}

// Function to render messages to the screen
function renderMessageToScreen(args) {
    let displayDate = (new Date()).toLocaleString('en-IN', {
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
    });
    let messagesContainer = $('.messages');

    // Create message element
    let message = $(`
        <li class="message ${args.message_side}">
            <div class="avatar"></div>
            <div class="text_wrapper">
                <div class="text">${args.is_html ? args.text : $('<div/>').text(args.text).html()}</div>
                <div class="timestamp">${displayDate}</div>
            </div>
        </li>
    `);

    // Append to message container
    messagesContainer.append(message);

    // Add animations
    setTimeout(function () {
        message.addClass('appeared');
    }, 0);
    messagesContainer.animate({ scrollTop: messagesContainer.prop('scrollHeight') }, 300);
}
