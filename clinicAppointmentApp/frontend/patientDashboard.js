document.addEventListener("DOMContentLoaded", async () => {
    const patientNameElement = document.getElementById("patientName");
    const greetingElement = document.getElementById("greeting");
  
    // Fetch user profile data
    const token = localStorage.getItem("token");
    if (!token) {
      alert("You are not logged in. Redirecting to login page.");
      window.location.href = "patientLogin.html";
      return;
    }
  
    try {
      const response = await fetch("http://127.0.0.1:5000/userprofile", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });
  
      const data = await response.json();
  
      if (data.status) {
        const userName = data.userName;
        patientNameElement.textContent = userName;
  
        // Customize greeting based on time
        const currentHour = new Date().getHours();
        if (currentHour < 12) {
          greetingElement.textContent = `Good Morning, ${userName}!`;
        } else if (currentHour < 18) {
          greetingElement.textContent = `Good Afternoon, ${userName}!`;
        } else {
          greetingElement.textContent = `Good Evening, ${userName}!`;
        }
      } else {
        alert("Error fetching user details.");
        localStorage.removeItem("token");
        window.location.href = "patientLogin.html";
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while fetching your details.");
    }
  
    // Logout functionality
    const logoutButton = document.getElementById("logoutButton");
    logoutButton.addEventListener("click", () => {
      localStorage.removeItem("token");
      window.location.href = "patientLogin.html";
    });
  });
  