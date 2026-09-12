// =====================================================
// BACKEND URL
// =====================================================

const API = "http://127.0.0.1:5000";


// =====================================================
// LOAD ADMIN DASHBOARD
// =====================================================

async function loadDashboard() {

    try {

        const response = await fetch(
            API + "/api/admin/dashboard"
        );

        if (!response.ok) {
            throw new Error("Dashboard request failed");
        }

        const data = await response.json();

        console.log("Dashboard:", data);

        if (data.success) {

            const dashboard = data.dashboard;

            document.getElementById("users").innerText =
                dashboard.total_users;

            document.getElementById("queues").innerText =
                dashboard.active_queues;

            document.getElementById("waiting").innerText =
                dashboard.people_waiting;

            document.getElementById("average").innerText =
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


// =====================================================
// LOAD ALL QUEUES
// =====================================================

async function loadQueues() {

    try {

        const response = await fetch(
            API + "/api/queue/list"
        );

        if (!response.ok) {
            throw new Error("Queue list request failed");
        }

        const data = await response.json();

        console.log("Queues:", data);

        const select =
            document.getElementById("queueSelect");

        select.innerHTML =
            '<option value="">Select Queue</option>';


        if (data.success && data.queues.length > 0) {

            data.queues.forEach(queue => {

                const option =
                    document.createElement("option");

                option.value = queue.id;

                option.textContent =
                    queue.id + " - " + queue.name;

                select.appendChild(option);
            });

            // Automatically select first queue

            select.value =
                data.queues[0].id;

            loadQueueDetails();
        }

    } catch (error) {

        console.error(
            "Queue loading error:",
            error
        );

        document.getElementById("message").innerText =
            "Could not load queues. Make sure Flask is running.";
    }
}


// =====================================================
// LOAD SELECTED QUEUE DETAILS
// =====================================================

async function loadQueueDetails() {

    const queueId =
        document.getElementById("queueSelect").value;

    if (!queueId) {
        return;
    }

    try {

        const response = await fetch(
            API + "/api/queue/details/" + queueId
        );

        if (!response.ok) {
            throw new Error("Queue details request failed");
        }

        const data = await response.json();

        console.log("Queue details:", data);

        if (data.success) {

            const q = data.queue;


            // Fill input fields

            document.getElementById("queueName").value =
                q.name;

            document.getElementById("serviceType").value =
                q.service_type;

            document.getElementById("activeCounters").value =
                q.active_counters;

            document.getElementById("averageServiceTime").value =
                q.average_service_time;


            // Current details

            document.getElementById("currentQueueName")
                .innerText = q.name;

            document.getElementById("currentServiceType")
                .innerText = q.service_type;

            document.getElementById("currentCounters")
                .innerText = q.active_counters;

            document.getElementById("currentServiceTime")
                .innerText = q.average_service_time;

            document.getElementById("currentPeopleWaiting")
                .innerText = q.people_waiting;


            // Calculate prediction immediately

            calculatePrediction(q);

        }

    } catch (error) {

        console.error(
            "Queue details error:",
            error
        );
    }
}


// =====================================================
// UPDATE QUEUE
// =====================================================

async function updateQueue() {

    console.log("Update Queue button clicked");


    const queueId =
        document.getElementById("queueSelect").value;

    if (!queueId) {

        alert("Please select a queue first.");

        return;
    }


    const queueName =
        document.getElementById("queueName").value;

    const serviceType =
        document.getElementById("serviceType").value;

    const activeCounters =
        document.getElementById("activeCounters").value;

    const averageServiceTime =
        document.getElementById("averageServiceTime").value;


    if (!queueName ||
        !serviceType ||
        !activeCounters ||
        !averageServiceTime) {

        alert("Please fill all queue fields.");

        return;
    }


    try {

        const response = await fetch(
            API + "/api/queue/update/" + queueId,
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
                        Number(activeCounters),

                    average_service_time:
                        Number(averageServiceTime)
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

            document.getElementById("message")
                .innerText =
                "Queue updated successfully!";


            // Reload queue details

            await loadQueueDetails();


            // Get latest dashboard values

            await loadDashboard();

        } else {

            alert(data.message);
        }


    } catch (error) {

        console.error(
            "Update error:",
            error
        );

        alert(
            "Could not update queue. " +
            "Make sure Flask is running."
        );
    }
}


// =====================================================
// CALCULATE PREDICTION
// =====================================================

async function calculatePrediction(queue) {

    const arrivalRate =
        Number(
            document.getElementById("arrivalRate").value
        );


    try {

        const response = await fetch(
            API + "/api/prediction/predict",
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
                        Number(queue.people_waiting),

                    active_counters:
                        Number(queue.active_counters),

                    avg_service_time:
                        Number(queue.average_service_time),

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


            // Selected queue prediction

            document.getElementById(
                "selectedPrediction"
            ).innerText =
                prediction.toFixed(2);


            // Reload dashboard average

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


// =====================================================
// SERVE NEXT CUSTOMER
// =====================================================

async function serveNext() {

    const queueId =
        document.getElementById("queueSelect").value;


    if (!queueId) {

        alert(
            "Please select a queue first."
        );

        return;
    }


    try {

        const response = await fetch(
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

            document.getElementById("message")
                .innerText =
                "Token " +
                data.served_token +
                " served successfully!";


            // Reload queue details

            await loadQueueDetails();


            // Reload dashboard

            await loadDashboard();

        } else {

            alert(data.message);
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


// =====================================================
// WHEN ARRIVAL RATE CHANGES
// RECALCULATE PREDICTION
// =====================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const arrivalInput =
            document.getElementById(
                "arrivalRate"
            );


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
);


// =====================================================
// INITIAL LOAD
// =====================================================

loadDashboard();

loadQueues();