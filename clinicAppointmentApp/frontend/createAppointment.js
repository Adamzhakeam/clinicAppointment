document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem("token");
    if (!token) {
        alert("You are not logged in. Redirecting to login page.");
        window.location.href = "patientLogin.html";
        return;
    }

    let anonymous;

    const patientNameElement = document.getElementById('patientName');
    const greetingElement = document.getElementById('greeting');
    const specializationSelect = document.getElementById('specialization');
    const doctorSelect = document.getElementById('doctor');
    const appointmentForm = document.getElementById('appointmentForm');

    // Fetch user profile
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
            anonymous = data.userId; // Store patient ID globally
            console.log("Fetched patient ID (anonymous):", anonymous);

            patientNameElement.textContent = userName;

            const currentHour = new Date().getHours();
            greetingElement.textContent =
                currentHour < 12
                    ? `Good Morning, ${userName}!`
                    : currentHour < 18
                    ? `Good Afternoon, ${userName}!`
                    : `Good Evening, ${userName}!`;
        } else {
            throw new Error("Invalid user profile");
        }
    } catch (error) {
        console.error("Error fetching user profile:", error);
        localStorage.removeItem("token");
        window.location.href = "patientLogin.html";
    }

    // Fetch specializations
    try {
        const response = await fetch("http://127.0.0.1:5000/fetchAllSpecialisations", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
        });

        const data = await response.json();
        data.data.forEach((spec) => {
            const option = document.createElement('option');
            option.value = spec.specializationId;
            option.textContent = spec.specializationName;
            specializationSelect.appendChild(option);
        });
    } catch (error) {
        console.error("Error fetching specializations:", error);
    }

    // Fetch doctors based on specialization
    specializationSelect.addEventListener('change', async (event) => {
        const specializationId = event.target.value;

        if (!specializationId) return;

        doctorSelect.innerHTML = '<option value="">Select Doctor</option>';
        try {
            const response = await fetch("http://127.0.0.1:5000/fetchAllDoctors", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
            });

            const data = await response.json();
            const doctors = data.filter(doc => doc.specialization == specializationId);
            doctors.forEach((doctor) => {
                const option = document.createElement('option');
                option.value = doctor.doctorId;
                option.textContent = `${doctor.firstName} ${doctor.lastName}`;
                doctorSelect.appendChild(option);
            });
        } catch (error) {
            console.error("Error fetching doctors:", error);
        }
    });

    // Capture and format appointment time
    const appointmentTimeInput = document.getElementById('appointmentTime');
    appointmentTimeInput.addEventListener('change', () => {
        if (appointmentTimeInput.value) {
            appointmentTimeInput.dataset.formattedTime = appointmentTimeInput.value + ":00"; // Append seconds
        }
    });

    // Submit appointment form
    appointmentForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        if (!anonymous) {
            alert("Patient ID not loaded. Please refresh the page.");
            return;
        }

        const formattedTime = appointmentTimeInput.dataset.formattedTime || (appointmentTimeInput.value ? appointmentTimeInput.value + ":00" : "");

        const formData = {
            doctor_id: doctorSelect.value,
            patient_id: anonymous,
            appointment_date: document.getElementById('appointmentDate').value,
            appointment_time: formattedTime, // Ensure HH:MM:SS format
            appointment_status: "Pending",
            description: document.getElementById('description').value,
        };

        console.log("Form data being sent:", formData); // Debugging payload

        try {
            const response = await fetch("http://127.0.0.1:5000/createAppointment", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify(formData),
            });

            const data = await response.json();
            alert(data.log || data.error || "Appointment successfully created!"); // Wait for user to press "OK"
            
            // Reset the form after alert is acknowledged
            appointmentForm.reset();  
        } catch (error) {
            console.error("Error submitting appointment:", error);
            alert("An error occurred while creating the appointment. Please try again.");
        }
    });
});
