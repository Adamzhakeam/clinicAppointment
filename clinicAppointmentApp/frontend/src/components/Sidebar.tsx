// src/components/Dashboard/Sidebar.tsx

import React from 'react';
import { Link } from 'react-router-dom';
import './dashboard.css';

const Sidebar: React.FC = () => {
  return (
    <div className="sidebar">
      <ul>
        <li><Link to="/adduser">Add User</Link></li>
        <li><Link to="/addpatient">Add Patient</Link></li>
        <li><Link to="/adddoctor">Add Doctor</Link></li>
        <li><Link to="/addspecialization">Add Specialization</Link></li>
        <li><Link to="/addrole">Add Role</Link></li>
      </ul>
    </div>
  );
};

export default Sidebar;
