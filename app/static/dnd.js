// Append the message to chat history.
function appendMessage(message) {
    $('#chat-history').append('<p>' + message.role + ': ' + message.content + '</p>');
}

// Start the game when the 'start-play-btn' is clicked.
$('.start-play-btn').click(function () {
    $.ajax({
        url: '/start',
        type: 'POST',
        contentType: 'application/json',
        success: function (data) {
            appendMessage({role: 'assistant', content: data});
        }
    });
});

// Send the message when the 'send-btn' is clicked.
$('#send-btn').click(function () {
    var prompt = $('#chat-input').val();
    $('#chat-input').val('');
    appendMessage({role: 'user', content: prompt});
    $.ajax({
        url: '/message',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({prompt: prompt}),
        success: function (data) {
            appendMessage({role: 'assistant', content: data});
        }
    });
});

// Send the message when the 'Enter' key is pressed in the chat-input field.
$('#chat-input').keydown(function(event) {
    if (event.keyCode === 13 && !event.shiftKey) {
        event.preventDefault();
        $('#send-btn').click();
    }
});