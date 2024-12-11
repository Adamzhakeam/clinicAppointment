document.addEventListener("DOMContentLoaded", function () {
    const token = localStorage.getItem("token");

    // Redirect if not authenticated
    if (!token) {
        window.location.href = "index.html";
        return;
    }

    // Fetch user details for authentication and greet the user
    fetch("http://127.0.0.1:5000/userprofile", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (!data.status) {
                // Token is invalid or user is not authenticated
                localStorage.removeItem("token");
                window.location.href = "index.html";
                return;
            }

            // If authenticated, display greeting
            const userName = data.userName;
            const greeting = document.getElementById("greeting") || document.createElement("p");
            greeting.id = "greeting";

            const hour = new Date().getHours();
            const timeOfDay =
                hour < 12
                    ? "Good Morning"
                    : hour < 18
                    ? "Good Afternoon"
                    : "Good Evening";

            greeting.textContent = `${timeOfDay}, ${userName}`;
            document.querySelector(".header").appendChild(greeting);
        });

    // Logout button functionality
    document.getElementById("logoutButton")?.addEventListener("click", function () {
        localStorage.removeItem("token");
        window.location.href = "index.html";
    });

    // Home button functionality
    document.getElementById("homeButton").addEventListener("click", function () {
        window.location.href = "dashboard.html";
    });

    // Handle form submission for creating a specialisation
    document.getElementById("specialisationForm").addEventListener("submit", async function (e) {
        e.preventDefault();

        const specializationName = document.getElementById("specializationName").value;
        const responseMessage = document.getElementById("responseMessage");
        responseMessage.textContent = "";
        responseMessage.className = "";

        try {
            const response = await fetch("http://127.0.0.1:5000/createSpecialisation", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({ specializationName }),
            });

            const data = await response.json();

            if (data.status) {
                responseMessage.textContent = data.log;
                responseMessage.className = "success";
                document.getElementById("specialisationForm").reset();
            } else {
                responseMessage.textContent = `Error: ${data.log}`;
                responseMessage.className = "error";
            }
        } catch (error) {
            responseMessage.textContent = "An error occurred. Please try again.";
            responseMessage.className = "error";
        }
    });
});
