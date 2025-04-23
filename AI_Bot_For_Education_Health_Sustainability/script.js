const typingForm = document.querySelector(".typing-form");
const chatList = document.querySelector(".chat-list");
const suggestionList = document.querySelector(".suggestion-list");
const toggleBtn = document.querySelector("#toggle-theme-btn");

let userMessage = null;

const getLocalData = () => {
    const currentTheme = localStorage.getItem('theme');
    const chats = localStorage.getItem('chats');

    if(chats){
        chatList.innerHTML = chats;
        document.querySelector('.header').style.display = "none";
        chatList.style.display = "block";
    }

    if(currentTheme === "light-mode"){
        document.body.classList.add('light-mode');
        toggleBtn.innerText = "light_mode";
    }else{
        document.body.classList.remove('light-mode');
        toggleBtn.innerText = "dark_mode";
    }
}

getLocalData();

toggleBtn.addEventListener('click', () => {
    document.body.classList.toggle('light-mode');
    const isLightMode = document.body.classList.contains('light-mode');
    
    toggleBtn.innerText = isLightMode ? "light_mode" : "dark_mode";
    localStorage.setItem("theme", isLightMode ? "light-mode" : "dark-mode");
});

const createMessageElement = (content, ...classes) => {
    const div = document.createElement("div");
    div.classList.add("message", ...classes);
    div.innerHTML = content;
    return div;
    
    
}

const generateAPIResponse = async (promptText, incomingMessageDiv) => {
    const textElement = incomingMessageDiv.querySelector(".text");
    const apiKey = "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";

    try {
        const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${apiKey}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                model: "google/gemini-flash-1.5",
                messages: [
                    {
                        role: "user",
                        content: [
                            {
                                type: "text",
                                text: promptText
                            }
                        ]
                    }
                ]
            })
        });

        const data = await response.json();

        if (data.choices && data.choices.length > 0 && data.choices[0].message?.content) {
            const reply = data.choices[0].message.content;
            const result = marked.parse(reply);
            textElement.innerHTML = result;
        } else {
            textElement.innerHTML = "No response received from the AI Because the apiKey expired.";
        }

        incomingMessageDiv.classList.remove("loading");
        localStorage.setItem("chats", chatList.innerHTML);
    }

    catch (error) {
        console.error("API error:", error);
        textElement.innerHTML = "⚠️ Error fetching response.";
        incomingMessageDiv.classList.remove("loading");
    }
}


document.querySelector('#delete-btn').addEventListener('click', ()=>{
    localStorage.removeItem("chats");
    location.reload();
})

const handleSuggestionRequest = (requestValue) => {
    typingForm.querySelector(".typing-input").value = requestValue;
    document.body.querySelector('.header').style.display = "none";
    chatList.style.display = "block";
    handleOutgoingChat();
}

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
}

// const copyMessage = (copyIcon) => {
//     const messageText = copyIcon.parentElement.querySelector('.text');
//     navigator.clipboard.writeText(messageText);
//     copyIcon.innerText = "done";
//     setTimeout(()=> copyIcon.innerText = "content_copy", 100)
// }

const copyMessage = (copyIcon) => {
    const messageDiv = copyIcon.closest('.message');
    const messageText = messageDiv.querySelector('.text').innerText;

    if (navigator.clipboard) {
        navigator.clipboard.writeText(messageText).then(() => {
            copyIcon.innerText = "done";
            setTimeout(() => copyIcon.innerText = "content_copy", 1000);
        }).catch((err) => {
            console.error("Failed to copy text: ", err);
        });
    } else {
        console.error("Clipboard API is not available.");
        alert("Clipboard functionality is not supported in this environment.");
    }
}


const handleOutgoingChat = () => {
    userMessage = typingForm.querySelector(".typing-input").value.trim();
    if (!userMessage) return;

    document.body.querySelector('.header').style.display = "none";
    chatList.style.display = "block";

    const html = `<div class="message-content">
                <img src="images/user.jpg" alt="User Image" class="avatar">
                <div class="text"></div>
            </div>`

    const outGoingMessageDiv = createMessageElement(html, "outgoing");
    outGoingMessageDiv.querySelector('.text').innerHTML = userMessage;
    chatList.appendChild(outGoingMessageDiv);
    typingForm.reset();
    setTimeout(showLoadingAnimation, 500);
}

typingForm.addEventListener("submit", (e) => {
    e.preventDefault();
    handleOutgoingChat();
})