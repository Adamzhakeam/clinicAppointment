import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const PatientDashboard = () => {
  const [userName, setUserName] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      alert("You are not logged in. Redirecting to login page.");
      navigate("/patientLogin");
      return;
    }

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
          setUserName(data.userName);
        } else {
          alert("Error fetching user details.");
          localStorage.removeItem("token");
          navigate("/patientLogin");
        }
      } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while fetching your details.");
      }
    };
    fetchUserProfile();
  }, [navigate]);

  const getGreeting = () => {
    const currentHour = new Date().getHours();
    if (currentHour < 12) return `Good Morning, ${userName}!`;
    if (currentHour < 18) return `Good Afternoon, ${userName}!`;
    return `Good Evening, ${userName}!`;
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/patientLogin");
  };

  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <div className="w-64 bg-gray-900 text-white flex flex-col p-5">
        <h2 className="text-lg font-bold mb-5">Patient Dashboard</h2>
        <nav className="space-y-4">
          <a href="#" className="block py-2 px-4 bg-gray-800 rounded">Home</a>
          <a href="#" className="block py-2 px-4 bg-gray-800 rounded">Appointments</a>
          <a href="#" className="block py-2 px-4 bg-gray-800 rounded">Settings</a>
        </nav>
        <button onClick={handleLogout} className="mt-auto bg-red-500 text-white py-2 px-4 rounded">
          Logout
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 p-6">
        <h2 className="text-2xl font-bold mb-6">{getGreeting()}</h2>

        {/* Cards Section */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white shadow-lg p-6 text-center rounded-lg hover:scale-105 transition">
            <h5 className="text-lg font-semibold">Schedule Appointment</h5>
            <p className="text-gray-600">View available slots and schedule a new appointment.</p>
            <a href="/createAppointment" className="block mt-4 bg-blue-500 text-white py-2 px-4 rounded">
              Schedule
            </a>
          </div>

          <div className="bg-white shadow-lg p-6 text-center rounded-lg hover:scale-105 transition">
            <h5 className="text-lg font-semibold">Cancelled Appointments</h5>
            <p className="text-gray-600">View your previously cancelled appointments.</p>
            <a href="/cancelledAppointments" className="block mt-4 bg-yellow-500 text-white py-2 px-4 rounded">
              View
            </a>
          </div>

          <div className="bg-white shadow-lg p-6 text-center rounded-lg hover:scale-105 transition">
            <h5 className="text-lg font-semibold">Confirmed Appointments</h5>
            <p className="text-gray-600">View and manage your confirmed appointments.</p>
            <a href="/confirmedAppointments" className="block mt-4 bg-green-500 text-white py-2 px-4 rounded">
              View
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PatientDashboard;
