// app/login/page.tsx

'use client'; // Add this directive to mark the component as a client component

import React, { useState } from 'react';
import styles from './page.module.css'; // Import the CSS Module

const Login = () => {
  const [phoneNumber, setPhoneNumber] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Phone Number:', phoneNumber);
    console.log('Password:', password);
  };

  return (
    <div className={styles['login-container']}>
      <div className={styles['login-form']}>
        {/* Apply the login-header class to the h2 element */}
        <h2 className={styles['login-header']}>Login</h2>
        <form onSubmit={handleSubmit}>
          <div className={styles['input-group']}>
            <label htmlFor="phone-number">Phone Number</label>
            <input
              type="text"
              id="phone-number"
              placeholder="Enter your phone number"
              value={phoneNumber}
              onChange={(e) => setPhoneNumber(e.target.value)}
              required
            />
          </div>
          <div className={styles['input-group']}>
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className={styles['login-button']}>Login</button>
        </form>
      </div>
    </div>
  );
};

export default Login;
