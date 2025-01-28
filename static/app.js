// Ensure this file is correctly linked in your HTML file

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("query-form");
  const input = document.getElementById("query-input");
  const chatContainer = document.getElementById("chat-container");

  form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const query = input.value.trim();
    if (!query) return;

    // Display user query in the chat
    const userMessage = document.createElement("div");
    userMessage.className = "user-message";
    userMessage.textContent = query;
    chatContainer.appendChild(userMessage);

    // Clear the input
    input.value = "";

    // Send the query to the backend
    try {
      const response = await fetch("/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch response from the server");
      }

      const data = await response.json();
      const botMessage = document.createElement("div");
      botMessage.className = "bot-message";
      botMessage.textContent = data.answer || "No response from the server.";
      chatContainer.appendChild(botMessage);
    } catch (error) {
      const errorMessage = document.createElement("div");
      errorMessage.className = "error-message";
      errorMessage.textContent = `Error: ${error.message}`;
      chatContainer.appendChild(errorMessage);
    }
  });
});
