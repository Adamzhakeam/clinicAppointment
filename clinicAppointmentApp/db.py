'''
    this module is meant to handle all the database logic and all the logic of 
    the application forexample all the logic for inserting,updating,altering,
    deleting to the database 
'''
import kisa_utils as kutils 

from models import db,User,Doctor,Department,Appointment,Roles,Patient
# ----the functions below are responsible for handling users database logic
def insertUser(userDetails:dict)->dict:
    '''
        this function is responsible for inserting 
        user into the dataBase 
        @param userDetails:'username','password','email','phoneNumber','roleId' are the expected keys
    '''
    passwordHash = kutils.encryption.hash(userDetails['password'])
    newUser = User(username=userDetails['userName'],password= passwordHash,email=userDetails['email']
                   ,phone=userDetails['phoneNumber'],roleId = userDetails['roleId'])
    db.session.add(newUser)
    db.session.commit()
    return newUser

def fetchAllUsers():
    '''
        this function is responsible for fetching 
        all the users from the database 
    '''
    allUsers = User.query.all()
    
    response = [{'username':user.username,"email":user.email,"phone":user.phone,
                "roleId":user.roleId,}for user in allUsers]
    return response

def fetchUserByPhoneNumber(userDetails:dict):
    '''
        this function is responsible for fetching users by there phone Number
        @param UserDetails:'phoneNumber' is the expected key 
    '''
    user = User.query.filter_by(phone=userDetails['phoneNumber']).first()
    response = {'username':user.username,'email':user.email,'phonenumber':user.id}
    return response

def fetchUserById(userDetails:dict):
    '''
        this function is responsible for fetching user by id
        @paramUserDetails:'userId' is the expected key
    '''
    user = User.query.filter_by(id=userDetails['userId']).first()
    response = {'username':user.username,"email":user.email,"phone":user.phone,
                "roleId":user.roleId,}
    return response 

# --the modules below are responsible for handling the database logic for doctors 
def insertDoctor(doctorDetails: dict) -> dict:
    '''
    Insert a doctor into the database.
    @param: doctorDetails - dictionary with keys: 'name', 'email', 'phone', 'specialization', 'password', 'department_id'
    '''
    passwordHash = kutils.encryption.hash(doctorDetails['password'])
    newDoctor = Doctor(
        name=doctorDetails['name'],
        email=doctorDetails['email'],
        phone=doctorDetails['phone'],
        specialization=doctorDetails['specialization'],
        password=passwordHash,
        department_id=doctorDetails['department_id']
    )
    db.session.add(newDoctor)
    db.session.commit()
    return newDoctor

def fetchAllDoctors():
    '''
        this function is responsible for fetching all doctors from the database 
    '''
    doctors = Doctor.query.all()
    response = [{'username':user.name,"email":user.email,"phone":user.phone,
                "roleId":user.role,}for user in doctors]
    return response 

def fetchDoctorsByPhoneNumber(doctorDetails:dict):
    '''
        this function is responsible for fetching doctors by there phoneNumber 
        @param doctorDetails:'phoneNumber' is the expected key 
    '''
    doctor = Doctor.query.filter_by(phone=doctorDetails['phoneNumber']).first()
    response = {'username':doctor.name,"email":doctor.email,"phone":doctor.phone,
                "role":doctor.role}
    return response

def fetchDoctorById(doctorDetails:dict):
    '''
        this function is responsible for fetching doctors by Id 
        @param doctorDetails:'doctorId' is the expected key
    '''
    doctor = Doctor.query.filter_by(id=doctorDetails['doctorId']).first()
    response = {'username':doctor.name,"email":doctor.email,"phone":doctor.phone,
                "role":doctor.role}
    return response  

def fetchDoctorsBySpecialization(doctorDetails:dict):
    '''
    this function is responsible for fetching doctors with by specialization 
    @param doctorDetails: 'specialization' is the expected key
    '''
    doctors = Doctor.query.filter(Doctor.specialization == doctorDetails['specialization']).all()
    response = [{'username':user.name,"email":user.email,"phone":user.phone,
                "roleId":user.role,}for user in doctors]
    
    return response

def fetchDoctorByDepartment(doctorDetails:dict):
    '''
        this function is responsible for fetching doctors by department
        @param doctorDetails:'departmentId is the expected key 
    '''
    doctors = Doctor.query.filter(Doctor.department_id == doctorDetails['departmentId'])
    response = [{'username':user.name,"email":user.email,"phone":user.phone,
                "roleId":user.role,}for user in doctors]
     
    return response 
    
# -- the functions below are responsible for handling patient logic in the database 
def insertPatient(patientDetails: dict) -> dict:
    '''
    Insert a patient into the database.
    @param: patientDetails - dictionary with keys: 'name', 'email', 'phone', 'password'
    '''
    passwordHash = kutils.encryption.hash(patientDetails['password'])
    newPatient = Patient(
        name=patientDetails['name'],
        email=patientDetails['email'],
        phone=patientDetails['phone'],
        password=passwordHash
    )
    db.session.add(newPatient)
    db.session.commit()
    return newPatient

def fetchAllPatients():
    '''
        this function is responsible for fetching all patients from the database 
    '''
    patients = Patient.query.all()
    response = [{'username':user.name,"email":user.email,"phone":user.phone,
                "roleId":user.role,}for user in patients]
    return response

def fetchPatientsById(doctorDetails:dict):
    '''
        this function is responsible for fetching doctors by Id 
        @param doctorDetails:'patientId' is the expected key
    '''
    patient = Patient.query.filter_by(id=doctorDetails['doctorId']).first()
    response = {'username':patient.name,"email":patient.email,"phone":patient.phone}
    return response 

# --the logic below is responsible for handling  department database querries

def insertDepartment(departmentDetails: dict) -> dict:
    '''
    Insert a department into the database.
    @param: departmentDetails - dictionary with keys: 'name'
    '''
    newDepartment = Department(
        name=departmentDetails['name']
    )
    db.session.add(newDepartment)
    db.session.commit()
    return newDepartment

def fetchAllDepartments():
    '''
        this function is responsible for fetching all departments from the database 
    '''
    departments = Department.query.all()
    response = [{'departmentName':department.name,}for department in departments]
    return response

def departmentById(departmentDetails:dict):
    '''
        this function is responsible for fetching doctors by Id 
        @param departmentDetails:'departmentId' is the expected key
    '''
    department = Department.query.filter_by(id=departmentDetails['doctorId']).first()
    response = {'departmentName':department.name,'departmentId':department.id}
    return response 

# --- the modules below are responsible for handling appointment logic 
def insertAppointment(appointmentDetails: dict) -> dict:
    '''
    Insert an appointment into the database.
    @param: appointmentDetails - dictionary with keys: 'doctor_id', 'patient_id', 'appointment_date', 'appointment_time', 'appointment_status'
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

def fetchAllSpecificAppointments(appointmentDetails: dict):
    '''
        This function is responsible for fetching appointments 
        for a specific doctor and patient
        @param appointmentDetails: 'doctorId' and 'patientId' are the expected keys
    '''
    doctor_id = appointmentDetails.get('doctorId')
    patient_id = appointmentDetails.get('patientId')

    if not doctor_id or not patient_id:
        return {"error": "Both doctorId and patientId are required"}, 400

    appointments = (
        Appointment.query
        .join(Doctor, Appointment.doctor_id == Doctor.id)
        .join(Patient, Appointment.patient_id == Patient.id)
        .filter(Doctor.id == doctor_id, Patient.id == patient_id)
        .all()
    )

    response = [{'date': appointment.appointment_date, 
                 'time': appointment.appointment_time, 
                 'status': appointment.appointment_status} 
                for appointment in appointments]
    return response
def fetchAppointmentsByPatientId(appointmentDetails: dict):
    '''
        This function is responsible for fetching appointments 
        for a specific patient by their patientId
        @param appointmentDetails: 'patientId' is the expected key
    '''
    patient_id = appointmentDetails.get('patientId')

    if not patient_id:
        return {"error": "patientId is required"}, 400

    appointments = (
        Appointment.query
        .join(Patient, Appointment.patient_id == Patient.id)
        .filter(Patient.id == patient_id)
        .all()
    )

    response = [{'date': appointment.appointment_date, 
                 'time': appointment.appointment_time, 
                 'status': appointment.appointment_status, 
                 'doctorId': appointment.doctor_id} 
                for appointment in appointments]
    return response

def fetchAppointmentsByPatientIdAndStatus(appointmentDetails: dict):
    '''
        This function is responsible for fetching appointments 
        for a specific patient by their patientId and appointment status
        @param appointmentDetails: 'patientId' and 'status' are the expected keys
    '''
    patient_id = appointmentDetails.get('patientId')
    status = appointmentDetails.get('status')

    if not patient_id or not status:
        return {"error": "Both patientId and status are required"}, 400

    appointments = (
        Appointment.query
        .join(Patient, Appointment.patient_id == Patient.id)
        .filter(Patient.id == patient_id, Appointment.appointment_status == status)
        .all()
    )

    response = [{'date': appointment.appointment_date, 
                 'time': appointment.appointment_time, 
                 'status': appointment.appointment_status, 
                 'doctorId': appointment.doctor_id} 
                for appointment in appointments]
    return response

def fetchAppointmentsByDoctorIdAndStatus(appointmentDetails: dict):
    '''
        This function is responsible for fetching appointments 
        for a specific doctor by their doctorId and appointment status.
        @param appointmentDetails: 'doctorId' and 'status' are the expected keys.
    '''
    doctor_id = appointmentDetails.get('doctorId')
    status = appointmentDetails.get('status')

    if not doctor_id or not status:
        return {"error": "Both doctorId and status are required"}, 400

    appointments = (
        Appointment.query
        .join(Doctor, Appointment.doctor_id == Doctor.id)
        .filter(Doctor.id == doctor_id, Appointment.appointment_status == status)
        .all()
    )

    response = [{'date': appointment.appointment_date, 
                 'time': appointment.appointment_time, 
                 'status': appointment.appointment_status, 
                 'patientId': appointment.patient_id} 
                for appointment in appointments]
    return response


def insertRole(roleDetails: dict) -> dict:
    '''
    Insert a role into the database.
    @param: roleDetails - dictionary with keys: 'roleName'
    '''
    newRole = Roles(
        roleName=roleDetails['roleName']
    )
    db.session.add(newRole)
    db.session.commit()
    return newRole

if __name__ == "__main__":
    user = {
        'userName':"johndoe",
        'password':"1234",
        'email':'johndoe@gmail.com',
        'phoneNumber':'0768678678',
        'role':'admin'
        
    }
    print(insertUser(user))
    pass
    