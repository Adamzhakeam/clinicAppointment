import React from "react";
import { Link } from "react-router-dom";

function NavBar() {
  return (
    <nav style={{ marginBottom: "20px", background: "#f4f4f4", padding: "10px" }}>
      <Link to="/" style={{ margin: "0 10px" }}>Login</Link>
      <Link to="/dashboard" style={{ margin: "0 10px" }}>Dashboard</Link>
      <Link to="/register-user" style={{ margin: "0 10px" }}>User Registration</Link>
      <Link to="/register-doctor" style={{ margin: "0 10px" }}>Doctor Registration</Link>
      <Link to="/register-patient" style={{ margin: "0 10px" }}>Patient Registration</Link>
    </nav>
  );
}

export default NavBar;
