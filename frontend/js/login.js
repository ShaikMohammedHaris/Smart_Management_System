/* =========================================================
   SMART QUEUE MANAGEMENT SYSTEM
   LOGIN JAVASCRIPT
   ========================================================= */

const API = "https://smart-queue-management-system-5vde.onrender.com";

/* =========================================================
   PAGE LOADED
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {
  console.log("=================================");
  console.log("Smart Queue Login JS Loaded");
  console.log("=================================");

  const loginForm = document.getElementById("loginForm");

  const emailInput = document.getElementById("email");

  const passwordInput = document.getElementById("password");

  const message = document.getElementById("message");

  /* =====================================================
       CHECK LOGIN FORM
       ===================================================== */

  if (!loginForm) {
    console.error("ERROR: Login form not found.");

    return;
  }

  console.log("Login form found successfully.");

  /* =====================================================
       LOGIN FORM SUBMIT
       ===================================================== */

  loginForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    console.log("Login button clicked");

    /* =============================================
               GET INPUT VALUES
               ============================================= */

    const email = emailInput.value.trim().toLowerCase();

    const password = passwordInput.value.trim();

    console.log("Email entered:", email);

    /* =============================================
               VALIDATE INPUT
               ============================================= */

    if (!email) {
      message.innerText = "Please enter your email address.";

      message.style.color = "red";

      emailInput.focus();

      return;
    }

    if (!password) {
      message.innerText = "Please enter your password.";

      message.style.color = "red";

      passwordInput.focus();

      return;
    }

    /* =============================================
               SHOW LOGIN STATUS
               ============================================= */

    message.innerText = "Logging in...";

    message.style.color = "#1976d2";

    /*
     * Prevent multiple clicks while
     * login request is running.
     */

    const loginButton = loginForm.querySelector('button[type="submit"]');

    if (loginButton) {
      loginButton.disabled = true;

      loginButton.innerText = "Logging in...";
    }

    /* =============================================
               SEND LOGIN REQUEST
               ============================================= */

    try {
      console.log("Sending request to Flask...");

      console.log("URL:", API + "/api/auth/login");

      const response = await fetch(API + "/api/auth/login", {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          email: email,

          password: password,
        }),
      });

      console.log("Server response status:", response.status);

      /* =========================================
                   READ SERVER RESPONSE
                   ========================================= */

      let data;

      try {
        data = await response.json();
      } catch (jsonError) {
        console.error("Invalid JSON response:", jsonError);

        message.innerText = "Invalid response from server.";

        message.style.color = "red";

        return;
      }

      console.log("Server response:", data);

      /* =========================================
                   LOGIN FAILED
                   ========================================= */

      if (!response.ok || !data.success) {
        message.innerText = data.message || "Invalid email or password.";

        message.style.color = "red";

        console.log("LOGIN FAILED");

        /*
         * Allow user to try again.
         */

        if (loginButton) {
          loginButton.disabled = false;

          loginButton.innerText = "Login";
        }

        return;
      }

      /* =========================================
                   LOGIN SUCCESSFUL
                   ========================================= */

      console.log("=================================");

      console.log("LOGIN SUCCESSFUL");

      console.log("User:", data.user);

      console.log("=================================");

      /* =========================================
                   CHECK USER DATA
                   ========================================= */

      if (!data.user) {
        console.error("User information missing from response.");

        message.innerText =
          "Login successful, but user information is missing.";

        message.style.color = "red";

        if (loginButton) {
          loginButton.disabled = false;

          loginButton.innerText = "Login";
        }

        return;
      }

      /* =========================================
                   SAVE USER INFORMATION
                   ========================================= */

      localStorage.setItem("user", JSON.stringify(data.user));

      /*
       * Remove old queue information
       * when a different user logs in.
       */

      localStorage.removeItem("queue_id");

      localStorage.removeItem("userQueue");

      console.log("User saved in localStorage:");

      console.log(localStorage.getItem("user"));

      /* =========================================
                   SHOW SUCCESS MESSAGE
                   ========================================= */

      message.innerText = "Login successful! Redirecting...";

      message.style.color = "green";

      /* =========================================
                   REDIRECT USER
                   ========================================= */

      setTimeout(function () {
        /*
         * ADMIN
         */

        if (data.user.role && data.user.role.toLowerCase() === "admin") {
          console.log("Redirecting to Admin Dashboard");

          window.location.href = "admin.html";
        } else {

        /*
         * NORMAL USER
         */
          console.log("Redirecting to User Dashboard");

          window.location.href = "dashboard.html";
        }
      }, 500);
    } catch (error) {
      /* =========================================
                   CONNECTION ERROR
                   ========================================= */

      console.error("LOGIN ERROR:", error);

      message.innerText =
        "Cannot connect to server. Make sure Flask is running.";

      message.style.color = "red";

      if (loginButton) {
        loginButton.disabled = false;

        loginButton.innerText = "Login";
      }
    }
  });

  /* =====================================================
       ENTER KEY SUPPORT
       ===================================================== */

  if (emailInput) {
    emailInput.addEventListener("keydown", function (event) {
      if (event.key === "Enter") {
        event.preventDefault();

        passwordInput.focus();
      }
    });
  }

  if (passwordInput) {
    passwordInput.addEventListener("keydown", function (event) {
      if (event.key === "Enter") {
        event.preventDefault();

        loginForm.requestSubmit();
      }
    });
  }
});
