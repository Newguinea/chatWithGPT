$(document).ready(function () {
  function fetchChats() {
    $.ajax({
      url: "/api/chats",
      method: "GET",
      success: function (chats) {
        $(".chat-select").html("");
        chats.forEach(function (chat) {
          let chatElement = `<li data-chat-id="${chat.id}">${chat.name}</li>`;
          $(".chat-select").append(chatElement);
        });
      },
    });
  }

  fetchChats();

  $(".chat-select").on("click", "li", function () {
    $(".chat-select li.active").removeClass("active");
    $(this).addClass("active");

    let chatId = $(this).data("chat-id");
    $.ajax({
      url: `/api/chats/${chatId}/messages`,
      method: "GET",
      success: function (messages) {
        $(".chat-history").html("");
        messages.forEach(function (message) {
          let messageElement = `<p>${message.role}: ${message.content}</p>`;
          $(".chat-history").append(messageElement);
        });
      },
    });
  });

  $(".chat-input button").on("click", function () {
    let messageText = $(".chat-input input").val();
    let chatId = $(".chat-select li.active").data("chat-id");

    $.ajax({
      url: `/api/chats/${chatId}/messages`,
      method: "POST",
      contentType: "application/json",
      data: JSON.stringify({
        content: messageText,
      }),
      success: function (response) {
        let messageElement = `<p>${response.role}: ${response.content}</p>`;
        $(".chat-history").append(messageElement);
        $(".chat-input input").val("");
      },
    });
  });

  $(".new-chat").on("click", function () {
    $.ajax({
      url: "/api/chats",
      method: "POST",
      success: function (chat) {
        let chatElement = `<li data-chat-id="${chat.id}">${chat.name}</li>`;
        $(".chat-select").append(chatElement);
      },
    });
  });
});