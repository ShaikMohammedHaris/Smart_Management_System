// ============================================================
// SMART QUEUE PREDICTOR - LOGIN
// File:
// frontend/js/login.js
// ============================================================

const API = "http://127.0.0.1:5000";

// ============================================================
// LOGIN PAGE INITIALIZATION
// ============================================================

document.addEventListener("DOMContentLoaded", function () {

    console.log("=================================");
    console.log("Smart Queue Login JS Loaded");
    console.log("=================================");

    const loginForm = document.getElementById("loginForm");

    if (!loginForm) {
        console.error("ERROR: loginForm was not found!");
        return;
    }

    console.log("Login form found successfully.");

    // ========================================================
    // LOGIN FORM SUBMIT
    // ========================================================

    loginForm.addEventListener("submit", async function (event) {

        // Prevent normal HTML form submission
        event.preventDefault();

        console.log("---------------------------------");
        console.log("Login button clicked");
        console.log("---------------------------------");

        // Get input elements
        const emailInput = document.getElementById("email");
        const passwordInput = document.getElementById("password");
        const message = document.getElementById("message");
        const loginButton = document.getElementById("loginButton");

        // Safety check
        if (!emailInput || !passwordInput) {

            console.error(
                "Email or password input was not found."
            );

            return;
        }

        // Get values
        const email = emailInput.value.trim();
        const password = passwordInput.value;

        console.log("Email entered:", email);

        // ====================================================
        // VALIDATION
        // ====================================================

        if (!email) {

            message.innerText =
                "Please enter your email address.";

            message.style.color = "red";

            emailInput.focus();

            return;
        }

        if (!password) {

            message.innerText =
                "Please enter your password.";

            message.style.color = "red";

            passwordInput.focus();

            return;
        }

        // ====================================================
        // SHOW LOGIN PROCESS
        // ====================================================

        if (loginButton) {

            loginButton.disabled = true;
            loginButton.innerText = "Logging in...";

        }

        message.innerText = "Checking login details...";
        message.style.color = "#333";

        // ====================================================
        // SEND LOGIN REQUEST TO FLASK
        // ====================================================

        try {

            console.log("Sending request to Flask...");
            console.log(
                "URL:",
                API + "/api/auth/login"
            );

            const response = await fetch(
                API + "/api/auth/login",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        email: email,
                        password: password
                    })
                }
            );

            console.log(
                "Server response status:",
                response.status
            );

            // =================================================
            // GET JSON RESPONSE
            // =================================================

            const data = await response.json();

            console.log(
                "Server response:",
                data
            );

            // =================================================
            // SUCCESSFUL LOGIN
            // =================================================

            if (response.ok && data.success) {

                console.log(
                    "LOGIN SUCCESSFUL"
                );

                console.log(
                    "User:",
                    data.user
                );

                // ---------------------------------------------
                // Save logged-in user
                // ---------------------------------------------

                localStorage.setItem(
                    "user",
                    JSON.stringify(data.user)
                );

                console.log(
                    "User information saved to localStorage."
                );

                // ---------------------------------------------
                // Show success message
                // ---------------------------------------------

                message.innerText =
                    "Login successful! Redirecting...";

                message.style.color = "green";

                // ---------------------------------------------
                // Redirect according to role
                // ---------------------------------------------

                setTimeout(function () {

                    if (
                        data.user &&
                        data.user.role === "admin"
                    ) {

                        console.log(
                            "Admin user detected."
                        );

                        console.log(
                            "Redirecting to admin dashboard..."
                        );

                        window.location.href =
                            "admin.html";

                    } else {

                        console.log(
                            "Normal user detected."
                        );

                        console.log(
                            "Redirecting to user dashboard..."
                        );

                        window.location.href =
                            "dashboard.html";
                    }

                }, 800);

                return;
            }

            // =================================================
            // INVALID LOGIN
            // =================================================

            console.log(
                "LOGIN FAILED"
            );

            message.innerText =
                data.message ||
                "Invalid email or password.";

            message.style.color = "red";

            if (loginButton) {

                loginButton.disabled = false;
                loginButton.innerText = "Login";

            }

        }

        // ====================================================
        // SERVER / NETWORK ERROR
        // ====================================================

        catch (error) {

            console.error(
                "Login request error:",
                error
            );

            message.innerText =
                "Cannot connect to the server.";

            message.style.color = "red";

            if (loginButton) {

                loginButton.disabled = false;
                loginButton.innerText = "Login";

            }

            console.log(
                "Make sure Flask is running on port 5000."
            );

        }

    });

});