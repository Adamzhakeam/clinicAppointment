// src/components/PatientRegistration/PatientRegistration.js

import React, { useState } from 'react';
import './PatientRegistration.css'; // Import CSS for styling
import axios from 'axios';

const PatientRegistration = () => {
    const [patientDetails, setPatientDetails] = useState({
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        password: '',
        description: 'no description' // Default value for description
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setPatientDetails({ ...patientDetails, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('/createPatient', patientDetails);
            console.log('Patient registered successfully:', response.data);
            // Optionally reset the form or show a success message
        } catch (error) {
            console.error('Error registering patient:', error);
            // Handle error appropriately
        }
    };

    return (
        <div className="patient-registration">
            <h2>Register Patient</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>First Name</label>
                    <input
                        type="text"
                        name="firstName"
                        value={patientDetails.firstName}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label>Last Name</label>
                    <input
                        type="text"
                        name="lastName"
                        value={patientDetails.lastName}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label>Email</label>
                    <input
                        type="email"
                        name="email"
                        value={patientDetails.email}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label>Phone</label>
                    <input
                        type="tel"
                        name="phone"
                        value={patientDetails.phone}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label>Password</label>
                    <input
                        type="password"
                        name="password"
                        value={patientDetails.password}
                        onChange={handleChange}
                        required
                    />
                </div>
                {/* The description field is not visible to the user */}
                <input type="hidden" name="description" value={patientDetails.description} />
                <button type="submit">Register Patient</button>
            </form>
        </div>
    );
};

export default PatientRegistration;

