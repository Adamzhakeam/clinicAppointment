import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const RegisterSpecialisation = () => {
  const [specializationName, setSpecializationName] = useState("");
  const [responseMessage, setResponseMessage] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/");
    } else {
      fetch("http://127.0.0.1:5000/userprofile", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (!data.status) {
            localStorage.removeItem("token");
            navigate("/");
          }
        });
    }
  }, [navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    setResponseMessage("");

    try {
      const response = await fetch("http://127.0.0.1:5000/createSpecialisation", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ specializationName }),
      });

      const data = await response.json();
      if (data.status) {
        setResponseMessage(data.log);
        setSpecializationName("");
      } else {
        setResponseMessage(`Error: ${data.log}`);
      }
    } catch (error) {
      setResponseMessage("An error occurred. Please try again.");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <div className="bg-white shadow-lg rounded-lg p-6 max-w-md w-full">
        <header className="flex justify-between items-center mb-4">
          <h1 className="text-xl font-bold text-green-600">Register Specialisation</h1>
          <button
            onClick={() => navigate("/dashboard")}
            className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
          >
            Home
          </button>
        </header>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block font-semibold mb-1">Specialisation Name:</label>
            <input
              type="text"
              value={specializationName}
              onChange={(e) => setSpecializationName(e.target.value)}
              placeholder="Enter specialisation name"
              required
              className="w-full p-2 border border-gray-300 rounded focus:ring focus:ring-green-200"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700"
          >
            Create Specialisation
          </button>
        </form>

        {responseMessage && (
          <div className="mt-4 text-center text-green-600 font-semibold">
            {responseMessage}
          </div>
        )}
      </div>
    </div>
  );
};

export default RegisterSpecialisation;
