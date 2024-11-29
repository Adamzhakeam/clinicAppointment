'''
    this module is meant to handle all the database logic and all the logic of 
    the application for example all the logic for inserting,updating,altering,
    deleting to the database 
'''

# import kisa_utils as kutils
from models import db, User, Doctor,Specialisation , Appointment, Roles, Patient,DoctorAvailability

# ---- Users database logic ----
def insertUser(userDetails: dict) -> dict:
    '''
    Inserts a user into the database.
    @param userDetails: dictionary with keys: 'firstName', 'lastName', 'email', 'phone', 'password', 'roleId'
    '''
    passwordHash = userDetails['password']
    newUser = User(
        firstName=userDetails['firstName'],
        lastName=userDetails['lastName'],
        email=userDetails['email'],
        phone=userDetails['phone'],
        password=passwordHash,
        roleId=userDetails['roleId']
    )
    db.session.add(newUser)
    db.session.commit()
    # print('>>>>>>>',newUser)
    return newUser

def fetchAllUsers():
    '''
    Fetches all users from the database.
    '''
    allUsers = User.query.all()
    response = [{'firstName': user.firstName, 'lastName': user.lastName, "email": user.email, "phone": user.phone, "roleId": user.roleId} for user in allUsers]
    return response

def fetchUserByPhoneNumber(userDetails: dict):
    '''
    Fetches a user by their phone number.
    @param userDetails: dictionary with 'phone' key
    '''
    user = User.query.filter_by(phone=userDetails['phone']).first()
    if user:
        response = {'firstName': user.firstName, 'lastName': user.lastName, 'email': user.email, 'phone': user.phone}
        return response
    return {"error": "User not found"}, 404

def fetchUserById(userDetails: dict):
    '''
    Fetches a user by their ID.
    @param userDetails: dictionary with 'userId' key
    '''
    user = User.query.filter_by(userId=userDetails['userId']).first()
    if user:
        response = {'firstName': user.firstName, 'lastName': user.lastName, 'email': user.email, 'phone': user.phone, 'roleId': user.roleId}
        return response
    return {"error": "User not found"}, 404

from werkzeug.security import check_password_hash

def login(credentials:dict)->dict:
    '''
    Validates phone number and password for login.

    Parameters:
        credentials (dict): A dictionary containing 'phone' and 'password'.

    Returns:
        dict: A dictionary with 'status' as a boolean and 'log' containing user details if successful.
    '''
    phone = credentials.get('phone')
    password = credentials.get('password')

    # Validate input
    if not phone or not password:
        return {'status': False, 'log': 'Phone number and password are required'}

    # Fetch the user by phone number
    user = User.query.filter_by(phone=phone).first()
    if not user:
        return {'status': False, 'log': 'Invalid phone number '}

    # Check if the password matches
    if user.password != password:
        return {'status': False, 'log': 'Invalid  password'}

    # If validation succeeds
    return {
        'status': True,
        'log': {
            'userId': user.userId,
            'roleId': user.roleId,
            'firstName': user.firstName,
            'lastName': user.lastName
        }
    }

def patientLogin(credentials:dict)->dict:
    '''
    Validates phone number and password for login.

    Parameters:
        credentials (dict): A dictionary containing 'phone' and 'password'.

    Returns:
        dict: A dictionary with 'status' as a boolean and 'log' containing user details if successful.
    '''
    phone = credentials.get('phone')
    password = credentials.get('password')

    # Validate input
    if not phone or not password:
        return {'status': False, 'log': 'Phone number and password are required'}

    # Fetch the user by phone number
    user = Patient.query.filter_by(phone=phone).first()
    if not user:
        return {'status': False, 'log': 'Invalid phone number '}

    # Check if the password matches
    if user.password != password:
        return {'status': False, 'log': 'Invalid  password'}

    # If validation succeeds
    return {
        'status': True,
        'log': {
            'userId': user.id,
            'roleId': user.role,
            'firstName': user.firstName,
            'lastName': user.lastName
        }
    }



# ---- Doctors database logic ----
def insertDoctor(doctorDetails: dict) -> dict:
    '''
    Inserts a doctor into the database.
    @param doctorDetails: dictionary with keys: 'firstName', 'lastName', 'email', 'phone', 'specialization',
    '''
    # passwordHash = doctorDetails['password']
    newDoctor = Doctor(
        firstName=doctorDetails['firstName'],
        lastName=doctorDetails['lastName'],
        email=doctorDetails['email'],
        phone=doctorDetails['phone'],
        specializationId=doctorDetails['specializationId'],
        # password=passwordHash,
        # department_id=doctorDetails['department_id']
    )
    db.session.add(newDoctor)
    db.session.commit()
    return newDoctor

def fetchAllDoctors():
    '''
    Fetches all doctors from the database.
    '''
    doctors = Doctor.query.all()
    response = [{'firstName': doctor.firstName, 'lastName': doctor.lastName, "email": doctor.email, "phone": doctor.phone, "specialization": doctor.specialization} for doctor in doctors]
    return response

def fetchDoctorByPhoneNumber(doctorDetails: dict):
    '''
    Fetches a doctor by their phone number.
    @param doctorDetails: dictionary with 'phoneNumber' key
    '''
    doctor = Doctor.query.filter_by(phone=doctorDetails['phoneNumber']).first()
    if doctor:
        response = {'firstName': doctor.firstName, 'lastName': doctor.lastName, 'email': doctor.email, 'phone': doctor.phone}
        return response
    return {"error": "Doctor not found"}, 404

def fetchDoctorById(doctorDetails: dict):
    '''
    Fetches a doctor by their ID.
    @param doctorDetails: dictionary with 'doctorId' key
    '''
    doctor = Doctor.query.filter_by(id=doctorDetails['doctorId']).first()
    if doctor:
        response = {'firstName': doctor.firstName, 'lastName': doctor.lastName, 'email': doctor.email, 'phone': doctor.phone, 'specialization': doctor.specialization}
        return response
    return {"error": "Doctor not found"}, 404

# ---- Patients database logic ----
def insertPatient(patientDetails: dict) -> dict:
    '''
    Inserts a patient into the database.
    @param patientDetails: dictionary with keys: 'firstName', 'lastName', 'email', 'phone', 'password'
    '''
    passwordHash = patientDetails['password']
    newPatient = Patient(
        firstName=patientDetails['firstName'],
        lastName=patientDetails['lastName'],
        email=patientDetails['email'],
        phone=patientDetails['phone'],
        password=passwordHash
    )
    db.session.add(newPatient)
    db.session.commit()
    return newPatient

def fetchAllPatients():
    '''
    Fetches all patients from the database.
    '''
    patients = Patient.query.all()
    response = [{'firstName': patient.firstName, 'lastName': patient.lastName, "email": patient.email, "phone": patient.phone} for patient in patients]
    return response

# # ---- Departments database logic ----
# def insertDepartment(departmentDetails: dict) -> dict:
#     '''
#     Inserts a department into the database.
#     @param departmentDetails: dictionary with key 'name'
#     '''
#     newDepartment = Department(name=departmentDetails['name'])
#     db.session.add(newDepartment)
#     db.session.commit()
#     return newDepartment

# def fetchAllDepartments():
#     '''
#     Fetches all departments from the database.
#     '''
#     departments = Department.query.all()
#     response = [{'departmentName': department.name} for department in departments]
#     return response

# def fetchDepartmentById(departmentDetails: dict):
#     '''
#     Fetches a department by its ID.
#     @param departmentDetails: dictionary with 'departmentId' key
#     '''
#     department = Department.query.filter_by(id=departmentDetails['departmentId']).first()
#     if department:
#         response = {'departmentName': department.name, 'departmentId': department.id}
#         return response
#     return {"error": "Department not found"}, 404

# ---- Appointments database logic ----
def insertAppointment(appointmentDetails: dict) -> dict:
    '''
    Inserts an appointment into the database.
    @param appointmentDetails: dictionary with keys: 'doctor_id', 'patient_id', 'appointment_date', 'appointment_time', 'appointment_status'
    '''
    newAppointment = Appointment(
        doctor_id=appointmentDetails['doctor_id'],
        patient_id=appointmentDetails['patient_id'],
        appointment_date=appointmentDetails['appointment_date'],
        appointment_time=appointmentDetails['appointment_time'],
        appointment_status=appointmentDetails['appointment_status']
    )
    db.session.add(newAppointment)
    db.session.commit()
    return newAppointment

def fetchAppointmentsByDoctorIdAndStatus(appointmentDetails: dict):
    '''
    Fetches appointments for a specific doctor by their ID and appointment status.
    @param appointmentDetails: dictionary with 'doctorId' and 'status' keys
    '''
    doctor_id = appointmentDetails.get('doctorId')
    status = appointmentDetails.get('status')

    if not doctor_id or not status:
        return {"error": "Both doctorId and status are required"}, 400

    appointments = Appointment.query.filter_by(doctor_id=doctor_id, appointment_status=status).all()
    response = [{'appointment_date': appointment.appointment_date, 'appointment_time': appointment.appointment_time, 'patient_id': appointment.patient_id} for appointment in appointments]
    return response

# ---- Roles database logic ----
def insertRole(roleDetails: dict) -> dict:
    '''
    Inserts a role into the database.
    @param roleDetails: dictionary with 'roleName' key
    '''
    newRole = Roles(roleName=roleDetails['roleName'])
    db.session.add(newRole)
    db.session.commit()
    return newRole

def fetchRoleById(roleDetails:dict):
    '''
        this function is responsible for fetching roles by id from the database 
        @param: 'roleId' is the expected key in the dictionary
    '''
    role = Roles.query.filter_by(id=roleDetails['roleId']).first()
    if role:
        response = {'status':True,'log':role.roleName}
        return response
    return {'status':False,"log":"role has not been"}, 404
# ---- Specialisation database logic ----
def insertSpecialisation(specialisationDetails: dict) -> dict:
    '''
    Inserts a specialisation into the database.
    @param specialisationDetails: dictionary with 'name' key
    '''
    newSpecialisation = Specialisation(name=specialisationDetails['name'])
    db.session.add(newSpecialisation)
    db.session.commit()
    return newSpecialisation

def fetchAllSpecialisations():
    '''
    Fetches all specialisations from the database.
    '''
    specialisations = Specialisation.query.all()
    response = [{'specialisationName': spec.name} for spec in specialisations]
    return response

def fetchSpecialisationById(specialisationDetails: dict):
    '''
    Fetches a specialisation by its ID.
    @param specialisationDetails: dictionary with 'specialisationId' key
    '''
    specialisation = Specialisation.query.filter_by(id=specialisationDetails['specialisationId']).first()
    if specialisation:
        response = {'specialisationName': specialisation.name}
        return response
    return {"error": "Specialisation not found"}, 404



# ---- Doctor Availability database logic ----
def insertDoctorAvailability(availabilityDetails: dict) -> dict:
    '''
    Inserts doctor availability into the database.
    @param availabilityDetails: dictionary with keys: 'doctorId', 'available_date', 'start_time', 'end_time'
    '''
    newAvailability = DoctorAvailability(
        doctor_id=availabilityDetails['doctorId'],
        available_date=availabilityDetails['available_date'],
        start_time=availabilityDetails['start_time'],
        end_time=availabilityDetails['end_time']
    )
    db.session.add(newAvailability)
    db.session.commit()
    return newAvailability

def fetchDoctorAvailabilityByDoctorId(availabilityDetails: dict):
    '''
    Fetches availability for a doctor by their ID.
    @param availabilityDetails: dictionary with 'doctorId' key
    '''
    doctor_id = availabilityDetails['doctorId']
    availability = DoctorAvailability.query.filter_by(doctor_id=doctor_id).all()
    response = [{'available_date': avail.available_date, 'start_time': avail.start_time, 'end_time': avail.end_time} for avail in availability]
    return response

def fetchDoctorAvailabilityByDate(availabilityDetails: dict):
    '''
    Fetches availability for a doctor on a specific date.
    @param availabilityDetails: dictionary with 'doctorId' and 'date' keys
    '''
    doctor_id = availabilityDetails['doctorId']
    date = availabilityDetails['date']
    availability = DoctorAvailability.query.filter_by(doctor_id=doctor_id, available_date=date).all()
    response = [{'start_time': avail.start_time, 'end_time': avail.end_time} for avail in availability]
    return response

# ---- Appointment Confirmation database logic ----
def confirmAppointment(appointmentDetails: dict) -> dict:
    '''
    Confirms an appointment in the database.
    @param appointmentDetails: dictionary with 'appointmentId' and 'confirmationStatus' keys
    '''
    appointment = Appointment.query.filter_by(id=appointmentDetails['appointmentId']).first()
    if not appointment:
        return {"error": "Appointment not found"}, 404
    
    appointment.confirmation_status = appointmentDetails['confirmationStatus']
    db.session.commit()
    return appointment

def fetchConfirmedAppointmentsByDoctorId(appointmentDetails: dict):
    '''
    Fetches confirmed appointments for a specific doctor by their ID.
    @param appointmentDetails: dictionary with 'doctorId' key
    '''
    doctor_id = appointmentDetails['doctorId']
    confirmed_appointments = Appointment.query.filter_by(doctor_id=doctor_id, confirmation_status='confirmed').all()
    response = [{'appointment_date': appt.appointment_date, 'patient_id': appt.patient_id, 'appointment_time': appt.appointment_time} for appt in confirmed_appointments]
    return response

def fetchConfirmedAppointmentsByPatientId(appointmentDetails: dict):
    '''
    Fetches confirmed appointments for a specific patient by their ID.
    @param appointmentDetails: dictionary with 'patientId' key
    '''
    patient_id = appointmentDetails['patientId']
    confirmed_appointments = Appointment.query.filter_by(patient_id=patient_id, confirmation_status='confirmed').all()
    response = [{'appointment_date': appt.appointment_date, 'doctor_id': appt.doctor_id, 'appointment_time': appt.appointment_time} for appt in confirmed_appointments]
    return response


if __name__ == "__main__":
    role = fetchRoleById({'roleId':1})
    print(role)