from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    userId = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    roleId = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)  # Corrected Foreign Key
    
    role = db.relationship('Roles', back_populates='users')  # Relationship

class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    specializationId = db.Column(db.Integer, db.ForeignKey('specialisations.id'), nullable=False)  # Corrected Foreign Key
    
    specialization = db.relationship('Specialisation', back_populates='doctors')  # Corrected relationship

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(255))  # Added description column
    role = db.Column(db.String(50), nullable=False, default='patient')

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    appointment_time = db.Column(db.String(10), nullable=False)
    appointment_status = db.Column(db.String(10), nullable=False)

    doctor = db.relationship('Doctor', backref='appointments')
    patient = db.relationship('Patient', backref='appointments')

class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    roleName = db.Column(db.String(20), nullable=False)
    others = db.Column(db.String(255), nullable=True)
    
    users = db.relationship('User', back_populates='role')  # Corrected relationship

class Specialisation(db.Model):
    __tablename__ = 'specialisations'
    id = db.Column(db.Integer, primary_key=True)
    specializationName = db.Column(db.String(20), nullable=False)  # Fixed the column name
    others = db.Column(db.String(255), nullable=True)

    doctors = db.relationship('Doctor', back_populates='specialization')  # Fixed relationship

# New Model for Appointment Confirmation

class AppointmentConfirmation(db.Model):
    __tablename__ = 'appointment_confirmations'
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    confirmed_by = db.Column(db.Integer, db.ForeignKey('users.userId'), nullable=False)  # Front desk user confirming the appointment
    confirmation_status = db.Column(db.String(50), nullable=False)  # e.g., "Confirmed", "Pending", "Canceled"
    confirmation_date = db.Column(db.DateTime, nullable=False)

    appointment = db.relationship('Appointment', backref='confirmation')
    confirmed_by_user = db.relationship('User', backref='confirmed_appointments')
    
class DoctorAvailability(db.Model):
    __tablename__ = 'doctor_availabilities'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    available_date = db.Column(db.Date, nullable=False)
    max_appointments = db.Column(db.Integer, nullable=False, default=4)  # Maximum appointments allowed per day
    current_appointments = db.Column(db.Integer, nullable=False, default=0)  # Track how many are currently booked

    doctor = db.relationship('Doctor', backref='availabilities')

