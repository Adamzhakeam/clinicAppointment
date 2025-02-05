import React, { useEffect, useState } from "react";

const AppointmentForm = () => {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [patientName, setPatientName] = useState("");
  const [patientId, setPatientId] = useState(null);
  const [specializations, setSpecializations] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [selectedSpecialization, setSelectedSpecialization] = useState("");
  const [formData, setFormData] = useState({
    doctor_id: "",
    appointment_date: "",
    appointment_time: "",
    description: "",
  });

  useEffect(() => {
    if (!token) {
      alert("You are not logged in. Redirecting to login page.");
      window.location.href = "patientLogin.html";
    }

    fetchUserProfile();
    fetchSpecializations();
  }, [token]);

  const fetchUserProfile = async () => {
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
        setPatientName(data.userName);
        setPatientId(data.userId);
      } else {
        throw new Error("Invalid user profile");
      }
    } catch (error) {
      console.error("Error fetching user profile:", error);
      localStorage.removeItem("token");
      window.location.href = "patientLogin.html";
    }
  };

  const fetchSpecializations = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/fetchAllSpecialisations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });
      const data = await response.json();
      setSpecializations(data.data);
    } catch (error) {
      console.error("Error fetching specializations:", error);
    }
  };

  const fetchDoctors = async (specializationId) => {
    try {
      const response = await fetch("http://127.0.0.1:5000/fetchAllDoctors", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });
      const data = await response.json();
      setDoctors(data.filter(doc => doc.specialization === specializationId));
    } catch (error) {
      console.error("Error fetching doctors:", error);
    }
  };

  const handleSpecializationChange = (event) => {
    const specializationId = event.target.value;
    setSelectedSpecialization(specializationId);
    fetchDoctors(specializationId);
  };

  const handleInputChange = (event) => {
    setFormData({ ...formData, [event.target.id]: event.target.value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!patientId) {
      alert("Patient ID not loaded. Please refresh the page.");
      return;
    }
    try {
      const response = await fetch("http://127.0.0.1:5000/createAppointment", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          ...formData,
          patient_id: patientId,
          appointment_status: "Pending",
          appointment_time: formData.appointment_time + ":00",
        }),
      });
      const data = await response.json();
      alert(data.log || data.error || "Appointment successfully created!");
    } catch (error) {
      console.error("Error submitting appointment:", error);
      alert("An error occurred while creating the appointment. Please try again.");
    }
  };

  return (
    <div>
      <header>
        <h1>{`Welcome, ${patientName}`}</h1>
        <a href="../../clinicAppointmentApp/frontend/patientDashboard.html">
          <button>Home</button>
        </a>
      </header>
      <main>
        <h2>Book an Appointment</h2>
        <form onSubmit={handleSubmit}>
          <label htmlFor="specialization">Specialization:</label>
          <select id="specialization" value={selectedSpecialization} onChange={handleSpecializationChange} required>
            <option value="">Select Specialization</option>
            {specializations.map((spec) => (
              <option key={spec.specializationId} value={spec.specializationId}>
                {spec.specializationName}
              </option>
            ))}
          </select>

          <label htmlFor="doctor">Doctor:</label>
          <select id="doctor" value={formData.doctor_id} onChange={handleInputChange} required>
            <option value="">Select Doctor</option>
            {doctors.map((doctor) => (
              <option key={doctor.doctorId} value={doctor.doctorId}>
                {doctor.firstName} {doctor.lastName}
              </option>
            ))}
          </select>

          <label htmlFor="appointment_date">Appointment Date:</label>
          <input type="date" id="appointment_date" value={formData.appointment_date} onChange={handleInputChange} required />

          <label htmlFor="appointment_time">Appointment Time:</label>
          <input type="time" id="appointment_time" value={formData.appointment_time} onChange={handleInputChange} required />

          <label htmlFor="description">Description:</label>
          <textarea id="description" rows="4" value={formData.description} onChange={handleInputChange} placeholder="Brief description of your concern" />

          <button type="submit">Set Appointment</button>
        </form>
      </main>
    </div>
  );
};

export default AppointmentForm;
