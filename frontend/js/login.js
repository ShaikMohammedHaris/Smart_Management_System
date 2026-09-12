async function login() {

    const email =
        document.getElementById("email").value;

    const password =
        document.getElementById("password").value;

    const response = await fetch(
        "http://127.0.0.1:5000/api/auth/login",
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({
                email: email,
                password: password
            })
        }
    );

    const data = await response.json();

    document.getElementById("message")
        .innerText = data.message;

    if (data.success) {

        localStorage.setItem(
            "user",
            JSON.stringify(data.user)
        );

        if (data.user.role === "admin") {

            window.location.href =
                "admin.html";

        } else {

            window.location.href =
                "dashboard.html";
        }
    }
}