import React, { useState } from "react";
import "./Login.css"; // Import the corresponding CSS file for styling

const Login = () => {
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = (e) => {
    e.preventDefault();
    // You can add logic to handle login (e.g., API call to your backend)
    console.log("Phone:", phone, "Password:", password);
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
