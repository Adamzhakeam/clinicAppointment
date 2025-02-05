import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const PatientAppointments = () => {
    const [appointments, setAppointments] = useState([]);
    const [statusMessage, setStatusMessage] = useState("");
    const navigate = useNavigate();
    
    useEffect(() => {
        const token = localStorage.getItem("token");
        if (!token) {
            navigate("/patientLogin");
            return;
        }
        
        const fetchAppointments = async () => {
            try {
                const patientData = await fetchUserProfile(token);
                if (!patientData || !patientData.userId) throw new Error("Invalid session");
                
                const fetchedAppointments = await getAppointments(patientData.userId);
                if (!fetchedAppointments.length) {
                    setStatusMessage("No appointments found.");
                    return;
                }
                
                const populatedAppointments = await Promise.all(
                    fetchedAppointments.map(async (appt) => {
                        const doctor = await fetchDoctor(appt.doctor_id);
                        return {
                            date: appt.appointment_date,
                            time: appt.appointment_time,
                            doctor: doctor ? `${doctor.firstName} ${doctor.lastName}` : "Unknown",
                            specialization: doctor ? doctor.specialization : "N/A"
                        };
                    })
                );
                
                setAppointments(populatedAppointments);
            } catch (error) {
                console.error("Error:", error);
                localStorage.removeItem("token");
                navigate("/patientLogin");
            }
        };

        fetchAppointments();
    }, [navigate]);
    
    const fetchUserProfile = async (token) => {
        const response = await fetch("http://127.0.0.1:5000/userprofile", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        });
        const data = await response.json();
        return data.status ? data : null;
    };

    const getAppointments = async (patientId) => {
        const response = await fetch("http://127.0.0.1:5000/fetchAppointmentsByPatientId", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ patientId })
        });
        const data = await response.json();
        return data.status ? data.data : [];
    };

    const fetchDoctor = async (doctorId) => {
        try {
            const response = await fetch("http://127.0.0.1:5000/fetchDoctorById", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ doctorId })
            });
            if (!response.ok) return null;
            const data = await response.json();
            return data.status ? data.data : null;
        } catch (error) {
            console.error("Network error:", error);
            return null;
        }
    };

    return (
        <div className="bg-[#0a0f36] min-h-screen text-white flex flex-col items-center p-6">
            <header className="w-full flex justify-between items-center bg-[#09102b] p-4">
                <h2 className="text-xl font-bold">My Appointments</h2>
                <div className="space-x-4">
                    <button onClick={() => navigate("/patientDashboard")} className="bg-white text-[#0a0f36] px-4 py-2 rounded-md font-bold">🏠 Home</button>
                    <button onClick={() => { localStorage.removeItem("token"); navigate("/patientLogin"); }} className="bg-white text-[#0a0f36] px-4 py-2 rounded-md font-bold">🚪 Logout</button>
                </div>
            </header>
            <main className="w-full max-w-4xl mt-6">
                <div className="overflow-x-auto">
                    <table className="w-full border-collapse bg-white text-black shadow-md rounded-lg">
                        <thead>
                            <tr className="bg-[#0a0f36] text-white">
                                <th className="p-3 border">Date</th>
                                <th className="p-3 border">Time</th>
                                <th className="p-3 border">Doctor</th>
                                <th className="p-3 border">Specialization</th>
                            </tr>
                        </thead>
                        <tbody>
                            {appointments.length > 0 ? (
                                appointments.map((appt, index) => (
                                    <tr key={index} className="hover:bg-gray-200">
                                        <td className="p-3 border">{appt.date}</td>
                                        <td className="p-3 border">{appt.time}</td>
                                        <td className="p-3 border">{appt.doctor}</td>
                                        <td className="p-3 border">{appt.specialization}</td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan="4" className="p-3 border text-center">{statusMessage}</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </main>
        </div>
    );
};

export default PatientAppointments;
