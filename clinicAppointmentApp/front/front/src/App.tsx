import React, { useState } from 'react';

const Login = () => {
  // States to manage form inputs, error messages, and loading state
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [token, setToken] = useState('');

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); // Prevent form from submitting the traditional way
    setLoading(true); // Set loading state to true
    setError(''); // Clear any previous errors

    // Prepare the payload for the POST request
    const payload = {
      phone: phone,
      password: password
    };

    try {
      // Make the POST request to the Flask backend
      const response = await fetch('http://127.0.0.1:5000/logIn', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload) // Send the phone and password as JSON
      });

      // Check if the response is successful (status code 2xx)
      if (!response.ok) {
        console.error('Failed to connect to the server. Status:', response.status);
        setError('Failed to connect to the server.');
        return;
      }

      // Parse the response JSON
      const data = await response.json();
      console.log("Response Data:", data); // Log the response to debug

      // Check the status of the login
      if (data.status) {
        // If login is successful, save the token and log success
        setToken(data.token);
        console.log('Login successful! Token:', data.token);
      } else {
        // If login failed, show the error message from the backend
        setError(data.log);
        console.log('Login failed:', data.log);
      }
    } catch (error) {
      // If an error occurs during the fetch process
      console.error('An error occurred:', error);
      setError('An error occurred while logging in.');
    } finally {
      // Turn off loading state after the request finishes
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Phone Number:</label>
          <input
            type="text"
            value={phone}
            onChange={(e) => setPhone(e.target.value)} // Update phone number state
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)} // Update password state
            required
          />
        </div>
        <button type="submit" >
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>

      {/* Display error message */}
      {error && <div className="error">{error}</div>}

      {/* If login is successful, display the token */}
      {token && <div>Logged in successfully. Token: {token}</div>}
    </div>
  );
};

export default Login;
