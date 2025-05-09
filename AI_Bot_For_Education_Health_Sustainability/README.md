# JavaScript Chatbot Application – Full Guide (README.md)

This README provides a complete guide to the chatbot front-end logic written in JavaScript, explaining each function and the core logic in a single file.

---

## 📁 File Structure
```
📦project-root
 ┣ 📜index.html (assumed)
 ┣ 📜style.css (assumed)
 ┣ 📜app.js (main chatbot JS logic)
 ┣ 📜README.md (this file)
 ┗ 📁images
     ┗ 📜user.jpg
     ┗ 📜gemini.svg
```

---

## 🚀 Features
- Chat with AI (OpenRouter Gemini model)
- Light/Dark mode toggle with persistence
- Save and load chat history from localStorage
- Suggestions for quick message input
- Copy message functionality

---

## ⚙️ Key Functionalities (app.js)

### 1. `getLocalData()`
Loads previously saved theme and chat history from localStorage.
```js
const getLocalData = () => {
    const currentTheme = localStorage.getItem('theme');
    const chats = localStorage.getItem('chats');

    if (chats) {
        chatList.innerHTML = chats;
        document.querySelector('.header').style.display = "none";
        chatList.style.display = "block";
    }

    if (currentTheme === "light-mode") {
        document.body.classList.add('light-mode');
        toggleBtn.innerText = "light_mode";
    } else {
        document.body.classList.remove('light-mode');
        toggleBtn.innerText = "dark_mode";
    }
};
```

### 2. Theme Toggle Button
Toggles between light and dark modes and saves the preference.
```js
toggleBtn.addEventListener('click', () => {
    document.body.classList.toggle('light-mode');
    const isLightMode = document.body.classList.contains('light-mode');
    toggleBtn.innerText = isLightMode ? "light_mode" : "dark_mode";
    localStorage.setItem("theme", isLightMode ? "light-mode" : "dark-mode");
});
```

### 3. `createMessageElement(content, ...classes)`
Utility function to create a message block.
```js
const createMessageElement = (content, ...classes) => {
    const div = document.createElement("div");
    div.classList.add("message", ...classes);
    div.innerHTML = content;
    return div;
};
```

### 4. `generateAPIResponse(promptText, incomingMessageDiv)`
Fetches AI response from OpenRouter API.
```js
const generateAPIResponse = async (promptText, incomingMessageDiv) => {
    const textElement = incomingMessageDiv.querySelector(".text");
    const apiKey = "<your-openrouter-api-key>";

    try {
        const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${apiKey}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                model: "google/gemini-flash-1.5",
                messages: [{ role: "user", content: [{ type: "text", text: promptText }] }]
            })
        });

        const data = await response.json();
        const reply = data.choices?.[0]?.message?.content || "No response received from the AI.";
        textElement.innerHTML = marked.parse(reply);
    } catch (error) {
        console.error("API error:", error);
        textElement.innerHTML = "⚠️ Error fetching response.";
    } finally {
        incomingMessageDiv.classList.remove("loading");
        localStorage.setItem("chats", chatList.innerHTML);
    }
};
```

### 5. `showLoadingAnimation()`
Displays typing/loading animation while waiting for API response.
```js
const showLoadingAnimation = () => {
    const html = `
        <div class="message-content">
            <img src="images/gemini.svg" alt="Gemini Image" class="avatar">
            <div class="text"></div>
            <div class="loading-indicator">
                <div class="loading-bar"></div>
                <div class="loading-bar"></div>
                <div class="loading-bar"></div>
            </div>
        </div>
        <span onclick="copyMessage(this)" class="icon material-symbols-rounded">content_copy</span>`;

    const incomingMessageDiv = createMessageElement(html, "incoming", "loading");
    chatList.appendChild(incomingMessageDiv);
    generateAPIResponse(userMessage, incomingMessageDiv);
};
```

### 6. `copyMessage(copyIcon)`
Copies AI's message to the clipboard.
```js
const copyMessage = (copyIcon) => {
    const messageDiv = copyIcon.closest('.message');
    const messageText = messageDiv.querySelector('.text').innerText;

    if (navigator.clipboard) {
        navigator.clipboard.writeText(messageText).then(() => {
            copyIcon.innerText = "done";
            setTimeout(() => copyIcon.innerText = "content_copy", 1000);
        }).catch(err => console.error("Copy failed:", err));
    }
};
```

### 7. `handleOutgoingChat()`
Handles the user's message submission.
```js
const handleOutgoingChat = () => {
    userMessage = typingForm.querySelector(".typing-input").value.trim();
    if (!userMessage) return;

    document.body.querySelector('.header').style.display = "none";
    chatList.style.display = "block";

    const html = `<div class="message-content">
                    <img src="images/user.jpg" alt="User Image" class="avatar">
                    <div class="text"></div>
                  </div>`;

    const outGoingMessageDiv = createMessageElement(html, "outgoing");
    outGoingMessageDiv.querySelector('.text').innerHTML = userMessage;
    chatList.appendChild(outGoingMessageDiv);
    typingForm.reset();
    setTimeout(showLoadingAnimation, 500);
};
```

### 8. Form Submit Handler
Handles enter/submit action.
```js
typingForm.addEventListener("submit", (e) => {
    e.preventDefault();
    handleOutgoingChat();
});
```

### 9. `handleSuggestionRequest(requestValue)`
Auto-fills a suggestion and triggers chat.
```js
const handleSuggestionRequest = (requestValue) => {
    typingForm.querySelector(".typing-input").value = requestValue;
    document.body.querySelector('.header').style.display = "none";
    chatList.style.display = "block";
    handleOutgoingChat();
};
```

### 10. Delete Button (Clear Chat History)
```js
document.querySelector('#delete-btn').addEventListener('click', () => {
    localStorage.removeItem("chats");
    location.reload();
});
```

---

## 🛡️ Security Notice
- Replace the placeholder API key with your actual [OpenRouter API Key](https://openrouter.ai/).
- Never expose the API key in production front-end applications.

---

## 📦 Dependencies
- `marked.js` – Used for rendering Markdown from AI response.

---

## 📌 Final Notes
This code provides a smooth user chat experience using modern front-end JavaScript features. You can extend it to:
- Add avatars dynamically
- Use secure APIs
- Store chat data in localStorage

---