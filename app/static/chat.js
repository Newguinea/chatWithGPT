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

    function createNewChat() {
        $.ajax({
            url: "/api/chats",
            type: "POST",
            success: function (chat) {
                let chatName = chat.context ? chat.context : 'new_chat';
                $(".chat-select ul").append(
                    '<li data-id="' + chat.id + '" class="chat-item">' + chatName + "</li>"
                );
                // 更新聊天选择器中的活动聊天
                $(".chat-select li.active").removeClass("active");
                $('.chat-select li[data-id="' + chat.id + '"]').addClass("active");

                // 清空聊天历史
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

                // 更新当前聊天窗口的context
                let currentChatItem = $('.chat-select li[data-id="' + chatId + '"]');
                currentChatItem.text(reply.context);
            },
        });
    }


    getChats();

    $(document).on('click', '.chat-select li', function () {
        $(".chat-select li.active").removeClass("active");
        $(this).addClass("active");
        getMessages($(this).data("id"));
    });

    $("#newChatButton").on('click', function () {
        createNewChat();
    });

    $(".chat-input-container button").on('click', function () {
        var chatId = $(".chat-select li.active").data("id");
        var content = $(".chat-input-container textarea").val();
        if (content.trim() !== '') {
            sendMessage(chatId, content);
            $(".chat-input-container textarea").val('');
        }
    });

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


    function deleteChat(chatId) {
        $.ajax({
            url: "/api/chats/" + chatId,
            type: "DELETE",
            success: function (response) {
                getChats();
            },
        });
    }

    // ...

    $(document).on('click', '.delete-icon', function (event) {
        event.stopPropagation();

        // Create new icons
        var confirmIcon = $('<i class="bi bi-check confirm-delete-icon"></i>');
        var cancelIcon = $('<i class="bi bi-x cancel-delete-icon"></i>');

        // Add new icons to parent
        $(this).parent().append(confirmIcon, cancelIcon);

        $(this).remove(); // Remove delete icon
    });

    $(document).on('click', '.confirm-delete-icon', function (event) {
        event.stopPropagation();
        var chatId = $(this).parent().data("id");
        deleteChat(chatId);
    });

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
