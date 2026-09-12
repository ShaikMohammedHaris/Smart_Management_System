const CHATBOT_API =
    "http://127.0.0.1:5000/api/chatbot/ask";


// ============================================================
// OPEN CHATBOT
// ============================================================

function toggleChatbot() {

    const windowBox =
        document.getElementById("chatbotWindow");

    if (!windowBox) {
        console.error("chatbotWindow not found");
        return;
    }

    if (
        windowBox.style.display === "none" ||
        windowBox.style.display === ""
    ) {

        windowBox.style.display = "flex";

        const input =
            document.getElementById("chatbotInput");

        if (input) {
            input.focus();
        }

    } else {

        windowBox.style.display = "none";
    }
}


// ============================================================
// CLOSE
// ============================================================

function closeChatbot() {

    const windowBox =
        document.getElementById("chatbotWindow");

    if (windowBox) {
        windowBox.style.display = "none";
    }
}


// ============================================================
// SEND MESSAGE
// ============================================================

async function sendChatMessage() {

    const input =
        document.getElementById("chatbotInput");

    const messages =
        document.getElementById("chatbotMessages");


    if (!input || !messages) {

        console.error("Chatbot elements not found");

        return;
    }


    const question =
        input.value.trim();


    if (!question) {
        return;
    }


    // User message
    addUserMessage(question);


    // Clear input
    input.value = "";


    // Typing message
    const typing =
        addBotMessage("Typing...");


    try {

        const response =
            await fetch(
                CHATBOT_API,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        question: question
                    })
                }
            );


        if (!response.ok) {

            throw new Error(
                "HTTP error: " + response.status
            );
        }


        const data =
            await response.json();


        // Remove typing
        if (typing) {
            typing.remove();
        }


        if (data.success) {

            addBotMessage(data.answer);

        } else {

            addBotMessage(
                data.message ||
                "Sorry, I could not answer that question."
            );
        }


    } catch (error) {

        console.error(
            "Chatbot error:",
            error
        );


        if (typing) {
            typing.remove();
        }


        addBotMessage(
            "⚠️ Cannot connect to the chatbot server.\n\n" +
            "Please make sure Flask is running on port 5000."
        );
    }
}


// ============================================================
// USER MESSAGE
// ============================================================

function addUserMessage(message) {

    const messages =
        document.getElementById("chatbotMessages");


    const div =
        document.createElement("div");


    div.className =
        "chat-message user-message";


    div.innerText =
        message;


    messages.appendChild(div);


    scrollChat();
}


// ============================================================
// BOT MESSAGE
// ============================================================

function addBotMessage(message) {

    const messages =
        document.getElementById("chatbotMessages");


    const div =
        document.createElement("div");


    div.className =
        "chat-message bot-message";


    div.innerText =
        message;


    messages.appendChild(div);


    scrollChat();


    return div;
}


// ============================================================
// SCROLL
// ============================================================

function scrollChat() {

    const messages =
        document.getElementById("chatbotMessages");


    if (messages) {

        messages.scrollTop =
            messages.scrollHeight;
    }
}


// ============================================================
// ENTER KEY
// ============================================================

function handleChatbotKey(event) {

    if (event.key === "Enter") {

        event.preventDefault();

        sendChatMessage();
    }
}


// ============================================================
// SUGGESTED QUESTION
// ============================================================

function askSuggestedQuestion(question) {

    const input =
        document.getElementById("chatbotInput");


    if (!input) {
        return;
    }


    input.value =
        question;


    sendChatMessage();
}


// ============================================================
// CLEAR CHAT
// ============================================================

function clearChat() {

    const messages =
        document.getElementById("chatbotMessages");


    if (!messages) {
        return;
    }


    messages.innerHTML = "";


    addBotMessage(
        "Chat cleared. 🤖\n\n" +
        "What would you like to know about " +
        "the Smart Queue Management System?"
    );
}


// ============================================================
// PAGE LOAD
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const windowBox =
            document.getElementById(
                "chatbotWindow"
            );


        if (windowBox) {

            windowBox.style.display =
                "none";
        }


        console.log(
            "Smart Queue Chatbot loaded successfully."
        );
    }
);