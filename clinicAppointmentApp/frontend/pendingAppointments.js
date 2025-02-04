document.addEventListener("DOMContentLoaded", async function () {
    const token = localStorage.getItem("token");

    // Redirect if no token
    if (!token) {
        window.location.href = "index.html";
        return;
    }

    async function fetchAppointments() {
        const response = await fetch("http://127.0.0.1:5000/fetchAllPendingAppointments", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }
        });

        const data = await response.json();
        const tableBody = document.getElementById("appointmentsTable");
        tableBody.innerHTML = "";

        if (!data.status) {
            tableBody.innerHTML = `<tr><td colspan="6">No pending appointments</td></tr>`;
            return;
        }

        for (const appointment of data.log) {
            const { appointment_date, appointment_time, doctor_id, patient_id } = appointment;

            const doctor = await fetchDoctorById(doctor_id);
            const patient = await fetchPatientById(patient_id);

            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${appointment_date}</td>
                <td>${appointment_time}</td>
                <td>${doctor}</td>
                <td>${patient}</td>
                <td>General Checkup</td>
                <td>
                    <button class="confirm" onclick="confirmAppointment('${doctor_id}', '${patient_id}')">Confirm</button>
                    <button class="cancel" onclick="cancelAppointment('${doctor_id}', '${patient_id}')">Cancel</button>
                </td>
            `;

            tableBody.appendChild(row);
        }
    }

    fetchAppointments(); // Load appointments on page load

    // Logout functionality
    document.getElementById("logoutBtn").addEventListener("click", () => {
        localStorage.removeItem("token");
        window.location.href = "index.html";
    });

    // Redirect to dashboard
    document.getElementById("homeBtn").addEventListener("click", () => {
        window.location.href = "dashboard.html";
    });
});

// ✅ Move functions to the global scope
async function confirmAppointment(doctorId, patientId) {
    const token = localStorage.getItem("token");
    const response = await fetch("http://127.0.0.1:5000/confirmAppointment", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ doctorId, patientId })
    });

    const data = await response.json();
    alert(data.log || "Appointment confirmed!");
    location.reload(); // Refresh the table
}

async function cancelAppointment(doctorId, patientId) {
    const token = localStorage.getItem("token");
    const response = await fetch("http://127.0.0.1:5000/cancelAppointment", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ doctorId, patientId })
    });

    const data = await response.json();
    alert(data.log || "Appointment canceled!");
    location.reload(); // Refresh the table
}

// Fetch doctor name
async function fetchDoctorById(doctorId) {
    const token = localStorage.getItem("token");
    const response = await fetch("http://127.0.0.1:5000/fetchDoctorById", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ doctorId })
    });

    const data = await response.json();
    return data.status ? `${data.data.firstName} ${data.data.lastName}` : "Unknown Doctor";
}

// Fetch patient name
async function fetchPatientById(patientId) {
    const token = localStorage.getItem("token");
    const response = await fetch("http://127.0.0.1:5000/fetchPatientById", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ patientId })
    });

    const data = await response.json();
    return data.status ? `${data.log.firstName} ${data.log.lastName}` : "Unknown Patient";
}
