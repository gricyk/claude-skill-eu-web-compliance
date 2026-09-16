// Chat assistant widget: answers questions about the menu, opening hours, and allergens.
(function () {
  var root = document.getElementById("chat-root");
  if (!root) return;

  root.innerHTML =
    '<div class="chat-bubble">' +
    '  <strong>Anna from Example Café</strong>' +
    '  <p>Hi! How can I help you today?</p>' +
    '  <input id="chat-input" type="text" placeholder="Ask about our menu...">' +
    '</div>';

  var history = JSON.parse(localStorage.getItem("chat_history") || "[]");

  document.getElementById("chat-input").addEventListener("keydown", async function (e) {
    if (e.key !== "Enter") return;
    history.push({ role: "user", content: e.target.value });
    var res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: history }),
    });
    var data = await res.json();
    history.push({ role: "assistant", content: data.reply });
    localStorage.setItem("chat_history", JSON.stringify(history));
    e.target.value = "";
  });
})();
