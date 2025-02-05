import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const CreateUser = () => {
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    phone: "",
    password: "",
    roleId: "",
  });
  const [message, setMessage] = useState("");
  const [userName, setUserName] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/");
      return;
    }

    fetch("http://127.0.0.1:5000/userprofile", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        if (!data.status) {
          localStorage.removeItem("token");
          navigate("/");
          return;
        }
        setUserName(data.userName);
      });
  }, [navigate]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.id]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    setMessage("");

    try {
      const response = await fetch("http://127.0.0.1:5000/createUser", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(formData),
      });
      const data = await response.json();
      setMessage(data.status ? data.log : `Error: ${data.log}`);
      if (data.status) setFormData({ firstName: "", lastName: "", email: "", phone: "", password: "", roleId: "" });
    } catch (error) {
      setMessage("An error occurred. Please try again.");
    }
  };

  return (
    <div className="max-w-lg mx-auto bg-white p-6 mt-10 rounded-lg shadow-md">
      <header className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold text-green-700">Good {new Date().getHours() < 12 ? "Morning" : new Date().getHours() < 18 ? "Afternoon" : "Evening"}, {userName}</h2>
        <div className="flex gap-2">
          <button className="bg-green-700 text-white px-4 py-2 rounded-md" onClick={() => navigate("/dashboard")}>Home</button>
          <button className="bg-red-600 text-white px-4 py-2 rounded-md" onClick={() => { localStorage.removeItem("token"); navigate("/"); }}>Logout</button>
        </div>
      </header>
      <h1 className="text-center text-2xl font-bold mb-4">Create User</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        {Object.keys(formData).map((key) => (
          <div key={key} className="flex flex-col">
            <label htmlFor={key} className="font-semibold capitalize">{key.replace("Id", " ID")}</label>
            <input type={key === "password" ? "password" : "text"} id={key} value={formData[key]} onChange={handleChange} className="p-2 border border-green-700 rounded" required />
          </div>
        ))}
        <button type="submit" className="w-full bg-green-700 text-white py-2 rounded-md hover:bg-green-800">Create User</button>
      </form>
      {message && <div className={`mt-4 p-2 text-center rounded ${message.startsWith("Error") ? "bg-red-500 text-white" : "bg-green-500 text-white"}`}>{message}</div>}
    </div>
  );
};

export default CreateUser;
