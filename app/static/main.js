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
                        '<li data-id="' + chat.id + '" class="chat-item">' + chatName + "</li>"
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

    $(".chat-input button").on('click', function () {
        var chatId = $(".chat-select li.active").data("id");
        var content = $(".chat-input input[type='text']").val();
        if (content.trim() !== '') {
            sendMessage(chatId, content);
            $(".chat-input input[type='text']").val('');
        }
    });
});
