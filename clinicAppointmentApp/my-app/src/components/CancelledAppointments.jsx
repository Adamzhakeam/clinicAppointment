import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const CancelledAppointments = () => {
    const [appointments, setAppointments] = useState([]);
    const [statusMessage, setStatusMessage] = useState("Loading...");
    const navigate = useNavigate();

    useEffect(() => {
        const fetchData = async () => {
            const token = localStorage.getItem("token");

            if (!token) {
                navigate("/patientLogin");
                return;
            }

            try {
                const patientData = await fetchUserProfile(token);
                if (!patientData || !patientData.userId) {
                    throw new Error("Invalid user session.");
                }

                const patientId = patientData.userId;
                const fetchedAppointments = await fetchAppointments(patientId);
                if (!fetchedAppointments.length) {
                    setStatusMessage("No cancelled appointments found.");
                    return;
                }

                const appointmentsWithDoctors = await Promise.all(
                    fetchedAppointments.map(async (appt) => {
                        const doctor = await fetchDoctor(appt.doctor_id);
                        return {
                            ...appt,
                            doctorName: doctor ? `${doctor.firstName} ${doctor.lastName}` : "Unknown",
                            specialization: doctor ? doctor.specialization : "N/A",
                        };
                    })
                );

                setAppointments(appointmentsWithDoctors);
            } catch (error) {
                console.error("Error:", error);
                localStorage.removeItem("token");
                navigate("/patientLogin");
            }
        };

        fetchData();
    }, [navigate]);

    const fetchUserProfile = async (token) => {
        const response = await fetch("http://127.0.0.1:5000/userprofile", {
            method: "POST",
            headers: { "Authorization": `Bearer ${token}`, "Content-Type": "application/json" },
        });
        const data = await response.json();
        return data.status ? data : null;
    };

    const fetchAppointments = async (patientId) => {
        const response = await fetch("http://127.0.0.1:5000/fetchCancelledAppointmentsByPatientId", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ patientId }),
        });
        const data = await response.json();
        return data.status ? data.data : [];
    };

    const fetchDoctor = async (doctorId) => {
        try {
            const response = await fetch("http://127.0.0.1:5000/fetchDoctorById", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ doctorId }),
            });
            const data = await response.json();
            return data.status ? data.data : null;
        } catch (error) {
            console.error("Network error:", error);
            return null;
        }
    };

    return (
        <div className="min-h-screen bg-orange-500 text-white flex flex-col items-center p-6">
            <header className="w-full flex justify-between items-center bg-blue-900 p-4 rounded-lg shadow-lg">
                <h2 className="text-xl font-semibold">My Cancelled Appointments</h2>
                <div className="flex space-x-4">
                    <button className="bg-white text-blue-900 px-4 py-2 rounded-lg" onClick={() => navigate("/patientDashboard")}>
                        🏠 Home
                    </button>
                    <button className="bg-white text-blue-900 px-4 py-2 rounded-lg" onClick={() => {
                        localStorage.removeItem("token");
                        navigate("/patientLogin");
                    }}>
                        🚪 Logout
                    </button>
                </div>
            </header>

            <main className="w-full max-w-4xl mt-6">
                <div className="overflow-x-auto shadow-lg rounded-lg">
                    <table className="w-full border-collapse bg-white text-black rounded-lg">
                        <thead>
                            <tr className="bg-blue-900 text-white">
                                <th className="px-4 py-2">Date</th>
                                <th className="px-4 py-2">Time</th>
                                <th className="px-4 py-2">Doctor</th>
                                <th className="px-4 py-2">Specialization</th>
                            </tr>
                        </thead>
                        <tbody>
                            {appointments.length > 0 ? (
                                appointments.map((appt, index) => (
                                    <tr key={index} className="odd:bg-gray-100 even:bg-gray-200">
                                        <td className="px-4 py-2 text-center">{appt.appointment_date}</td>
                                        <td className="px-4 py-2 text-center">{appt.appointment_time}</td>
                                        <td className="px-4 py-2 text-center">{appt.doctorName}</td>
                                        <td className="px-4 py-2 text-center">{appt.specialization}</td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan="4" className="text-center py-4">{statusMessage}</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </main>
        </div>
    );
};

export default CancelledAppointments;
