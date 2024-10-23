// src/components/DoctorRegistration/DoctorRegistration.js

import React, { useState, useEffect } from 'react';
import './DoctorRegistration.css'; // Import CSS for styling
import axios from 'axios';

const DoctorRegistration = () => {
    const [doctorDetails, setDoctorDetails] = useState({
        firstName: '',
        lastName: '',
        email: '',
        phoneNumber: '',
        password: '',
        specializationId: ''
    });

    const [specializations, setSpecializations] = useState([]);

    useEffect(() => {
        // Fetch specializations from the endpoint
        const fetchSpecializations = async () => {
            try {
                const response = await axios.get('/fetchSpecialisationById');
                setSpecializations(response.data);
            } catch (error) {
                console.error('Error fetching specializations:', error);
            }
        };

        fetchSpecializations();
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setDoctorDetails({ ...doctorDetails, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('/createDoctor', doctorDetails);
            console.log('Doctor registered successfully:', response.data);
            // Optionally reset the form or show a success message
        } catch (error) {
            console.error('Error registering doctor:', error);
            // Handle error appropriately
        }
    };

    return (
        <div className="doctor-registration">
            <h2>Register Doctor</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>First Name</label>
                    <input
                        type="text"
                        name="firstName"
                        value={doctorDetails.firstName}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label>Last Name</label>
                    <input
                        type="text"
                        name="lastName"
                        value={doctorDetails.lastName}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label>Email</label>
                    <input
                        type="email"
                        name="email"
                        value={doctorDetails.email}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label>Phone Number</label>
                    <input
                        type="tel"
                        name="phoneNumber"
                        value={doctorDetails.phoneNumber}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label>Password</label>
                    <input
                        type="password"
                        name="password"
                        value={doctorDetails.password}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label>Specialization</label>
                    <select
                        name="specializationId"
                        value={doctorDetails.specializationId}
                        onChange={handleChange}
                        required
                    >
                        <option value="">Select Specialization</option>
                        {specializations.map((specialization) => (
                            <option key={specialization.id} value={specialization.id}>
                                {specialization.name}
                            </option>
                        ))}
                    </select>
                </div>
                <button type="submit">Register Doctor</button>
            </form>
        </div>
    );
};

export default DoctorRegistration;

