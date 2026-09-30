// ============================================================
// SMART QUEUE PREDICTOR
// REGISTER JAVASCRIPT
// ============================================================

const API = "https://smart-queue-management-system-5vde.onrender.com";

console.log("=================================");
console.log("Smart Queue Register JS Loaded");
console.log("=================================");


document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("registerForm");

    const nameInput = document.getElementById("name");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const confirmPasswordInput =
        document.getElementById("confirmPassword");

    const message = document.getElementById("message");

    if (!form) {
        console.error("Register form not found.");
        return;
    }

    console.log("Register form found successfully.");


    // ========================================================
    // SUBMIT
    // ========================================================

    form.addEventListener("submit", async function (event) {

        // VERY IMPORTANT
        // Prevent register.html?name=... URL
        event.preventDefault();

        console.log("Register button clicked");


        const name = nameInput.value.trim();

        const email =
            emailInput.value.trim().toLowerCase();

        const password =
            passwordInput.value;

        const confirmPassword =
            confirmPasswordInput.value;


        console.log("Name:", name);
        console.log("Email:", email);


        message.innerText = "";


        // ====================================================
        // VALIDATION
        // ====================================================

        if (!name) {

            message.innerText =
                "Please enter your full name.";

            message.style.color = "red";

            nameInput.focus();

            return;
        }


        if (!email) {

            message.innerText =
                "Please enter your email address.";

            message.style.color = "red";

            emailInput.focus();

            return;
        }


        const emailPattern =
            /^[^\s@]+@[^\s@]+\.[^\s@]+$/;


        if (!emailPattern.test(email)) {

            message.innerText =
                "Please enter a valid email address.";

            message.style.color = "red";

            emailInput.focus();

            return;
        }


        if (!password) {

            message.innerText =
                "Please enter a password.";

            message.style.color = "red";

            passwordInput.focus();

            return;
        }


        if (password.length < 3) {

            message.innerText =
                "Password must contain at least 3 characters.";

            message.style.color = "red";

            passwordInput.focus();

            return;
        }


        if (password !== confirmPassword) {

            message.innerText =
                "Passwords do not match.";

            message.style.color = "red";

            confirmPasswordInput.focus();

            return;
        }


        // ====================================================
        // BUTTON
        // ====================================================

        const button =
            form.querySelector("button[type='submit']");

        button.disabled = true;

        button.innerText =
            "Creating Account...";


        message.innerText =
            "Creating your account...";

        message.style.color = "#2563eb";


        // ====================================================
        // SEND TO FLASK
        // ====================================================

        try {

            console.log(
                "Sending registration request to Flask..."
            );


            const response = await fetch(
                API + "/api/auth/register",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        name: name,
                        email: email,
                        password: password
                    })
                }
            );


            console.log(
                "Server response status:",
                response.status
            );


            const data =
                await response.json();


            console.log(
                "Server response:",
                data
            );


            // =================================================
            // SUCCESS
            // =================================================

            if (response.ok && data.success) {

                console.log(
                    "REGISTRATION SUCCESS:",
                    email
                );


                message.innerText =
                    "Registration successful! Redirecting to login...";

                message.style.color = "green";


                // Clear form

                form.reset();


                // Redirect to login

                setTimeout(function () {

                    window.location.replace(
                        "login.html"
                    );

                }, 1000);


                return;
            }


            // =================================================
            // DUPLICATE EMAIL
            // =================================================

            if (response.status === 409) {

                message.innerText =
                    "This email is already registered. Please login.";

                message.style.color = "red";

                button.disabled = false;

                button.innerText =
                    "Create Account";

                return;
            }


            // =================================================
            // OTHER ERROR
            // =================================================

            message.innerText =
                data.message ||
                "Registration failed.";

            message.style.color = "red";


            button.disabled = false;

            button.innerText =
                "Create Account";


        } catch (error) {

            console.error(
                "Registration error:",
                error
            );


            message.innerText =
                "Cannot connect to server. Please make sure Flask is running.";

            message.style.color = "red";


            button.disabled = false;

            button.innerText =
                "Create Account";
        }

    });

});