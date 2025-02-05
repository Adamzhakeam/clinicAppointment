import { useEffect, useState } from "react";

export default function Dashboard() {
  const [stats, setStats] = useState({
    confirmedAppointments: 0,
    pendingAppointments: 0,
    cancelledAppointments: 0,
    totalAppointments: 0,
    patients: 0,
    doctors: 0,
  });

  const [user, setUser] = useState({ name: "", role: "" });

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      window.location.href = "/";
      return;
    }

    fetch("http://localhost:5000/userprofile", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.status) {
          setUser({ name: data.userName, role: data.role });
        } else {
          alert("Error fetching user profile.");
        }
      })
      .catch(() => alert("Error fetching user profile."));

    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const endpoints = [
        "fetchAllPendingAppointments",
        "fetchAllConfirmedAppointments",
        "fetchAllCancelledAppointments",
      ];
      
      const responses = await Promise.all(
        endpoints.map((endpoint) =>
          fetch(`http://localhost:5000/${endpoint}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
          }).then((res) => res.json())
        )
      );
      
      const [pendingData, confirmedData, cancelledData] = responses;
      setStats({
        pendingAppointments: pendingData.status ? pendingData.log.length : 0,
        confirmedAppointments: confirmedData.status ? confirmedData.log.length : 0,
        cancelledAppointments: cancelledData.status ? cancelledData.log.length : 0,
        totalAppointments:
          (pendingData.status ? pendingData.log.length : 0) +
          (confirmedData.status ? confirmedData.log.length : 0) +
          (cancelledData.status ? cancelledData.log.length : 0),
      });
    } catch (error) {
      console.error("Error fetching dashboard stats:", error);
    }
  };

  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <aside className="w-64 bg-green-700 text-white p-5 fixed h-full">
        <h2 className="text-xl text-center font-bold mb-6">Admin Dashboard</h2>
        <ul className="space-y-3">
          <li><a href="createUser.html" className="block hover:bg-green-600 p-2">Add User</a></li>
          <li><a href="#" className="block hover:bg-green-600 p-2">Add Patient</a></li>
          <li><a href="doctorRegistration.html" className="block hover:bg-green-600 p-2">Add Doctor</a></li>
          <li><a href="registerSpecialisation.html" className="block hover:bg-green-600 p-2">Add Specialisation</a></li>
          <li><a href="#" className="block hover:bg-green-600 p-2">Add Role</a></li>
        </ul>
        <button 
          className="mt-6 w-full bg-red-600 hover:bg-red-700 p-2 rounded text-white" 
          onClick={() => { localStorage.removeItem("token"); window.location.href = "/"; }}
        >Logout</button>
      </aside>

      {/* Main Content */}
      <main className="ml-64 p-6 w-full">
        <h1 className="text-2xl font-bold">{`Hello, ${user.name}`}</h1>
        <p className="text-gray-600 mb-6">Role: {user.role}</p>
        
        {/* Dashboard Cards */}
        <div className="grid grid-cols-3 gap-4">
          <div className="bg-white p-6 shadow rounded text-center">
            <h3 className="text-lg font-semibold">Confirmed Appointments</h3>
            <p className="text-2xl font-bold text-green-700">{stats.confirmedAppointments}</p>
          </div>
          <div className="bg-white p-6 shadow rounded text-center">
            <h3 className="text-lg font-semibold">Pending Appointments</h3>
            <p className="text-2xl font-bold text-green-700">{stats.pendingAppointments}</p>
          </div>
          <div className="bg-white p-6 shadow rounded text-center">
            <h3 className="text-lg font-semibold">Cancelled Appointments</h3>
            <p className="text-2xl font-bold text-green-700">{stats.cancelledAppointments}</p>
          </div>
          <div className="bg-white p-6 shadow rounded text-center">
            <h3 className="text-lg font-semibold">Total Appointments</h3>
            <p className="text-2xl font-bold text-green-700">{stats.totalAppointments}</p>
          </div>
          <div className="bg-white p-6 shadow rounded text-center">
            <h3 className="text-lg font-semibold">Patients</h3>
            <p className="text-2xl font-bold text-green-700">{stats.patients}</p>
          </div>
          <div className="bg-white p-6 shadow rounded text-center">
            <h3 className="text-lg font-semibold">Doctors</h3>
            <p className="text-2xl font-bold text-green-700">{stats.doctors}</p>
          </div>
        </div>
      </main>
    </div>
  );
}
