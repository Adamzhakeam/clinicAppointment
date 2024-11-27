// script.js

// Fetch user profile from the backend after checking if the token exists in localStorage
window.onload = async () => {
    const token = localStorage.getItem("token");
  
    if (!token) {
      window.location.href = "login.html"; // Redirect to login if no token found
    }
  
    // Fetch user profile data from the backend
    try {
      const response = await fetch("http://localhost:5000/userprofile", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });
  
      const data = await response.json();
  
      if (data.status) {
        // Greet user based on the time of the day
        const hour = new Date().getHours();
        let greetingMessage = "Good Morning";
  
        if (hour >= 12 && hour < 18) {
          greetingMessage = "Good Afternoon";
        } else if (hour >= 18 && hour < 24) {
          greetingMessage = "Good Evening";
        }
  
        // Display the greeting message and user details
        document.getElementById("greeting").textContent = `${greetingMessage}, ${data.userName}`;
        document.getElementById("userInfo").textContent = `Role: ${data.role}`;
      } else {
        alert("Error fetching user profile.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Error fetching user profile.");
    }
  
    // Get dashboard statistics (appointments, users)
    fetchDashboardStats();
  };
  
  // Function to fetch and display dashboard statistics (appointments, users)
  async function fetchDashboardStats() {
    try {
      const response = await fetch("http://localhost:5000/dashboardStats", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });
  
      const stats = await response.json();
  
      if (stats.status) {
        document.getElementById("confirmedAppointments").textContent = stats.confirmedAppointments;
        document.getElementById("pendingAppointments").textContent = stats.pendingAppointments;
        document.getElementById("cancelledAppointments").textContent = stats.cancelledAppointments;
        document.getElementById("appointments").textContent = stats.totalAppointments;
        document.getElementById("patients").textContent = stats.totalPatients;
        document.getElementById("doctors").textContent = stats.totalDoctors;
      } else {
        alert("Error fetching dashboard statistics.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Error fetching dashboard statistics.");
    }
  }
  
  // Logout function
  document.getElementById("logoutBtn").addEventListener("click", () => {
    localStorage.removeItem("token"); // Remove token from localStorage
    window.location.href = "login.html"; // Redirect to login page
  });
  