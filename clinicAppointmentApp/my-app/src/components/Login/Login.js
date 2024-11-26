import React, { useState } from "react";
import axios from "axios"; // Import axios
import "./Login.css"; // Import the corresponding CSS file for styling

const Login = () => {
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(""); // To store error messages (if any)

  const handleLogin = async (e) => {
    e.preventDefault();
    
    // Check if the phone number and password are entered
    if (!phone || !password) {
      setError("Phone number and password are required");
      return;
    }

    try {
      // Make the POST request to the backend
      const response = await axios.post(
        "http://127.0.0.1:5000/logIn", // Your backend endpoint
        { phone, password }
      );

      // Handle the successful response
      if (response.data.status) {
        // Store the token in localStorage
        localStorage.setItem("token", response.data.token);
        
        // Redirect to the dashboard (you can use react-router to navigate)
        window.location.href = "/UserDashboard"; // You can use `navigate("/dashboard")` if you're using react-router
      } else {
        setError(response.data.log); // Show error message from backend
      }
    } catch (error) {
      console.error("Error during login:", error);
      setError("An error occurred. Please try again.");
    }
  };

  const handleForgotPassword = () => {
    // This can be a redirect or a modal opening, depending on your routing setup
    alert("Forgot password clicked!");
  };

  return (
    <div className="login-container">
      <h2 className="login-title">Login</h2>
      <form onSubmit={handleLogin} className="login-form">
        <div className="input-group">
          <label>Phone Number</label>
          <input
            type="text"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            placeholder="Enter phone number"
            required
          />
        </div>
        <div className="input-group">
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter password"
            required
          />
        </div>
        {error && <p className="error-message">{error}</p>} {/* Show error message if any */}
        <button type="submit" className="login-button">
          Login
        </button>
        <p className="forgot-password" onClick={handleForgotPassword}>
          Forgot Password?
        </p>
      </form>
    </div>
  );
};

export default Login;
