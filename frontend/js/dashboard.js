// ============================================================
// SMART QUEUE USER DASHBOARD
// ============================================================

const API = "http://127.0.0.1:5000";

// ============================================================
// GET LOGGED-IN USER
// ============================================================

function getLoggedInUser() {
    try {
        const userData = localStorage.getItem("user");

        if (!userData) {
            return null;
        }

        return JSON.parse(userData);

    } catch (error) {
        console.error("Error reading user:", error);
        return null;
    }
}


// ============================================================
// PAGE LOAD
// ============================================================

document.addEventListener("DOMContentLoaded", function () {

    const user = getLoggedInUser();

    if (!user) {
        alert("Please login first.");
        window.location.href = "login.html";
        return;
    }

    // Display welcome message
    const welcome = document.getElementById("welcome");

    if (welcome) {
        welcome.innerText =
            "Welcome, " + (user.name || "User") + "!";
    }

    // Load user's queue information
    loadUserQueue();

});


// ============================================================
// JOIN QUEUE
// ============================================================

async function joinQueue() {

    const queueIdInput =
        document.getElementById("queueId");

    const message =
        document.getElementById("joinMessage");

    const user = getLoggedInUser();

    if (!user) {
        alert("Please login first.");
        window.location.href = "login.html";
        return;
    }

    if (!queueIdInput) {
        return;
    }

    const queueId =
        Number(queueIdInput.value);

    if (!queueId || queueId <= 0) {

        if (message) {
            message.innerText =
                "Please enter a valid Queue ID.";
        }

        return;
    }

    try {

        const response = await fetch(
            API + "/api/queue/join",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    queue_id: queueId,
                    user_id: user.id
                })
            }
        );

        const data =
            await response.json();

        console.log(
            "Join queue response:",
            data
        );

        if (data.success) {

            if (message) {
                message.innerText =
                    "Successfully joined the queue!";
            }

            // Save queue ID
            localStorage.setItem(
                "queue_id",
                queueId
            );

            // Save basic queue information
            localStorage.setItem(
                "userQueue",
                JSON.stringify({
                    queue_id: queueId,
                    token_number:
                        data.token_number
                })
            );

            // Display token
            const token =
                document.getElementById("token");

            if (token) {
                token.innerText =
                    data.token_number;
            }

            // Load complete queue information
            await loadUserQueue();

        } else {

            if (message) {
                message.innerText =
                    data.message ||
                    "Unable to join queue.";
            }
        }

    } catch (error) {

        console.error(
            "Join queue error:",
            error
        );

        if (message) {
            message.innerText =
                "Cannot connect to server. Make sure Flask is running.";
        }
    }
}


// ============================================================
// LOAD USER QUEUE
// ============================================================

async function loadUserQueue() {

    const user =
        getLoggedInUser();

    if (!user) {
        return;
    }

    try {

        // Get saved queue ID
        let queueId =
            localStorage.getItem("queue_id");

        // If no queue ID, try userQueue
        if (!queueId) {

            const savedQueue =
                localStorage.getItem("userQueue");

            if (savedQueue) {

                try {

                    const queue =
                        JSON.parse(savedQueue);

                    queueId =
                        queue.queue_id ||
                        queue.id;

                } catch (error) {

                    console.error(
                        "Saved queue error:",
                        error
                    );
                }
            }
        }

        if (!queueId) {

            console.log(
                "User has not joined a queue yet."
            );

            return;
        }

        // Get queue status for this queue
        const response =
            await fetch(
                API +
                "/api/queue/status/" +
                queueId
            );

        if (!response.ok) {

            throw new Error(
                "Queue status request failed"
            );
        }

        const data =
            await response.json();

        console.log(
            "Queue status:",
            data
        );

        if (!data.success) {

            console.log(
                data.message ||
                "Queue information unavailable."
            );

            return;
        }

        const queue =
            data.queue || data;

        updateQueueDisplay(queue);

        // Automatically calculate prediction
        await predictUserWaitingTime(queue);

    } catch (error) {

        console.error(
            "Load user queue error:",
            error
        );
    }
}


// ============================================================
// UPDATE QUEUE INFORMATION ON SCREEN
// ============================================================

function updateQueueDisplay(queue) {

    // ----------------------------
    // TOKEN
    // ----------------------------

    if (
        queue.token_number !== undefined
    ) {

        const token =
            document.getElementById("token");

        if (token) {
            token.innerText =
                queue.token_number;
        }
    }


    // ----------------------------
    // QUEUE NAME
    // ----------------------------

    if (
        queue.queue_name !== undefined
    ) {

        const element =
            document.getElementById(
                "userQueueName"
            );

        if (element) {
            element.innerText =
                queue.queue_name;
        }
    }


    // ----------------------------
    // SERVICE TYPE
    // ----------------------------

    if (
        queue.service_type !== undefined
    ) {

        const element =
            document.getElementById(
                "userServiceType"
            );

        if (element) {
            element.innerText =
                queue.service_type;
        }
    }


    // ----------------------------
    // PEOPLE WAITING
    // ----------------------------

    if (
        queue.people_waiting !== undefined
    ) {

        const element =
            document.getElementById(
                "userPeopleWaiting"
            );

        if (element) {
            element.innerText =
                queue.people_waiting;
        }
    }


    // ----------------------------
    // PEOPLE AHEAD
    // ----------------------------

    if (
        queue.people_ahead !== undefined
    ) {

        const element =
            document.getElementById(
                "userPeopleAhead"
            );

        if (element) {
            element.innerText =
                queue.people_ahead;
        }
    }


    // ----------------------------
    // QUEUE POSITION
    // ----------------------------

    if (
        queue.position !== undefined
    ) {

        const element =
            document.getElementById(
                "userPosition"
            );

        if (element) {
            element.innerText =
                queue.position;
        }
    }


    // ----------------------------
    // QUEUE STATUS
    // ----------------------------

    if (
        queue.status !== undefined
    ) {

        const element =
            document.getElementById(
                "userQueueStatus"
            );

        if (element) {
            element.innerText =
                queue.status;
        }
    }


    // ----------------------------
    // ACTIVE COUNTERS
    // ----------------------------

    if (
        queue.active_counters !== undefined
    ) {

        const element =
            document.getElementById(
                "userActiveCounters"
            );

        if (element) {
            element.innerText =
                queue.active_counters;
        }
    }


    // ----------------------------
    // AVERAGE SERVICE TIME
    // ----------------------------

    if (
        queue.average_service_time !==
        undefined
    ) {

        const element =
            document.getElementById(
                "userAverageServiceTime"
            );

        if (element) {

            element.innerText =
                Number(
                    queue.average_service_time
                ).toFixed(1) +
                " minutes";
        }
    }


    // ========================================================
    // FILL PREDICTION INPUTS AUTOMATICALLY
    // ========================================================

    if (
        queue.people_waiting !== undefined
    ) {

        const input =
            document.getElementById(
                "queueLength"
            );

        if (input) {
            input.value =
                queue.people_waiting;
        }
    }


    if (
        queue.active_counters !== undefined
    ) {

        const input =
            document.getElementById(
                "counters"
            );

        if (input) {
            input.value =
                queue.active_counters;
        }
    }


    if (
        queue.average_service_time !==
        undefined
    ) {

        const input =
            document.getElementById(
                "serviceTime"
            );

        if (input) {

            input.value =
                queue.average_service_time;
        }
    }
}


// ============================================================
// PREDICT USER WAITING TIME
// ============================================================

async function predictUserWaitingTime(queue) {

    if (!queue) {
        return;
    }

    const user =
        getLoggedInUser();

    if (!user) {
        return;
    }

    const queueId =
        queue.queue_id ||
        queue.id ||
        localStorage.getItem(
            "queue_id"
        );

    if (!queueId) {
        return;
    }

    const queueLength =
        Number(
            queue.people_waiting || 0
        );

    const activeCounters =
        Number(
            queue.active_counters || 1
        );

    const serviceTime =
        Number(
            queue.average_service_time || 5
        );

    // Default arrival rate
    const arrivalRateInput =
        document.getElementById(
            "arrivalRate"
        );

    let arrivalRate = 1;

    if (
        arrivalRateInput &&
        arrivalRateInput.value
    ) {

        arrivalRate =
            Number(
                arrivalRateInput.value
            );
    }

    if (!arrivalRate || arrivalRate <= 0) {
        arrivalRate = 1;
    }

    try {

        const response =
            await fetch(
                API +
                "/api/prediction/predict",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        queue_id:
                            Number(queueId),

                        queue_length:
                            queueLength,

                        active_counters:
                            activeCounters,

                        avg_service_time:
                            serviceTime,

                        arrival_rate:
                            arrivalRate
                    })
                }
            );

        if (!response.ok) {

            throw new Error(
                "Prediction request failed"
            );
        }

        const data =
            await response.json();

        console.log(
            "Prediction response:",
            data
        );

        if (data.success) {

            const prediction =
                document.getElementById(
                    "prediction"
                );

            if (prediction) {

                prediction.innerText =
                    Number(
                        data.predicted_waiting_time
                    ).toFixed(2);
            }

            // Save prediction
            localStorage.setItem(
                "predicted_waiting_time",
                data.predicted_waiting_time
            );
        }

    } catch (error) {

        console.error(
            "Prediction error:",
            error
        );
    }
}


// ============================================================
// MANUAL PREDICTION BUTTON
// ============================================================

async function predictTime() {

    const user =
        getLoggedInUser();

    if (!user) {

        alert(
            "Please login first."
        );

        return;
    }


    const queueId =
        localStorage.getItem(
            "queue_id"
        );

    if (!queueId) {

        alert(
            "Please join a queue first."
        );

        return;
    }


    const queueLength =
        Number(
            document.getElementById(
                "queueLength"
            ).value
        );

    const counters =
        Number(
            document.getElementById(
                "counters"
            ).value
        );

    const serviceTime =
        Number(
            document.getElementById(
                "serviceTime"
            ).value
        );

    const arrivalRate =
        Number(
            document.getElementById(
                "arrivalRate"
            ).value
        );


    if (
        queueLength < 0 ||
        counters <= 0 ||
        serviceTime <= 0 ||
        arrivalRate < 0
    ) {

        alert(
            "Please enter valid prediction values."
        );

        return;
    }


    try {

        const response =
            await fetch(
                API +
                "/api/prediction/predict",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        queue_id:
                            Number(queueId),

                        queue_length:
                            queueLength,

                        active_counters:
                            counters,

                        avg_service_time:
                            serviceTime,

                        arrival_rate:
                            arrivalRate
                    })
                }
            );


        const data =
            await response.json();

        console.log(
            "Manual prediction:",
            data
        );


        if (data.success) {

            const prediction =
                document.getElementById(
                    "prediction"
                );

            if (prediction) {

                prediction.innerText =
                    Number(
                        data.predicted_waiting_time
                    ).toFixed(2);
            }

        } else {

            alert(
                data.message ||
                "Prediction failed."
            );
        }

    } catch (error) {

        console.error(
            "Prediction error:",
            error
        );

        alert(
            "Cannot connect to Flask server."
        );
    }
}


// ============================================================
// LOGOUT
// ============================================================

function logout() {

    localStorage.removeItem("user");
    localStorage.removeItem("queue_id");
    localStorage.removeItem("userQueue");
    localStorage.removeItem(
        "predicted_waiting_time"
    );

    window.location.href =
        "login.html";
}


// ============================================================
// AUTO REFRESH QUEUE
// Every 30 seconds
// ============================================================

setInterval(
    function () {

        const user =
            getLoggedInUser();

        if (user) {
            loadUserQueue();
        }

    },
    30000
);