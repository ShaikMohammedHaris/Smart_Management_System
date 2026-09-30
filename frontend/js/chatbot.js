// =====================================================
// SMART QUEUE CUSTOMER CHATBOT
// =====================================================

const CHATBOT_API =
    "https://smart-queue-management-system-5vde.onrender.com/api/chatbot/ask";


// =====================================================
// GET LOGGED-IN USER
// =====================================================

function getLoggedInUser() {

    try {

        const user =
            JSON.parse(
                localStorage.getItem("user")
            );

        return user;

    }
    catch (error) {

        console.error(
            "User data error:",
            error
        );

        return null;

    }

}


// =====================================================
// GET QUEUE ID
// =====================================================

function getQueueId() {

    return localStorage.getItem(
        "queue_id"
    );

}


// =====================================================
// ADD MESSAGE TO CHAT
// =====================================================

function addChatMessage(
    message,
    type
) {

    const chatMessages =
        document.getElementById(
            "chatMessages"
        );


    if (!chatMessages) {

        console.error(
            "chatMessages element not found."
        );

        return;

    }


    const messageDiv =
        document.createElement(
            "div"
        );


    messageDiv.classList.add(
        "chat-message"
    );


    if (type === "user") {

        messageDiv.classList.add(
            "user-message"
        );

    }
    else {

        messageDiv.classList.add(
            "bot-message"
        );

    }


    messageDiv.innerText =
        message;


    chatMessages.appendChild(
        messageDiv
    );


    // Automatically scroll down

    chatMessages.scrollTop =
        chatMessages.scrollHeight;

}


// =====================================================
// SEND MESSAGE
// =====================================================

async function sendMessage() {

    const input =
        document.getElementById(
            "chatInput"
        );


    if (!input) {

        console.error(
            "chatInput element not found."
        );

        return;

    }


    const question =
        input.value.trim();


    // Don't send empty message

    if (!question) {

        return;

    }


    const user =
        getLoggedInUser();


    if (!user) {

        addChatMessage(
            "Please login first to use the customer support chatbot.",
            "bot"
        );

        return;

    }


    const queueId =
        getQueueId();


    // Display customer's message

    addChatMessage(
        question,
        "user"
    );


    // Clear input

    input.value = "";


    // Show temporary message

    const loadingMessage =
        document.createElement(
            "div"
        );


    loadingMessage.classList.add(
        "chat-message",
        "bot-message"
    );


    loadingMessage.innerText =
        "Checking your queue information...";


    const chatMessages =
        document.getElementById(
            "chatMessages"
        );


    chatMessages.appendChild(
        loadingMessage
    );


    chatMessages.scrollTop =
        chatMessages.scrollHeight;


    try {

        console.log(
            "Sending chatbot request..."
        );


        console.log(
            "User ID:",
            user.id
        );


        console.log(
            "Queue ID:",
            queueId
        );


        console.log(
            "Question:",
            question
        );


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
                            Number(user.id),

                        queue_id:
                            queueId
                                ? Number(queueId)
                                : null

                    })

                }
            );


        console.log(
            "Chatbot HTTP status:",
            response.status
        );


        const data =
            await response.json();


        console.log(
            "Chatbot response:",
            data
        );


        // Remove loading message

        loadingMessage.remove();


        if (response.ok && data.success) {

            let answer =
                data.answer ||
                data.message ||
                data.response;


            if (!answer) {

                answer =
                    "I received your request, but no answer was returned.";

            }


            addChatMessage(
                answer,
                "bot"
            );

        }

        else {

            addChatMessage(

                data.message ||
                "Sorry, I could not get your queue information.",

                "bot"

            );

        }

    }
    catch (error) {

        console.error(
            "CHATBOT ERROR:",
            error
        );


        loadingMessage.remove();


        addChatMessage(

            "Unable to connect to the chatbot server. Please make sure the Flask backend is running.",

            "bot"

        );

    }

}


// =====================================================
// ENTER KEY
// =====================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const input =
            document.getElementById(
                "chatInput"
            );


        if (!input) {

            console.error(
                "Chat input not found."
            );

            return;

        }


        input.addEventListener(
            "keydown",
            function (event) {

                if (
                    event.key ===
                    "Enter"
                ) {

                    event.preventDefault();

                    sendMessage();

                }

            }
        );

    }
);


// =====================================================
// CLEAR CHAT
// =====================================================

function clearChat() {

    const chatMessages =
        document.getElementById(
            "chatMessages"
        );


    if (!chatMessages) {
        return;
    }


    chatMessages.innerHTML = "";


    addChatMessage(

        "Hello! I can help you with your token number, queue position, people waiting, queue status and estimated waiting time.",

        "bot"

    );

}


// =====================================================
// SUGGESTED QUESTIONS
// =====================================================

function askSuggestedQuestion(
    question
) {

    const input =
        document.getElementById(
            "chatInput"
        );


    if (!input) {
        return;
    }


    input.value =
        question;


    sendMessage();

}