$(document).ready(function () {
    function getChats() {
        $.ajax({
            url: "/api/chats",
            type: "GET",
            success: function (chats) {
                $(".chat-select ul").empty();
                chats.forEach(function (chat) {
                    let chatName = chat.context ? chat.context : '';
                    $(".chat-select ul").append(
                        '<li data-id="' + chat.id + '" class="chat-item">' +
                        chatName +
                        '<i class="bi bi-trash delete-icon"></i>' +
                        '</li>'
                    );
                });
                $(".chat-select li:first-child").addClass("active");
                getMessages($(".chat-select li.active").data("id"));
            },
        });
    }

    // Retrieve all messages for a given chat session
    function getMessages(chatId) {
        $.ajax({
            url: "/api/chats/" + chatId + "/messages",
            type: "GET",
            success: function (messages) {
                $(".chat-history").empty();
                messages.forEach(function (message) {
                    $(".chat-history").append('<p>' + message.role + ': ' + message.content + '</p>');
                });
            },
        });
    }

    // Create a new chat session for the user
    function createNewChat() {
        $.ajax({
            url: "/api/chats",
            type: "POST",
            success: function (chat) {
                let chatName = chat.context ? chat.context : 'new_chat';
                $(".chat-select ul").append(
                    '<li data-id="' + chat.id + '" class="chat-item">' + chatName + "</li>"
                );
                $(".chat-select li.active").removeClass("active");
                $('.chat-select li[data-id="' + chat.id + '"]').addClass("active");
                $(".chat-history").empty();
            },
        });
    }

    function sendMessage(chatId, content) {
        $.ajax({
            url: "/api/chats/" + chatId + "/messages",
            type: "POST",
            contentType: 'application/json',
            data: JSON.stringify({content: content}),
            success: function (reply) {
                $(".chat-history").append('<p>User: ' + content + "</p>");
                $(".chat-history").append("<p>AI: " + reply.content + "</p>");

                // Update context in current window
                let currentChatItem = $('.chat-select li[data-id="' + chatId + '"]');
                currentChatItem.text(reply.context);
            },
        });
    }

    // Load all chat sessions upon page load
    getChats();

    // When a chat session is clicked, load the messages for that session
    $(document).on('click', '.chat-select li', function () {
        $(".chat-select li.active").removeClass("active");
        $(this).addClass("active");
        getMessages($(this).data("id"));
    });

    // When the 'new chat' button is clicked, create a new chat session
    $("#newChatButton").on('click', function () {
        createNewChat();
    });

    // When the 'send' button is clicked, send the current message to the active chat session
    $(".chat-input-container button").on('click', function () {
        var chatId = $(".chat-select li.active").data("id");
        var content = $(".chat-input-container textarea").val();
        if (content.trim() !== '') {
            sendMessage(chatId, content);
            $(".chat-input-container textarea").val('');
        }
    });

    // When the 'enter' key is pressed in the message input box, send the current message
    $(".chat-input-container textarea").keydown(function (event) {
        // Checks if the enter key is pressed
        if (event.key === "Enter") {
            // Check if the Shift key is pressed at the same time
            if (event.shiftKey) {
                // If the Shift key is pressed at the same time, do nothing and let the browser do the default line wrap
            } else {
                // If the Shift key is not pressed at the same time, we block the browser's default action
                // and then call the function that sends the message
                event.preventDefault();
                var chatId = $(".chat-select li.active").data("id");
                var content = $(this).val();
                if (content.trim() !== '') {
                    sendMessage(chatId, content);
                    $(this).val('');  // 清空 textarea
                }
            }
        }
    });

    // Delete a given chat session
    function deleteChat(chatId) {
        $.ajax({
            url: "/api/chats/" + chatId,
            type: "DELETE",
            success: function (response) {
                getChats();
            },
        });
    }

    // When the 'delete' icon is clicked, show confirm and cancel icons
    $(document).on('click', '.delete-icon', function (event) {
        event.stopPropagation();

        // Create new icons
        var confirmIcon = $('<i class="bi bi-check confirm-delete-icon"></i>');
        var cancelIcon = $('<i class="bi bi-x cancel-delete-icon"></i>');

        // Add new icons to parent
        $(this).parent().append(confirmIcon, cancelIcon);

        $(this).remove(); // Remove delete icon
    });

    // When the 'confirm' icon is clicked, delete the chat session
    $(document).on('click', '.confirm-delete-icon', function (event) {
        event.stopPropagation();
        var chatId = $(this).parent().data("id");
        deleteChat(chatId);
    });

    // When the 'cancel' icon is clicked, hide the confirm and cancel icons
    $(document).on('click', '.cancel-delete-icon', function (event) {
        event.stopPropagation();

        // Create delete icon
        var deleteIcon = $('<i class="bi bi-trash delete-icon"></i>');

        // Add delete icon to parent
        $(this).parent().append(deleteIcon);

        // Remove new icons
        $(this).siblings('.confirm-delete-icon').remove();
        $(this).remove();
    });


});
