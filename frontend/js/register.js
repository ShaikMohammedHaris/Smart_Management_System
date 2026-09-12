async function register() {

    const name =
        document.getElementById("name").value;

    const email =
        document.getElementById("email").value;

    const password =
        document.getElementById("password").value;

    const response = await fetch(
        "http://127.0.0.1:5000/api/auth/register",
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({
                name: name,
                email: email,
                password: password
            })
        }
    );

    const data = await response.json();

    document.getElementById("message")
        .innerText = data.message;

    if (data.success) {

        setTimeout(() => {

            window.location.href =
                "login.html";

        }, 1000);
    }
}