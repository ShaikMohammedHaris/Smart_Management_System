let predictionFormEdited = false;

const API = "https://smart-queue-management-system-5vde.onrender.com";


/* =========================================================
   GET LOGGED-IN USER
   ========================================================= */

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
            "User data error:",
            error
        );

        return null;
    }
}


/* =========================================================
   CHECK LOGIN
   ========================================================= */

const currentUser =
    getLoggedInUser();


if (!currentUser) {

    window.location.href =
        "login.html";

}


/* =========================================================
   SHOW USER NAME
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const user =
            getLoggedInUser();

        if (!user) {
            return;
        }

        const welcome =
            document.getElementById(
                "welcomeUser"
            );

        if (welcome && user.name) {

            welcome.innerText =
                "Welcome, " +
                user.name +
                " to Smart Queue Predictor";

        }

    }
);


/* =========================================================
   JOIN QUEUE
   ========================================================= */

async function joinQueue() {

    const queueInput =
        document.getElementById(
            "queueId"
        );

    const message =
        document.getElementById(
            "joinMessage"
        );

    const user =
        getLoggedInUser();


    if (!user) {

        window.location.href =
            "login.html";

        return;

    }


    const queueId =
        Number(queueInput.value);


    if (!queueId || queueId < 1) {

        message.innerText =
            "Please enter a valid Queue ID.";

        message.style.color =
            "#dc2626";

        return;

    }


    message.innerText =
        "Joining queue...";

    message.style.color =
        "#1976d2";


    try {

        const response =
            await fetch(
                API +
                "/api/queue/join",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        queue_id:
                            queueId,

                        user_id:
                            user.id

                    })
                }
            );


        const data =
            await response.json();


        console.log(
            "Join queue response:",
            data
        );


        if (!response.ok || !data.success) {

            message.innerText =
                data.message ||
                "Could not join queue.";

            message.style.color =
                "#dc2626";

            return;

        }


        /*
         * Save the selected queue.
         */

        localStorage.setItem(
            "queue_id",
            String(queueId)
        );


        /*
         * Save queue information
         * if backend returns it.
         */

        if (data.queue) {

            localStorage.setItem(
                "userQueue",
                JSON.stringify(data.queue)
            );

        }


        /*
         * Show token.
         */

        if (
            data.token_number !== undefined &&
            data.token_number !== null
        ) {

            document.getElementById(
                "tokenNumber"
            ).innerText =
                data.token_number;

            document.getElementById(
                "tokenMessage"
            ).innerText =
                "You have successfully joined the queue.";

        }


        message.innerText =
            data.message ||
            "Successfully joined the queue!";

        message.style.color =
            "#15803d";


        /*
         * Load latest queue information.
         */

        await loadUserQueue();


    } catch (error) {

        console.error(
            "Join queue error:",
            error
        );

        message.innerText =
            "Cannot connect to the server. Make sure Flask is running.";

        message.style.color =
            "#dc2626";

    }

}


/* =========================================================
   LOAD USER QUEUE
   ========================================================= */

async function loadUserQueue() {

    const user =
        getLoggedInUser();

    if (!user) {
        return;
    }


    let queueId =
        localStorage.getItem(
            "queue_id"
        );


    /*
     * If queue_id isn't available,
     * try the saved queue object.
     */

    if (!queueId) {

        try {

            const savedQueue =
                localStorage.getItem(
                    "userQueue"
                );

            if (savedQueue) {

                const queue =
                    JSON.parse(savedQueue);

                if (queue && queue.id) {

                    queueId =
                        queue.id;

                }

            }

        } catch (error) {

            console.error(
                "Saved queue error:",
                error
            );

        }

    }


    /*
     * Nothing saved in this browser (new device, cleared storage,
     * or joined elsewhere): ask the server which queue this
     * user is waiting in.
     */

    if (!queueId) {

        try {

            const mine =
                await fetch(
                    API +
                    "/api/queue/mine/" +
                    user.id
                );

            if (mine.ok) {

                const mineData =
                    await mine.json();

                if (mineData.success) {

                    queueId =
                        String(mineData.queue_id);

                    localStorage.setItem(
                        "queue_id",
                        queueId
                    );

                }

            }

        } catch (error) {

            console.error(
                "Find user queue error:",
                error
            );

        }

    }


    if (!queueId) {

        return;

    }


    try {

        const response =
            await fetch(
                API +
                "/api/queue/status/" +
                queueId +
                "?user_id=" +
                user.id
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


        if (data.success) {

            const queue =
                data.queue;

            updateQueueDisplay(
                queue
            );


            /*
             * Automatically predict
             * waiting time.
             */

            if (!predictionFormEdited) {

                await predictUserWaitingTime(
                    queue
                );

            }

        }


    } catch (error) {

        console.error(
            "Queue loading error:",
            error
        );

    }

}


/* =========================================================
   UPDATE QUEUE DISPLAY
   ========================================================= */

function updateQueueDisplay(queue) {

    if (!queue) {
        return;
    }


    /*
     * Queue name
     */

    const queueName =
        document.getElementById(
            "userQueueName"
        );

    if (queueName) {

        queueName.innerText =
            queue.name ||
            queue.queue_name ||
            "-";

    }


    /*
     * Service type
     */

    const serviceType =
        document.getElementById(
            "userServiceType"
        );

    if (serviceType) {

        serviceType.innerText =
            queue.service_type ||
            "-";

    }


    /*
     * People waiting
     */

    const peopleWaiting =
        Number(
            queue.people_waiting ??
            queue.queue_length ??
            0
        );


    document.getElementById(
        "userPeopleWaiting"
    ).innerText =
        peopleWaiting;


    /*
     * People ahead
     */

    const peopleAhead =
        Number(
            queue.people_ahead ??
            0
        );


    document.getElementById(
        "userPeopleAhead"
    ).innerText =
        peopleAhead;


    /*
     * Queue position
     */

    const position =
        Number(
            queue.position ??
            queue.queue_position ??
            0
        );


    document.getElementById(
        "userPosition"
    ).innerText =
        position;


    /*
     * Queue status
     */

    const status =
        document.getElementById(
            "userQueueStatus"
        );


    if (status) {

        status.innerText =
            queue.status ||
            "Active";


        if (
            String(queue.status)
                .toLowerCase()
                === "active"
        ) {

            status.className =
                "status-active";

        } else {

            status.className =
                "";

        }

    }


    /*
     * Active counters
     */

    document.getElementById(
        "userActiveCounters"
    ).innerText =
        queue.active_counters ??
        "-";


    /*
     * Average service time
     */

    document.getElementById(
        "userAverageServiceTime"
    ).innerText =
        queue.average_service_time !== undefined
            ? queue.average_service_time + " min"
            : "-";


    /*
     * Prediction form automatically
     * receives current queue values.
     */

    const queueLengthInput =
        document.getElementById(
            "queueLength"
        );

    const countersInput =
        document.getElementById(
            "counters"
        );

    const serviceTimeInput =
        document.getElementById(
            "serviceTime"
        );


    if (queueLengthInput && !predictionFormEdited) {

        queueLengthInput.value =
            peopleWaiting;

    }


    if (countersInput && !predictionFormEdited) {

        countersInput.value =
            queue.active_counters ??
            1;

    }


    if (serviceTimeInput && !predictionFormEdited) {

        serviceTimeInput.value =
            queue.average_service_time ??
            1;

    }


    /*
     * Display token if returned.
     */

    if (
        queue.token_number !== undefined &&
        queue.token_number !== null
    ) {

        document.getElementById(
            "tokenNumber"
        ).innerText =
            queue.token_number;

        document.getElementById(
            "tokenMessage"
        ).innerText =
            "Your token is active in this queue.";

    }

}


/* =========================================================
   AUTOMATIC WAITING TIME PREDICTION
   ========================================================= */

async function predictUserWaitingTime(queue) {

    if (!queue) {
        return;
    }


    const arrivalInput =
        document.getElementById(
            "arrivalRate"
        );


    const arrivalRate =
        Number(
            arrivalInput?.value || 1
        );


    const queueLength =
        Number(
            queue.people_waiting ??
            queue.queue_length ??
            0
        );


    const activeCounters =
        Number(
            queue.active_counters ||
            1
        );


    const serviceTime =
        Number(
            queue.average_service_time ||
            1
        );


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
                            queue.id,

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
            "Automatic prediction:",
            data
        );


        if (data.success) {

            const prediction =
                Number(
                    data.predicted_waiting_time
                );


            document.getElementById(
                "prediction"
            ).innerText =
                prediction.toFixed(2);

        }


    } catch (error) {

        console.error(
            "Automatic prediction error:",
            error
        );

    }

}


/* =========================================================
   MANUAL PREDICTION
   ========================================================= */

async function predictTime() {

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
        !counters ||
        !serviceTime
    ) {

        alert(
            "Please enter valid prediction values."
        );

        return;

    }


    try {

        const queueId =
            Number(
                localStorage.getItem(
                    "queue_id"
                )
            );

        if (!queueId) {

            alert(
                "Please join a queue first."
            );

            return;

        }


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
                            queueId,

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


        if (!data.success) {

            alert(
                data.message ||
                "Prediction failed."
            );

            return;

        }


        const prediction =
            Number(
                data.predicted_waiting_time
            );


        document.getElementById(
            "prediction"
        ).innerText =
            prediction.toFixed(2);


    } catch (error) {

        console.error(
            "Prediction error:",
            error
        );

        alert(
            "Cannot connect to prediction server."
        );

    }

}


/* =========================================================
   USE LIVE QUEUE VALUES
   Refills the prediction form from the joined queue.
   ========================================================= */

async function useLiveQueueValues() {

    predictionFormEdited = false;

    await loadUserQueue();

}


/* =========================================================
   LOGOUT
   ========================================================= */

function logout() {

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


/* =========================================================
   AUTO REFRESH
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        loadUserQueue();


        /*
         * Refresh queue information
         * every 30 seconds.
         */

        setInterval(
            loadUserQueue,
            30000
        );


        /*
         * Remember when the user edits the prediction form
         * so auto-refresh never overwrites their values.
         */

        [
            "queueLength",
            "counters",
            "serviceTime",
            "arrivalRate"
        ].forEach(function (id) {

            const field =
                document.getElementById(id);

            if (field) {

                field.addEventListener(
                    "input",
                    function () {

                        predictionFormEdited = true;

                    }
                );

            }

        });

    }
);