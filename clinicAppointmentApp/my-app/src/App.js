import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import NavBar from "./components/NavBar/NavBar"; // Navigation Bar
import Login from "./components/Login"; // Root/Index Page
import Dashboard from "./components/Dashboard"; // Dashboard Page
import CreateUser from "./components/CreateUser"; // Create User Page
import DoctorRegistration from "./components/DoctorRegistration"; // Doctor Registration Page
import RegisterSpecialisation from "./components/RegisterSpecialisation"; // Specialization Registration Page
import CreateAppointment from "./components/CreateAppointment"; // Create Appointment Page
import PatientLogin from "./components/PatientLogin"; // Patient Login Page
import PatientDashboard from "./components/PatientDashboard"; // Patient Dashboard Page
import ConfirmedAppointments from "./components/ConfirmedAppointments"; // Confirmed Appointments Page
import CancelledAppointments from "./components/CancelledAppointments"; // Cancelled Appointments Page

function App() {
  return (
    <Router>
      <div className="App">
        <NavBar />
        <Routes>
          {/* Root/Index Route */}
          <Route path="/" element={<Login />} />

          {/* Dashboard Route */}
          <Route path="/dashboard" element={<Dashboard />} />

          {/* User Management Routes */}
          <Route path="/create-user" element={<CreateUser />} />
          <Route path="/register-doctor" element={<DoctorRegistration />} />
          <Route path="/register-specialisation" element={<RegisterSpecialisation />} />

          {/* Appointment Management Routes */}
          <Route path="/create-appointment" element={<CreateAppointment />} />
          <Route path="/confirmed-appointments" element={<ConfirmedAppointments />} />
          <Route path="/cancelled-appointments" element={<CancelledAppointments />} />

          {/* Patient-Specific Routes */}
          <Route path="/patient-login" element={<PatientLogin />} />
          <Route path="/patient-dashboard" element={<PatientDashboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;