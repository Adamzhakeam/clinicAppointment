import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import Sidebar from './Sidebar';
import './dashboard.css';

interface UserProfile {
  status: boolean;
  userName: string;
}

const Dashboard: React.FC = () => {
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [greeting, setGreeting] = useState<string>('');
  const navigate = useNavigate(); // Use useNavigate instead of useHistory

  // Memoize fetchUserProfile function using useCallback
  const fetchUserProfile = useCallback(async (token: string) => {
    try {
      const response = await axios.post('/userprofile', {}, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (response.data.status) {
        setUserProfile(response.data);
        setGreeting(getGreeting());
      }
    } catch (error) {
      console.error('Error fetching user profile:', error);
      // Handle error (e.g., redirect to login)
    }
  }, []);

  // Check if user is logged in and has a token
  useEffect(() => {
    const token = localStorage.getItem('authToken');
    if (!token) {
      navigate('/login'); // Redirect to login if no token is found
    } else {
      fetchUserProfile(token);
    }
  }, [navigate, fetchUserProfile]); // Add fetchUserProfile to dependencies

  const getGreeting = (): string => {
    const hours = new Date().getHours();
    if (hours < 12) return 'Good Morning';
    else if (hours < 18) return 'Good Afternoon';
    else return 'Good Evening';
  };

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    navigate('/login'); // Use navigate for redirection
  };

  return (
    <div className="dashboard-container">
      <Sidebar />
      <div className="dashboard-content">
        <header className="dashboard-header">
          <h1>{greeting}, {userProfile?.userName}</h1>
          <button onClick={handleLogout} className="logout-button">Logout</button>
        </header>

        <div className="dashboard-cards">
          <div className="card">
            <h3>Confirmed Appointments</h3>
            <p>10</p>
          </div>
          <div className="card">
            <h3>Pending Appointments</h3>
            <p>5</p>
          </div>
          <div className="card">
            <h3>Cancelled Appointments</h3>
            <p>2</p>
          </div>
          <div className="card">
            <h3>Appointments</h3>
            <p>20</p>
          </div>
          <div className="card">
            <h3>Patients</h3>
            <p>200</p>
          </div>
          <div className="card">
            <h3>Doctors</h3>
            <p>15</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
