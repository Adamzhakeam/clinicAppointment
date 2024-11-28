document.addEventListener("DOMContentLoaded", function () {
    const token = localStorage.getItem("token");
  
    // Redirect if not authenticated
    if (!token) {
      window.location.href = "index.html";
      return;
    }
  
    // Fetch user details and greet
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
          localStorage.removeItem("token");
          window.location.href = "index.html";
          return;
        }
  
        const userName = data.userName;
        const greeting = document.getElementById("greeting");
  
        const hour = new Date().getHours();
        const timeOfDay =
          hour < 12
            ? "Good Morning"
            : hour < 18
            ? "Good Afternoon"
            : "Good Evening";
  
        greeting.textContent = `${timeOfDay}, ${userName}`;
      });
  
    // Logout button functionality
    document.getElementById("logoutButton").addEventListener("click", function () {
      localStorage.removeItem("token");
      window.location.href = "index.html";
    });
  
    // Home button functionality
    document.getElementById("homeButton").addEventListener("click", function () {
      window.location.href = "dashboard.html";
    });
  
    // Form submission
    document
      .getElementById("createUserForm")
      .addEventListener("submit", async function (e) {
        e.preventDefault();
  
        const firstName = document.getElementById("firstName").value;
        const lastName = document.getElementById("lastName").value;
        const email = document.getElementById("email").value;
        const phone = document.getElementById("phone").value;
        const password = document.getElementById("password").value;
        const roleId = document.getElementById("roleId").value;
  
        const messageBox = document.getElementById("messageBox");
        messageBox.textContent = "";
        messageBox.className = "";
  
        const payload = {
          firstName,
          lastName,
          email,
          phone,
          password,
          roleId,
        };
  
        try {
          const response = await fetch("http://127.0.0.1:5000/createUser", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify(payload),
          });
  
          const data = await response.json();
  
          if (data.status) {
            messageBox.textContent = data.log;
            messageBox.className = "success";
            document.getElementById("createUserForm").reset();
          } else {
            messageBox.textContent = `Error: ${data.log}`;
            messageBox.className = "error";
          }
        } catch (error) {
          messageBox.textContent = "An error occurred. Please try again.";
          messageBox.className = "error";
        }
      });
  });
  