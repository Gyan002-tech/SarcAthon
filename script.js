document.getElementById("send-btn").addEventListener("click", sendMessage);
document
  .getElementById("user-input")
  .addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      sendMessage();
    }
  });

function sendMessage() {
  const inputBox = document.getElementById("user-input");
  const userMessage = inputBox.value;

  if (userMessage.trim() === "") return; // Ignore empty messages

  // Create user message element
  const userMessageElement = document.createElement("div");
  userMessageElement.classList.add("chat-message", "user");
  userMessageElement.innerHTML = `<span>${userMessage}</span><i class="fas fa-user"></i>`; // User icon
  document.querySelector(".chat-body").appendChild(userMessageElement);
  inputBox.value = ""; // Clear input box

  // Check for known queries
  const botResponse = getBotResponse(userMessage);

  // If the botResponse is default (meaning unrecognized query), call the FastAPI API
  if (
    botResponse === "I'm not sure how to respond to that, but I'll do my best!"
  ) {
    fetch("http://127.0.0.1:5000/get-response", {
      // Ensure the URL matches your FastAPI endpoint
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question: userMessage }), // Send the user message as a question
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        // Create bot message element with the response from the model.py
        const botMessageElement = document.createElement("div");
        botMessageElement.classList.add("chat-message", "bot");
        botMessageElement.innerHTML = `<i class="fas fa-robot"></i><span>${data.response}</span>`; // Bot icon
        document.querySelector(".chat-body").appendChild(botMessageElement);
        document.querySelector(".chat-body").scrollTop =
          document.querySelector(".chat-body").scrollHeight; // Scroll to bottom
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  } else {
    // If we have a predefined response, display it
    setTimeout(() => {
      const botMessageElement = document.createElement("div");
      botMessageElement.classList.add("chat-message", "bot");
      botMessageElement.innerHTML = `<i class="fas fa-robot"></i><span>${botResponse}</span>`; // Bot icon
      document.querySelector(".chat-body").appendChild(botMessageElement);
      document.querySelector(".chat-body").scrollTop =
        document.querySelector(".chat-body").scrollHeight; // Scroll to bottom
    }, 1000);
  }
}

function getBotResponse(query) {
  // Replace this logic with actual processing on the server
  if (query.toLowerCase().includes("hello")) {
    return "Hi there! How can I help you today?";
  } else if (query.toLowerCase().includes("how are you")) {
    return "I'm just a bot, but I'm doing great! Thanks for asking!";
  } else {
    return "I'm not sure how to respond to that, but I'll do my best!";
  }
}
