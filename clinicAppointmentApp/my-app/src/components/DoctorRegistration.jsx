import { useState, useEffect } from "react";

const DoctorRegistration = () => {
  const [specializations, setSpecializations] = useState([]);
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    phone: "",
    specializationId: "",
  });
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchSpecializations = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/fetchAllSpecialisations", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
        });
        const data = await response.json();
        if (data.status) {
          setSpecializations(data.data);
        } else {
          console.error("Error fetching specializations:", data.log);
        }
      } catch (error) {
        console.error("Error:", error);
      }
    };
    fetchSpecializations();
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    setError("");
    try {
      const response = await fetch("http://127.0.0.1:5000/createDoctor", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify(formData),
      });
      const data = await response.json();
      if (data.status) {
        setMessage(`${formData.firstName} has been successfully registered!`);
        setFormData({ firstName: "", lastName: "", email: "", phone: "", specializationId: "" });
      } else {
        setError(`Error: ${data.log}`);
      }
    } catch (error) {
      setError("An error occurred while registering the doctor.");
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <div className="bg-white shadow-lg rounded-lg p-6 max-w-lg w-full">
        <h3 className="text-xl font-bold text-center text-blue-600">Doctor Registration</h3>
        {message && <p className="text-green-600 text-center mt-2">{message}</p>}
        {error && <p className="text-red-600 text-center mt-2">{error}</p>}
        <form onSubmit={handleSubmit} className="mt-4 space-y-4">
          <input type="text" name="firstName" value={formData.firstName} onChange={handleChange} placeholder="First Name" required className="w-full p-2 border rounded" />
          <input type="text" name="lastName" value={formData.lastName} onChange={handleChange} placeholder="Last Name" required className="w-full p-2 border rounded" />
          <input type="email" name="email" value={formData.email} onChange={handleChange} placeholder="Email" required className="w-full p-2 border rounded" />
          <input type="tel" name="phone" value={formData.phone} onChange={handleChange} placeholder="Phone Number" required className="w-full p-2 border rounded" />
          <select name="specializationId" value={formData.specializationId} onChange={handleChange} required className="w-full p-2 border rounded">
            <option value="">Select Specialization</option>
            {specializations.map((spec) => (
              <option key={spec.specializationId} value={spec.specializationId}>{spec.specializationName}</option>
            ))}
          </select>
          <button type="submit" className="w-full bg-blue-600 text-white p-2 rounded">Register Doctor</button>
        </form>
      </div>
    </div>
  );
};

export default DoctorRegistration;
