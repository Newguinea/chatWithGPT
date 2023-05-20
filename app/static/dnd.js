function appendMessage(message) {
    $('#chat-history').append('<p>' + message.role + ': ' + message.content + '</p>');
}

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

$('#chat-input').keydown(function(event) {
    if (event.keyCode === 13 && !event.shiftKey) {
        event.preventDefault();
        $('#send-btn').click();
    }
});