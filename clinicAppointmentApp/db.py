'''
    this module is meant to handle all the database logic and all the logic of 
    the application for example all the logic for inserting,updating,altering,
    deleting to the database 
'''
from datetime import datetime,timedelta
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

# from werkzeug.security import check_password_hash

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
    response = [{'doctorId':doctor.id,'firstName': doctor.firstName, 'lastName': doctor.lastName, "email": doctor.email, "phone": doctor.phone, "specialization": doctor.specializationId} for doctor in doctors]
    # response = []
    # for doctor in doctors:
    #     response.append({
    #         'firstName': doctor.firstName,
    #         'lastName': doctor.lastName,
    #         'email': doctor.email,
    #         'phone': doctor.phone,
    #         'specialization': doctor.specializationId,
    #         'doctorId':doctor.id
    #     })
    return response

def fetchDoctorFromAppointments(doctorId:str,appointmentDate:str,appointmentTime:str):
    # appointmentDatez=datetime.strptime(appointmentDate, '%Y-%m-%d').date()
    print(doctorId,appointmentDate,appointmentTime)
    doctor = Appointment.query.filter_by(doctor_id=doctorId, appointment_date = appointmentDate, appointment_time = appointmentTime).all()
    print('>>>>',doctor)
    
    #  apptTime = checkAppointmentWithin35Minutes(doctorId,appointmentDate,appointmentTime)
    #     if apptTime['status']:
    #         return apptTime
    #     return apptTime
    if not doctor:
        return {'status':True, 'log':'no  schedule'}
       
    return {'status':False,'log':'there an appointment scheduled in the timeframe'}
    

def checkAppointmentWithin35Minutes(doctorId: str, patientId: str, appointmentDate: str, appointmentTime: str) -> dict:
    """
    Checks if there is already an appointment within 35 minutes of the provided appointment time
    for either the doctor or the patient.

    :param doctorId: ID of the doctor
    :param patientId: ID of the patient
    :param appointmentDate: Date of the appointment in string format (YYYY-MM-DD)
    :param appointmentTime: Time of the appointment in string format (HH:MM:SS)
    :return: Dictionary with status and log
    """
    # Convert appointmentDate and appointmentTime to a datetime object
    new_appointment_datetime = datetime.strptime(f"{appointmentDate} {appointmentTime}", "%Y-%m-%d %H:%M:%S")

    # Fetch all appointments for the doctor and patient on the given date
    doctor_appointments = Appointment.query.filter_by(
        doctor_id=doctorId, appointment_date=appointmentDate
    ).all()

    patient_appointments = Appointment.query.filter_by(
        patient_id=patientId, appointment_date=appointmentDate
    ).all()

    # Check conflicts for the doctor
    for appointment in doctor_appointments:
        existing_datetime = datetime.strptime(
            f"{appointment.appointment_date} {appointment.appointment_time}",
            "%Y-%m-%d %H:%M:%S"
        )
        # Check if the time difference is within 35 minutes
        if abs((new_appointment_datetime - existing_datetime).total_seconds()) <= 35 * 60:
            return {'status': True, 'log': 'Doctor has a conflicting appointment within 35 minutes'}

    # Check conflicts for the patient
    for appointment in patient_appointments:
        existing_datetime = datetime.strptime(
            f"{appointment.appointment_date} {appointment.appointment_time}",
            "%Y-%m-%d %H:%M:%S"
        )
        # Check if the time difference is within 35 minutes
        if abs((new_appointment_datetime - existing_datetime).total_seconds()) <= 35 * 60:
            return {'status': True, 'log': 'Patient has a conflicting appointment within 35 minutes'}

    # If no conflicts are found
    return {'status': False, 'log': 'No conflicting appointments'}





def fetchDoctorFromAppointment(doctorId:str,appointmentDate:str):
    # appointmentDatez=datetime.strptime(appointmentDate, '%Y-%m-%d').date()
    # print(appointmentDatez)
    doctor = Appointment.query.filter_by(doctor_id=doctorId, appointment_date = appointmentDate).all()
    if not doctor:
        return {'status':False, 'log':'no  schedule'}
    return doctor

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
    response =[{'patientId':patient.id,'firstName': patient.firstName, 'lastName': patient.lastName, "email": patient.email, "phone": patient.phone} for patient in patients]
    return response

def fetchPatientById(patientDetails:dict)->dict:
    '''
        this function si responsible for fetching patient by Id 
        @param:patientId is the require key in the dictionary 
    '''
    patient = Patient.query.filter_by(id=patientDetails['patientId']).first()
    if not patient:
        return({'status':False,'log':'patient registered to Id not found visit reception'})
    return({'status':True,'log':{'firstName': patient.firstName, 'lastName': patient.lastName, 
                                 "email": patient.email, "phone": patient.phone}})

# ---- Appointments database logic ----
def insertAppointment(appointmentDetails: dict) -> dict:
    '''
    Inserts an appointment into the database.
    @param appointmentDetails: dictionary with keys: 'doctor_id', 'patient_id', 'appointment_date', 'appointment_time', 'appointment_status',
    'description'
    '''
    appointment_date = datetime.strptime(appointmentDetails['appointment_date'], '%Y-%m-%d').date()
    appointment_time = datetime.strptime(appointmentDetails['appointment_time'], '%H:%M:%S').time()
    
    print('appointment date>>>>> ',appointment_date)
    doctorScheduleStatus = checkAppointmentWithin35Minutes(appointmentDetails['doctor_id'],appointmentDetails['patient_id'],appointment_date,appointment_time.strftime('%H:%M:%S'))
    print('>>>>>>>>>>',appointment_date,appointment_time.strftime('%H:%M:%S'))
    if  not doctorScheduleStatus['status']:
    
        newAppointment = Appointment(
            doctor_id=appointmentDetails['doctor_id'],
            patient_id=appointmentDetails['patient_id'],
            appointment_date=appointment_date,
            appointment_time=appointment_time.strftime('%H:%M:%S'),
            appointment_status=appointmentDetails['appointment_status'],
            description = appointmentDetails['description']
        )
        db.session.add(newAppointment)
        db.session.commit()
        return {'status':True,'log':f"appointment has been scheduled at {newAppointment.appointment_time} on {newAppointment.appointment_date}"}
    return doctorScheduleStatus

def fetchConfirmedAppointmentsByPatientId(patientDetails:dict):
    '''
    this function fetches all confirmed patient appointments by patient Id
    @param: patientDetails: dictionary with 'patientId' key
    '''
    
    patientId = patientDetails['patientId']
    appointments = Appointment.query.filter_by(patient_id=patientId , appointment_status='confirmed').all()
    response = [{'appointment_date': appointment.appointment_date, 'appointment_time': appointment.appointment_time, 'doctor_id': appointment.doctor_id} for appointment in appointments]
    return response

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
    @param specialisationDetails: dictionary with 'specializationName' key
    '''
    newSpecialisation = Specialisation(specializationName=specialisationDetails['specializationName'])
    db.session.add(newSpecialisation)
    db.session.commit()
    return newSpecialisation

def fetchAllSpecialisations():
    '''
    Fetches all specialisations from the database.
    '''
    specialisations = Specialisation.query.all()
    response = [{'specializationId':spec.id,'specializationName': spec.specializationName} for spec in specialisations]
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
# def confirmAppointment(appointmentDetails: dict) -> dict:
#     '''
#     Confirms an appointment in the database.
#     @param appointmentDetails: dictionary with 'appointmentId' and 'confirmationStatus' keys
#     '''
#     appointment = Appointment.query.filter_by(id=appointmentDetails['appointmentId']).first()
#     if not appointment:
#         return {"error": "Appointment not found"}, 404
    
#     appointment.appointment_status = appointmentDetails['confirmationStatus']
#     db.session.commit()
    # return appointment
def confirmAppointment(appointmentDetails: dict) -> dict:
    """
    Confirms an appointment in the database.
    @param appointmentDetails: dictionary with 'appointmentId' and 'confirmationStatus' keys
    """
    # Fetch the appointment from the database
    appointment = Appointment.query.filter_by(id=appointmentDetails['appointmentId']).first()
    if not appointment:
        return {"error": "Appointment not found"}, 404

    # Update the confirmation status
    appointment.appointment_status = appointmentDetails['confirmationStatus']
    db.session.commit()

    return {
        "message": "Appointment confirmed successfully",
        "appointmentId": appointment.id,
        "confirmationStatus": appointment.appointment_status
    }, 200
    
def cancelAppointment(appointmentDetails: dict) -> dict:
    """
    Confirms an appointment in the database.
    @param appointmentDetails: dictionary with 'appointmentId' and 'confirmationStatus' keys
    """
    # Fetch the appointment from the database
    appointment = Appointment.query.filter_by(id=appointmentDetails['appointmentId']).first()
    if not appointment:
        return {"error": "Appointment not found"}, 404

    # Update the confirmation status
    appointment.appointment_status = appointmentDetails['confirmationStatus']
    db.session.commit()

    return {
        "message": "Appointment cancelled successfully",
        "appointmentId": appointment.id,
        "confirmationStatus": appointment.appointment_status
    }, 200

def fetchAllPendingAppointments()->dict:
    '''
        THis function  is responsible for fetching all pending appointments 
    '''
    pendingAppointments =Appointment.query.filter_by(appointment_status='pending').all()
    if not pendingAppointments:
        return {'status':False,'log':'no pending appointments'}
    response = [{'appointment_date': appointment.appointment_date, 'appointment_time': appointment.appointment_time, 'doctor_id': appointment.doctor_id, 'patient_id': appointment.patient_id} for appointment in pendingAppointments]
    return {'status':True,'log':response}

def fetchAllConfirmedAppointments()->dict:
    '''
        THis function  is responsible for fetching all confirmed appointments 
    '''
    pendingAppointments =Appointment.query.filter_by(appointment_status='confirmed').all()
    if not pendingAppointments:
        return {'status':False,'log':'no confirmed appointments'}
    response = [{'appointment_date': appointment.appointment_date, 'appointment_time': appointment.appointment_time, 'doctor_id': appointment.doctor_id, 'patient_id': appointment.patient_id} for appointment in pendingAppointments]
    return {'status':True,'log':response}

def fetchAllCancelledAppointments()->dict:
    '''
        THis function  is responsible for fetching all cancelled appointments 
    '''
    pendingAppointments =Appointment.query.filter_by(appointment_status='cancelled').all()
    if not pendingAppointments:
        return {'status':False,'log':'no cancelled appointments'}
    response = [{'appointment_date': appointment.appointment_date, 'appointment_time': appointment.appointment_time, 'doctor_id': appointment.doctor_id, 'patient_id': appointment.patient_id} for appointment in pendingAppointments]
    return {'status':True,'log':response}

    
def fetchConfirmedAppointmentsByDoctorId(appointmentDetails: dict):
    '''
    Fetches confirmed appointments for a specific doctor by their ID.
    @param appointmentDetails: dictionary with 'doctorId' key
    '''
    doctor_id = appointmentDetails['doctorId']
    confirmed_appointments = Appointment.query.filter_by(doctor_id=doctor_id, appointment_status='confirmed').all()
    response = [{'appointment_date': appt.appointment_date, 'patient_id': appt.patient_id, 'appointment_time': appt.appointment_time} for appt in confirmed_appointments]
    return response

def fetchConfirmedAppointmentsByPatientId(appointmentDetails: dict):
    '''
    Fetches confirmed appointments for a specific patient by their ID.
    @param appointmentDetails: dictionary with 'patientId' key
    '''
    patient_id = appointmentDetails['patientId']
    confirmed_appointments = Appointment.query.filter_by(patient_id=patient_id, appointment_status='confirmed').all()
    response = [{'appointment_date': appt.appointment_date, 'doctor_id': appt.doctor_id, 'appointment_time': appt.appointment_time} for appt in confirmed_appointments]
    return response

def fetchCancelledAppointmentsByPatientId(appointmentDetails: dict):
    '''
    Fetches confirmed appointments for a specific patient by their ID.
    @param appointmentDetails: dictionary with 'patientId' key
    '''
    patient_id = appointmentDetails['patientId']
    confirmed_appointments = Appointment.query.filter_by(patient_id=patient_id, appointment_status='cancelled').all()
    response = [{'appointment_date': appt.appointment_date, 'doctor_id': appt.doctor_id, 'appointment_time': appt.appointment_time} for appt in confirmed_appointments]
    return response


if __name__ == "__main__":
    role = fetchRoleById({'roleId':1})
    print(role)