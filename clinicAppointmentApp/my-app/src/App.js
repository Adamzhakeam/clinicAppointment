import React from "react";
// import NavBar from "./components/NavBar/NavBar";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import NavBar from "./components/NavBar/NavBar"; // Navigation Bar
import Login from "./components/Login/Login";
import UserDashboard from "./components/UserDashboard/UserDashboard";
import UserRegistration from "./components/UserRegistration/UserRegistration";
import DoctorRegistration from "./components/DoctorRegistration/DoctorRegistration";
import PatientRegistration from "./components/PatientRegistration/PatientRegistration";

function App() {
  return (
    <Router>
      <div className="App">
        <NavBar />
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/dashboard" element={<UserDashboard />} />
          <Route path="/register-user" element={<UserRegistration />} />
          <Route path="/register-doctor" element={<DoctorRegistration />} />
          <Route path="/register-patient" element={<PatientRegistration />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
