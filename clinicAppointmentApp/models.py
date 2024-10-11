from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(200), nullable=False)
#     phone = db.Column(db.String(15), unique=True, nullable=False)
#     roleId = db.Column(db.String(50), db.ForeignKey('roles.id'),nullable=False)
#     birthdate = db.Column(db.Date, nullable=True)  # New Column
    
#     roles = db.relationship('Roles', back_populates='users')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(15), unique=True,nullable=False)
    roleId = db.Column(db.String(50),db.ForeignKey('roles.id',name='fk_users_roles') , nullable=False)
    others = db.Column(db.String(255),nullable = True)
    
    
    roles = db.relationship('Roles', back_populates='users')

class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True,nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='doctor')
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    birthDate = db.Column(db.String(10),nullable=True)
    others = db.Column(db.String(255),nullable=True)
    
    department = db.relationship('Department', back_populates='doctors')

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='patient')
    birthDate = db.Column(db.String(10),nullable=True)
    others = db.Column(db.String(255),nullable=True)

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    others = db.Column(db.String(255),nullable=True)
    
    doctors = db.relationship('Doctor', back_populates='department')

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    appointment_time = db.Column(db.String(10),nullable=False)
    appointment_status = db.Column(db.String(10),nullable=False)
    
    doctor = db.relationship('Doctor', backref='appointments')
    patient = db.relationship('Patient', backref='appointments')
    
class Roles(db.Model):
    __tablename__='roles'
    id = db.Column(db.Integer, primary_key=True)
    roleName = db.Column(db.String(20), nullable=False)
    others = db.Column(db.String(255),nullable = True)
    
    user = db.relationship('User',back_populates='roles')
