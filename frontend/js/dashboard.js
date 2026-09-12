const user =
    JSON.parse(
        localStorage.getItem("user")
    );

if (!user) {

    window.location.href =
        "login.html";
}

document.getElementById("welcome")
    .innerText =
    "Welcome " + user.name;


async function joinQueue() {

    const queueId =
        document.getElementById(
            "queueId"
        ).value;

    const response = await fetch(
        "http://127.0.0.1:5000/api/queue/join",
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({
                queue_id: Number(queueId),
                user_id: user.id
            })
        }
    );

    const data =
        await response.json();

    if (data.success) {

        document.getElementById(
            "token"
        ).innerText =
            "Token: " +
            data.token_number;

    } else {

        alert(data.message);
    }
}


async function predictTime() {

    const queueId =
        document.getElementById(
            "queueId"
        ).value;

    const queueLength =
        document.getElementById(
            "queueLength"
        ).value;

    const counters =
        document.getElementById(
            "counters"
        ).value;

    const serviceTime =
        document.getElementById(
            "serviceTime"
        ).value;

    const arrivalRate =
        document.getElementById(
            "arrivalRate"
        ).value;


    const response = await fetch(
        "http://127.0.0.1:5000/api/prediction/predict",
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
                    Number(queueLength),

                active_counters:
                    Number(counters),

                avg_service_time:
                    Number(serviceTime),

                arrival_rate:
                    Number(arrivalRate)
            })
        }
    );


    const data =
        await response.json();


    if (data.success) {

        document.getElementById(
            "prediction"
        ).innerText =
            "Predicted Waiting Time: " +
            data.predicted_waiting_time +
            " minutes";

    } else {

        alert(data.message);
    }
}