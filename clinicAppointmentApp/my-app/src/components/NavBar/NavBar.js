import React from "react";
import { Link } from "react-router-dom";

function NavBar() {
  return (
    <nav className="bg-gray-100 p-4 shadow-md mb-6">
      <div className="flex space-x-4 justify-center">
        <Link
          to="/"
          className="px-4 py-2 text-gray-700 hover:bg-gray-200 rounded transition duration-200"
        >
          Login
        </Link>
        <Link
          to="/dashboard"
          className="px-4 py-2 text-gray-700 hover:bg-gray-200 rounded transition duration-200"
        >
          Dashboard
        </Link>
        <Link
          to="/create-user"
          className="px-4 py-2 text-gray-700 hover:bg-gray-200 rounded transition duration-200"
        >
          Create User
        </Link>
        <Link
          to="/register-doctor"
          className="px-4 py-2 text-gray-700 hover:bg-gray-200 rounded transition duration-200"
        >
          Doctor Registration
        </Link>
        <Link
          to="/register-specialisation"
          className="px-4 py-2 text-gray-700 hover:bg-gray-200 rounded transition duration-200"
        >
          Register Specialisation
        </Link>
        <Link
          to="/patient-login"
          className="px-4 py-2 text-gray-700 hover:bg-gray-200 rounded transition duration-200"
        >
          Patient Login
        </Link>
      </div>
    </nav>
  );
}

export default NavBar;