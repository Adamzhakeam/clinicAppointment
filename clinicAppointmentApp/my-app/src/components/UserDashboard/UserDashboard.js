import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './UserDashboard.css'; // Import custom CSS for styling

const UserDashboard = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState({});
  const [greeting, setGreeting] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('token');

    if (!token) {
      navigate('/login'); // Redirect to login if no token is found
    } else {
      fetchUserProfile(token);
    }

    setGreetingBasedOnTime();
  }, []);

  const fetchUserProfile = async (token) => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/userprofile', {}, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (response.data.status) {
        setUser(response.data);
      } else {
        navigate('/login'); // Redirect to login if token validation fails
      }
    } catch (error) {
      console.error('Error fetching user profile:', error);
      navigate('/login'); // Redirect to login on error
    }
  };

  const setGreetingBasedOnTime = () => {
    const hour = new Date().getHours();
    if (hour < 12) setGreeting('Good Morning');
    else if (hour < 18) setGreeting('Good Afternoon');
    else setGreeting('Good Evening');
  };

  const handleLogout = () => {
    localStorage.removeItem('token'); // Remove token from local storage
    navigate('/login'); // Redirect to login
  };

  return (
    <div className="dashboard">
      <aside className="sidebar">
        <h2>Dashboard</h2>
        <ul>
          <li>Add User</li>
          <li>Add Patient</li>
          <li>Add Doctor</li>
          <li>Add Specialisation</li>
          <li>Add Role</li>
        </ul>
        <button className="logout-btn" onClick={handleLogout}>Logout</button>
      </aside>
      <main className="main-content">
        <header>
          <h1>{greeting}, {user.userName || 'User'}!</h1>
        </header>
        <section className="cards">
          <div className="card">Confirmed Appointments</div>
          <div className="card">Pending Appointments</div>
          <div className="card">Cancelled Appointments</div>
          <div className="card">Appointments</div>
        </section>
        <section className="cards">
          <div className="card">Patients</div>
          <div className="card">Doctors</div>
        </section>
      </main>
    </div>
  );
};

export default UserDashboard;
