const API = "[http://127.0.0.1:5000](http://127.0.0.1:5000)";

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

document.addEventListener("DOMContentLoaded", function () {

    const user = getLoggedInUser();

    if (!user) {
        alert("Please login first.");
        window\.location.href = "login.html";
        return;
    }

    const welcome = document.getElementById("welcome");

    if (welcome) {
        welcome.innerText =
            "Welcome, " + (user.name || "User") + "!";
    }

    loadUserQueue();

});

async function joinQueue() {

    const queueIdInput =
        document.getElementById("queueId");

    const message =
        document.getElementById("joinMessage");

    const user = getLoggedInUser();

    if (!user) {
        alert("Please login first.");
        window\.location.href = "login.html";
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

            localStorage.setItem(
                "queue_id",
                queueId
            );

            localStorage.setItem(
                "userQueue",
                JSON.stringify({
                    queue_id: queueId,
                    token_number:
                        data.token_number
                })
            );

            const token =
                document.getElementById("token");

            if (token) {
                token.innerText =
                    data.token_number;
            }

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

async function loadUserQueue() {

    const user =
        getLoggedInUser();

    if (!user) {
        return;
    }

    try {

        let queueId =
            localStorage.getItem("queue_id");

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

        await predictUserWaitingTime(queue);

    } catch (error) {

        console.error(
            "Load user queue error:",
            error
        );
    }
}

function updateQueueDisplay(queue) {

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

function logout() {

    localStorage.removeItem("user");
    localStorage.removeItem("queue_id");
    localStorage.removeItem("userQueue");
    localStorage.removeItem(
        "predicted_waiting_time"
    );

    window\.location.href =
        "login.html";
}

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