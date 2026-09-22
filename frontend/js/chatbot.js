// ============================================================
// SMART QUEUE USER CHATBOT
// Helps the logged-in user with:
// - Token number
// - People waiting
// - Estimated waiting time
// - Queue name
// - Service type
// - Queue status
// - Active counters
// - Average service time
// ============================================================

const CHATBOT_API =
    "http://127.0.0.1:5000/api/chatbot/ask";


// ============================================================
// GET LOGGED-IN USER
// ============================================================

function getLoggedInUser() {

    try {

        const userData =
            localStorage.getItem("user");

        if (!userData) {
            return null;
        }

        return JSON.parse(userData);

    } catch (error) {

        console.error(
            "Error reading logged-in user:",
            error
        );

        return null;
    }
}


// ============================================================
// GET CURRENT QUEUE ID
// ============================================================

function getCurrentQueueId() {

    // First check queueId input on dashboard
    const queueInput =
        document.getElementById("queueId");

    if (
        queueInput &&
        queueInput.value
    ) {

        return Number(queueInput.value);
    }


    // Check localStorage
    const savedQueueId =
        localStorage.getItem("queue_id");

    if (savedQueueId) {

        return Number(savedQueueId);
    }


    // Check saved queue object
    const savedQueue =
        localStorage.getItem("userQueue");

    if (savedQueue) {

        try {

            const queue =
                JSON.parse(savedQueue);

            if (queue.queue_id) {
                return Number(queue.queue_id);
            }

            if (queue.id) {
                return Number(queue.id);
            }

        } catch (error) {

            console.error(
                "Queue data error:",
                error
            );
        }
    }


    return null;
}


// ============================================================
// OPEN CHATBOT
// ============================================================

function toggleChatbot() {

    const windowBox =
        document.getElementById(
            "chatbotWindow"
        );

    if (!windowBox) {

        console.error(
            "chatbotWindow not found"
        );

        return;
    }


    if (
        windowBox.style.display === "none" ||
        windowBox.style.display === ""
    ) {

        windowBox.style.display = "flex";


        const input =
            document.getElementById(
                "chatbotInput"
            );

        if (input) {

            input.focus();
        }

    } else {

        windowBox.style.display = "none";
    }
}


// ============================================================
// CLOSE CHATBOT
// ============================================================

function closeChatbot() {

    const windowBox =
        document.getElementById(
            "chatbotWindow"
        );

    if (windowBox) {

        windowBox.style.display = "none";
    }
}


// ============================================================
// SEND MESSAGE
// ============================================================

async function sendChatMessage() {

    const input =
        document.getElementById(
            "chatbotInput"
        );

    const messages =
        document.getElementById(
            "chatbotMessages"
        );


    if (!input || !messages) {

        console.error(
            "Chatbot elements not found"
        );

        return;
    }


    const question =
        input.value.trim();


    if (!question) {

        return;
    }


    // --------------------------------------------------------
    // Check logged-in user
    // --------------------------------------------------------

    const user =
        getLoggedInUser();


    if (!user) {

        addBotMessage(
            "⚠️ You are not logged in.\n\n" +
            "Please login first to use the Smart Queue Assistant."
        );

        return;
    }


    // --------------------------------------------------------
    // Get queue
    // --------------------------------------------------------

    const queueId =
        getCurrentQueueId();


    // --------------------------------------------------------
    // Display user message
    // --------------------------------------------------------

    addUserMessage(
        question
    );


    input.value = "";


    // --------------------------------------------------------
    // Show typing
    // --------------------------------------------------------

    const typing =
        addBotMessage(
            "Typing..."
        );


    try {

        // ----------------------------------------------------
        // Send information to Flask
        // ----------------------------------------------------

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

                        question:
                            question,

                        user_id:
                            user.id,

                        queue_id:
                            queueId

                    })
                }
            );


        // ----------------------------------------------------
        // HTTP error
        // ----------------------------------------------------

        if (!response.ok) {

            throw new Error(
                "HTTP Error: " +
                response.status
            );
        }


        // ----------------------------------------------------
        // Convert response to JSON
        // ----------------------------------------------------

        const data =
            await response.json();


        // ----------------------------------------------------
        // Remove typing
        // ----------------------------------------------------

        if (typing) {

            typing.remove();
        }


        // ----------------------------------------------------
        // Display chatbot response
        // ----------------------------------------------------

        if (data.success) {

            addBotMessage(
                data.answer
            );

        } else {

            addBotMessage(

                data.message ||
                "Sorry, I could not find the requested information."

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

            "⚠️ Cannot connect to the Smart Queue Assistant.\n\n" +
            "Please make sure Flask is running on port 5000."

        );
    }
}


// ============================================================
// ADD USER MESSAGE
// ============================================================

function addUserMessage(message) {

    const messages =
        document.getElementById(
            "chatbotMessages"
        );


    if (!messages) {

        return;
    }


    const div =
        document.createElement(
            "div"
        );


    div.className =
        "chat-message user-message";


    div.innerText =
        message;


    messages.appendChild(
        div
    );


    scrollChat();
}


// ============================================================
// ADD BOT MESSAGE
// ============================================================

function addBotMessage(message) {

    const messages =
        document.getElementById(
            "chatbotMessages"
        );


    if (!messages) {

        return null;
    }


    const div =
        document.createElement(
            "div"
        );


    div.className =
        "chat-message bot-message";


    div.innerText =
        message;


    messages.appendChild(
        div
    );


    scrollChat();


    return div;
}


// ============================================================
// SCROLL CHAT TO BOTTOM
// ============================================================

function scrollChat() {

    const messages =
        document.getElementById(
            "chatbotMessages"
        );


    if (messages) {

        messages.scrollTop =
            messages.scrollHeight;
    }
}


// ============================================================
// ENTER KEY
// ============================================================

function handleChatbotKey(event) {

    if (
        event.key === "Enter"
    ) {

        event.preventDefault();

        sendChatMessage();
    }
}


// ============================================================
// SUGGESTED QUESTION
// ============================================================

function askSuggestedQuestion(
    question
) {

    const input =
        document.getElementById(
            "chatbotInput"
        );


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
        document.getElementById(
            "chatbotMessages"
        );


    if (!messages) {

        return;
    }


    messages.innerHTML = "";


    addBotMessage(

        "Hello! 👋\n\n" +

        "I am your Smart Queue Assistant. 🤖\n\n" +

        "I can help you check:\n" +

        "🎫 Your token number\n" +

        "👥 People waiting\n" +

        "⏱️ Estimated waiting time\n" +

        "📍 Your queue\n" +

        "🏢 Service type\n" +

        "🪟 Active counters\n" +

        "📊 Queue status\n\n" +

        "Ask me anything about your current queue."

    );
}


// ============================================================
// INITIAL CHATBOT MESSAGE
// ============================================================

function showWelcomeMessage() {

    const messages =
        document.getElementById(
            "chatbotMessages"
        );


    if (!messages) {

        return;
    }


    // Don't add duplicate welcome message
    if (
        messages.children.length > 0
    ) {

        return;
    }


    const user =
        getLoggedInUser();


    if (!user) {

        addBotMessage(

            "Hello! 👋\n\n" +

            "Please login first to use the Smart Queue Assistant."

        );

        return;
    }


    addBotMessage(

        "Hello, " +
        (user.name || "User") +
        "! 👋\n\n" +

        "I am your Smart Queue Assistant. 🤖\n\n" +

        "I can help you with your current queue.\n\n" +

        "You can ask:\n" +

        "🎫 What is my token?\n" +

        "👥 How many people are waiting?\n" +

        "⏱️ How long do I need to wait?\n" +

        "📍 Where is my queue?\n" +

        "🏢 What service am I waiting for?\n" +

        "🪟 How many counters are active?\n" +

        "📊 What is the queue status?"

    );
}


// ============================================================
// LOGOUT SUPPORT
// ============================================================

function chatbotLogout() {

    localStorage.removeItem(
        "user"
    );

    localStorage.removeItem(
        "queue_id"
    );

    localStorage.removeItem(
        "userQueue"
    );

    window.location.href =
        "login.html";
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


        showWelcomeMessage();


        console.log(
            "Smart Queue User Chatbot loaded successfully."
        );


        const user =
            getLoggedInUser();


        if (user) {

            console.log(
                "Logged-in user:",
                user.name
            );

            console.log(
                "User ID:",
                user.id
            );
        }

    }
);