// ============================================================
// SMART QUEUE ADMIN DASHBOARD
// ============================================================

const API =
    "http://127.0.0.1:5000";


// ============================================================
// LOAD DASHBOARD
// ============================================================

async function loadDashboard() {

    try {

        const response =
            await fetch(
                API + "/api/admin/dashboard"
            );


        if (!response.ok) {

            throw new Error(
                "Dashboard request failed"
            );

        }


        const data =
            await response.json();


        console.log(
            "Dashboard:",
            data
        );


        if (data.success) {

            const dashboard =
                data.dashboard;


            document.getElementById(
                "users"
            ).innerText =
                dashboard.total_users;


            document.getElementById(
                "queues"
            ).innerText =
                dashboard.active_queues;


            document.getElementById(
                "waiting"
            ).innerText =
                dashboard.people_waiting;


            document.getElementById(
                "average"
            ).innerText =
                Number(
                    dashboard.average_predicted_waiting_time
                ).toFixed(2);

        }


    } catch (error) {

        console.error(
            "Dashboard error:",
            error
        );

    }

}


// ============================================================
// LOAD QUEUES
// ============================================================

async function loadQueues() {

    try {

        const response =
            await fetch(
                API + "/api/queue/list"
            );


        if (!response.ok) {

            throw new Error(
                "Queue list request failed"
            );

        }


        const data =
            await response.json();


        console.log(
            "Queues:",
            data
        );


        const select =
            document.getElementById(
                "queueSelect"
            );


        select.innerHTML =
            '<option value="">Select Queue</option>';


        if (
            data.success &&
            data.queues.length > 0
        ) {


            data.queues.forEach(
                q => {

                    const option =
                        document.createElement(
                            "option"
                        );


                    option.value =
                        q.id;


                    option.textContent =
                        q.id +
                        " - " +
                        q.name;


                    select.appendChild(
                        option
                    );

                }
            );


            // Select first queue

            select.value =
                data.queues[0].id;


            loadQueueDetails();

        }


    } catch (error) {

        console.error(
            "Queue loading error:",
            error
        );


        const message =
            document.getElementById(
                "message"
            );


        if (message) {

            message.innerText =
                "Could not load queues. Make sure Flask is running.";

        }

    }

}


// ============================================================
// LOAD SELECTED QUEUE DETAILS
// ============================================================

async function loadQueueDetails() {

    const queueId =
        document.getElementById(
            "queueSelect"
        ).value;


    if (!queueId) {

        return;

    }


    try {

        const response =
            await fetch(
                API +
                "/api/queue/details/" +
                queueId
            );


        if (!response.ok) {

            throw new Error(
                "Queue details request failed"
            );

        }


        const data =
            await response.json();


        console.log(
            "Queue details:",
            data
        );


        if (data.success) {

            const q =
                data.queue;


            // ------------------------------------------------
            // FORM VALUES
            // ------------------------------------------------

            document.getElementById(
                "queueName"
            ).value =
                q.name;


            document.getElementById(
                "serviceType"
            ).value =
                q.service_type;


            document.getElementById(
                "activeCounters"
            ).value =
                q.active_counters;


            document.getElementById(
                "averageServiceTime"
            ).value =
                q.average_service_time;


            // IMPORTANT:
            // People Waiting is now editable

            document.getElementById(
                "peopleWaiting"
            ).value =
                q.people_waiting;


            // ------------------------------------------------
            // CURRENT DETAILS
            // ------------------------------------------------

            document.getElementById(
                "currentQueueName"
            ).innerText =
                q.name;


            document.getElementById(
                "currentServiceType"
            ).innerText =
                q.service_type;


            document.getElementById(
                "currentCounters"
            ).innerText =
                q.active_counters;


            document.getElementById(
                "currentServiceTime"
            ).innerText =
                q.average_service_time;


            document.getElementById(
                "currentPeopleWaiting"
            ).innerText =
                q.people_waiting;


            // ------------------------------------------------
            // CALCULATE PREDICTION
            // ------------------------------------------------

            await calculatePrediction(q);

        }


    } catch (error) {

        console.error(
            "Queue details error:",
            error
        );

    }

}


// ============================================================
// UPDATE QUEUE
// ============================================================

async function updateQueue() {

    console.log(
        "Update Queue button clicked"
    );


    const queueId =
        document.getElementById(
            "queueSelect"
        ).value;


    if (!queueId) {

        alert(
            "Please select a queue first."
        );

        return;

    }


    // --------------------------------------------------------
    // READ VALUES
    // --------------------------------------------------------

    const queueName =
        document.getElementById(
            "queueName"
        ).value.trim();


    const serviceType =
        document.getElementById(
            "serviceType"
        ).value.trim();


    const activeCounters =
        document.getElementById(
            "activeCounters"
        ).value;


    const averageServiceTime =
        document.getElementById(
            "averageServiceTime"
        ).value;


    const peopleWaiting =
        document.getElementById(
            "peopleWaiting"
        ).value;


    // --------------------------------------------------------
    // VALIDATION
    // --------------------------------------------------------

    if (!queueName) {

        alert(
            "Please enter queue name."
        );

        return;

    }


    if (!serviceType) {

        alert(
            "Please enter service type."
        );

        return;

    }


    if (
        activeCounters === "" ||
        Number(activeCounters) < 1
    ) {

        alert(
            "Active counters must be at least 1."
        );

        return;

    }


    if (
        averageServiceTime === "" ||
        Number(averageServiceTime) < 0
    ) {

        alert(
            "Please enter a valid average service time."
        );

        return;

    }


    if (
        peopleWaiting === "" ||
        Number(peopleWaiting) < 0
    ) {

        alert(
            "Please enter a valid number of people waiting."
        );

        return;

    }


    // --------------------------------------------------------
    // SEND TO BACKEND
    // --------------------------------------------------------

    try {

        const response =
            await fetch(
                API +
                "/api/queue/update/" +
                queueId,
                {

                    method: "PUT",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        queue_name:
                            queueName,

                        service_type:
                            serviceType,

                        active_counters:
                            Number(
                                activeCounters
                            ),

                        average_service_time:
                            Number(
                                averageServiceTime
                            ),

                        people_waiting:
                            Number(
                                peopleWaiting
                            )

                    })

                }
            );


        const data =
            await response.json();


        console.log(
            "Update response:",
            data
        );


        if (data.success) {

            document.getElementById(
                "message"
            ).innerText =
                "Queue updated successfully!";


            // Reload details

            await loadQueueDetails();


            // Reload dashboard

            await loadDashboard();

        } else {

            alert(
                data.message ||
                "Queue update failed."
            );

        }


    } catch (error) {

        console.error(
            "Update error:",
            error
        );


        alert(
            "Could not update queue. Make sure Flask is running."
        );

    }

}


// ============================================================
// CALCULATE WAITING TIME PREDICTION
// ============================================================

async function calculatePrediction(queue) {

    const arrivalRateElement =
        document.getElementById(
            "arrivalRate"
        );


    let arrivalRate = 5;


    if (arrivalRateElement) {

        arrivalRate =
            Number(
                arrivalRateElement.value
            );

    }


    if (
        isNaN(arrivalRate) ||
        arrivalRate < 0
    ) {

        arrivalRate = 5;

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
                            queue.id,

                        // IMPORTANT:
                        // Use manually entered
                        // people waiting value

                        queue_length:
                            Number(
                                document.getElementById(
                                    "peopleWaiting"
                                ).value
                            ),

                        active_counters:
                            Number(
                                document.getElementById(
                                    "activeCounters"
                                ).value
                            ),

                        avg_service_time:
                            Number(
                                document.getElementById(
                                    "averageServiceTime"
                                ).value
                            ),

                        arrival_rate:
                            arrivalRate

                    })

                }
            );


        const data =
            await response.json();


        console.log(
            "Prediction response:",
            data
        );


        if (data.success) {

            const prediction =
                Number(
                    data.predicted_waiting_time
                );


            document.getElementById(
                "selectedPrediction"
            ).innerText =
                prediction.toFixed(2);


            await loadDashboard();

        } else {

            console.error(
                "Prediction error:",
                data.message
            );

        }


    } catch (error) {

        console.error(
            "Prediction request error:",
            error
        );

    }

}


// ============================================================
// SERVE NEXT CUSTOMER
// ============================================================

async function serveNext() {

    const queueId =
        document.getElementById(
            "queueSelect"
        ).value;


    if (!queueId) {

        alert(
            "Please select a queue first."
        );

        return;

    }


    try {

        const response =
            await fetch(
                API +
                "/api/queue/next/" +
                queueId,
                {
                    method: "POST"
                }
            );


        const data =
            await response.json();


        if (data.success) {

            document.getElementById(
                "message"
            ).innerText =
                "Token " +
                data.served_token +
                " served successfully!";


            await loadQueueDetails();

            await loadDashboard();

        } else {

            alert(
                data.message
            );

        }


    } catch (error) {

        console.error(
            "Serve error:",
            error
        );


        alert(
            "Could not serve customer."
        );

    }

}


// ============================================================
// ARRIVAL RATE CHANGE
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const arrivalInput =
            document.getElementById(
                "arrivalRate"
            );


        if (arrivalInput) {

            arrivalInput.addEventListener(
                "change",
                function () {

                    const queueId =
                        document.getElementById(
                            "queueSelect"
                        ).value;


                    if (queueId) {

                        loadQueueDetails();

                    }

                }
            );

        }


        // ----------------------------------------------------
        // PEOPLE WAITING CHANGE
        // ----------------------------------------------------
        //
        // When the admin changes People Waiting,
        // immediately calculate a new prediction.
        //

        const peopleWaitingInput =
            document.getElementById(
                "peopleWaiting"
            );


        if (peopleWaitingInput) {

            peopleWaitingInput.addEventListener(
                "input",
                async function () {

                    const queueId =
                        document.getElementById(
                            "queueSelect"
                        ).value;


                    if (!queueId) {

                        return;

                    }


                    const queue = {

                        id:
                            Number(queueId),

                        people_waiting:
                            Number(
                                peopleWaitingInput.value
                            ),

                        active_counters:
                            Number(
                                document.getElementById(
                                    "activeCounters"
                                ).value
                            ),

                        average_service_time:
                            Number(
                                document.getElementById(
                                    "averageServiceTime"
                                ).value
                            )

                    };


                    // Update current display immediately

                    document.getElementById(
                        "currentPeopleWaiting"
                    ).innerText =
                        peopleWaitingInput.value || 0;


                    // Calculate prediction

                    await calculatePrediction(
                        queue
                    );

                }
            );

        }

    }
);


// ============================================================
// QUEUE SELECTION CHANGE
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const queueSelect =
            document.getElementById(
                "queueSelect"
            );


        if (queueSelect) {

            queueSelect.addEventListener(
                "change",
                function () {

                    loadQueueDetails();

                }
            );

        }

    }
);


// ============================================================
// INITIAL LOAD
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        loadDashboard();

        loadQueues();

    }
);