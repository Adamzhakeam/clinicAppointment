// Function to fetch and display dashboard statistics
async function fetchDashboardStats() {
  try {
      // Fetch pending appointments
      const pendingResponse = await fetch("http://localhost:5000/fetchAllPendingAppointments", {
          method: "POST",
          headers: { "Content-Type": "application/json" }
      });
      const pendingData = await pendingResponse.json();
      document.getElementById("pendingAppointments").textContent = pendingData.status ? pendingData.log.length : 0;

      // Fetch confirmed appointments
      const confirmedResponse = await fetch("http://localhost:5000/fetchAllConfirmedAppointments", {
          method: "POST",
          headers: { "Content-Type": "application/json" }
      });
      const confirmedData = await confirmedResponse.json();
      document.getElementById("confirmedAppointments").textContent = confirmedData.status ? confirmedData.log.length : 0;

      // Fetch cancelled appointments
      const cancelledResponse = await fetch("http://localhost:5000/fetchAllCancelledAppointments", {
          method: "POST",
          headers: { "Content-Type": "application/json" }
      });
      const cancelledData = await cancelledResponse.json();
      document.getElementById("cancelledAppointments").textContent = cancelledData.status ? cancelledData.log.length : 0;

      // Calculate total appointments
      const totalAppointments = 
          (pendingData.status ? pendingData.log.length : 0) +
          (confirmedData.status ? confirmedData.log.length : 0) +
          (cancelledData.status ? cancelledData.log.length : 0);
      document.getElementById("appointments").textContent = totalAppointments;
      
  } catch (error) {
      console.error("Error fetching dashboard statistics:", error);
  }
}

// Call function on page load
window.onload = async () => {
  const token = localStorage.getItem("token");

  if (!token) {
      window.location.href = "index.html"; // Redirect to login if no token found
  }

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
          const hour = new Date().getHours();
          let greetingMessage = "Good Morning";
          if (hour >= 12 && hour < 18) greetingMessage = "Good Afternoon";
          else if (hour >= 18) greetingMessage = "Good Evening";

          document.getElementById("greeting").textContent = `${greetingMessage}, ${data.userName}`;
          document.getElementById("userInfo").textContent = `Role: ${data.role}`;
      } else {
          alert("Error fetching user profile.");
      }
  } catch (error) {
      console.error("Error:", error);
      alert("Error fetching user profile.");
  }

  // Fetch dashboard statistics
  fetchDashboardStats();
};

// Logout function
document.getElementById("logoutBtn").addEventListener("click", () => {
  localStorage.removeItem("token"); // Remove token from localStorage
  window.location.href = "index.html"; // Redirect to login page
});
