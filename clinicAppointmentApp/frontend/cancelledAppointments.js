document.addEventListener("DOMContentLoaded", async function () {
    const token = localStorage.getItem("token");
    
    if (!token) {
        // Redirect to login if token is missing
        window.location.href = "patientLogin.html";
        return;
    }

    try {
        // Step 1: Get Patient ID from Token
        const patientData = await fetchUserProfile(token);
        if (!patientData || !patientData.userId) {
            throw new Error("Invalid user session.");
        }
        const patientId = patientData.userId;

        // Step 2: Fetch Appointments
        const appointments = await fetchAppointments(patientId);
        if (!appointments.length) {
            document.getElementById("statusMessage").innerText = "No appointments found.";
            return;
        }

        // Step 3: Fetch Doctor Details and Populate Table
        await populateAppointmentsTable(appointments);
    } catch (error) {
        console.error("Error:", error);
        localStorage.removeItem("token");
        window.location.href = "patientLogin.html";
    }
});

// Fetch user profile to get Patient ID
async function fetchUserProfile(token) {
    const response = await fetch("http://127.0.0.1:5000/userprofile", {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        }
    });
    const data = await response.json();
    return data.status ? data : null;
}

// Fetch appointments by patient ID
async function fetchAppointments(patientId) {
    const response = await fetch("http://127.0.0.1:5000/fetchCancelledAppointmentsByPatientId", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ patientId })
    });
    //console.log('>>>>>>',response.json());

    const data = await response.json();
    return data.status ? data.data : [];
}

// Fetch doctor details by ID
async function fetchDoctor(doctorId) {
    try {
        const response = await fetch("http://127.0.0.1:5000/fetchDoctorById", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ doctorId })
        });

        if (!response.ok) {
            // Handle non-200 responses
            const errorData = await response.json();
            console.error("Error fetching doctor:", errorData.error || "Unknown error");
            return null; // Return null when doctor is not found
        }

        const data = await response.json();
        console.log("Doctor Data:", data.data);
        return data.status ? data.data : null;
    } catch (error) {
        console.error("Network error:", error);
        return null;
    }
}

// Populate appointments table
async function populateAppointmentsTable(appointments) {
    const tableBody = document.querySelector("#appointmentsTable tbody");
    tableBody.innerHTML = ""; // Clear existing data

    for (const appt of appointments) {
        const doctor = await fetchDoctor(appt.doctor_id);
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${appt.appointment_date}</td>
            <td>${appt.appointment_time}</td>
            <td>${doctor ? `${doctor.firstName} ${doctor.lastName}` : "Unknown"}</td>
            <td>${doctor ? doctor.specialization : "N/A"}</td>
        `;

        tableBody.appendChild(row);
    }
}

// Logout function
document.getElementById("logoutBtn").addEventListener("click", function () {
    localStorage.removeItem("token");
    window.location.href = "patientLogin.html";
});

// Home button
document.getElementById("homeBtn").addEventListener("click", function () {
    window.location.href = "patientDashboard.html";
});
