'''
    this module is responsible for 
'''

from marshmallow import Schema, fields, ValidationError, validates
from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import traceback
from datetime import datetime
from flask_migrate import Migrate
from models import db, User, Doctor, Patient, Appointment,Specialisation,AppointmentConfirmation,Roles,DoctorAvailability
from flask_cors import CORS
from auth_utils import generate_token, decode_token
from functools import wraps

# import kisa_utils as kutils


# Initialize Flask application
app = Flask(__name__)
CORS(app)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinicAppointment.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "xzhf bphb kwuz ybzj"

# Initialize the database and migration tool
db.init_app(app)
migrate = Migrate(app, db)

def token_required(roles):
    from db import fetchRoleById
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')

            if not token:
                return jsonify({'status': False, 'log': 'Token is missing'}), 403

            # Extract the token from the 'Bearer' format
            try:
                token = token.split()[1]
                print('>>>>>>>>>>>>>>>>token >>>',token)
            except IndexError:
                return jsonify({'status': False, 'log': 'Token format is invalid'}), 403

            try:
                data = decode_token(token, app.config['SECRET_KEY'])
                if not data:
                    return jsonify({'status': False, 'log': 'Token is invalid or expired'}), 403

                roleFetchResult = fetchRoleById({'roleId':data['role_id']})
                
                if roleFetchResult['status']:
                    if roleFetchResult['log'] not in roles:
                        return jsonify({'status': False, 'log': 'Permission denied'}), 403
                else:
                    return jsonify({'status': False, 'log': 'Permission denied'}), 403


                # if data['role_id'] not in roles:
                #     print('>>>>>>>>>>>>>>>>>>>>>>>>>roleId',data['role_id'])
                #     return jsonify({'status': False, 'log': 'Permission denied'}), 403

                # Attach user data to the request
                request.user = data
            except Exception as e:
                return jsonify({'status': False, 'log': 'Token is invalid'}), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator

def role_required(allowed_roles:list):
    from db import fetchRoleById
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')

            if not token:
                return jsonify({'status': False, 'log': 'Token is missing'}), 403

            try:
                # Extract the token from the 'Bearer' format
                token = token.split()[1]
            except IndexError:
                return jsonify({'status': False, 'log': 'Token format is invalid'}), 403

            try:
                # Decode the token to get user data
                data = decode_token(token, app.config['SECRET_KEY'])
                # print("newdecorator>>>>>>>>>>>>>>>>>>>>",data)
                if not data:
                    return jsonify({'status': False, 'log': 'Token is invalid or expired'}), 403

                roleFetchResult = fetchRoleById({'roleId':data['role_id']})
                
                if roleFetchResult['status']:
                    if roleFetchResult['log'] not in allowed_roles:
                        return jsonify({'status': False, 'log': 'Permission denied'}), 403
                else:
                    return jsonify({'status': False, 'log': 'Permission denied'}), 403
            except:
                return jsonify({'status': False, 'log': 'Invalid token'}), 403

            # Check if the user's role is in the allowed roles
            # if user_role not in allowed_roles:
            #     return jsonify({'status': False, 'log': 'Permission denied'}), 403

            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

class userPhoneNumber(Schema):
    phone = fields.Str(required=True)

class UserSchema(Schema):
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    phone = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Email(required=True)
    roleId = fields.Str(required=True)
    
class DoctorSchema(Schema):
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    phone = fields.Str(required=True)
    # password = fields.Str(required=True)
    email = fields.Email(required=True)
    specializationId = fields.Int(required=True)
    
class PatientSchema(Schema):
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    phone = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class AppointmentSchema(Schema):
    doctor_id = fields.Int(required=True)
    patient_id = fields.Int(required=True)
    appointment_date = fields.Date(required=True)
    appointment_time = fields.Time(required=True)
    appointment_status = fields.Str(required=True)
    description = fields.Str(required=True)
    # date = fields.Date(required=True)
    
class logInSchema(Schema):
    phone = fields.Str(required=True)
    password = fields.Str(required=True)

class RoleSchema(Schema):
    roleName = fields.Str(required=True)

class SpecialisationSchema(Schema):
    specializationName = fields.Str(required=True)

class DoctorAvailabilitySchema(Schema):
    doctor_id = fields.Int(required=True)
    availability_date = fields.Date(required=True)
    


class AppointmentConfirmationSchema(Schema):
    appointmentId = fields.Int(required=True, error_messages={"required": "Appointment ID is required."})
    confirmationStatus = fields.Str(required=True, error_messages={"required": "Confirmation status is required."})

    @validates('confirmationStatus')
    def validate_appointment_status(self, value):
        allowed_statuses = ["confirmed"] or ["cancelled"]
        if value not in allowed_statuses:
            raise ValidationError(f"Invalid confirmation status. Allowed values: {allowed_statuses}.")


# Utility function for validation
def validate_request(schema, data):
    try:
        schema().load(data)
    except ValidationError as err:
        return err.messages, 400
    return None

@app.route('/logIn',methods=['POST'])
def logIn():
    userDetails = request.json
    errors = validate_request(logInSchema, userDetails)
    if errors:
        return errors
    from db import login
    user = login(userDetails)
    if user['status']:
        user_id = user['log']['userId']
        role_id = user['log']['roleId']
        user_name = user['log']['firstName']
        token = generate_token(user_id, role_id, user_name, app.config['SECRET_KEY'])
        return jsonify({'status':True,'token':token})
        
    return user

@app.route('/patientLogin',methods=['POST'])
def patientLogIn():
    userDetails = request.json
    errors = validate_request(logInSchema, userDetails)
    if errors:
        return {'status':False,'log':errors}
    from db import patientLogin
    user = patientLogin(userDetails)
    if user['status']:
        user_id = user['log']['userId']
        role_id = user['log']['roleId']
        user_name = user['log']['firstName']
        token = generate_token(user_id, role_id, user_name, app.config['SECRET_KEY'])
        return jsonify({'status':True,'token':token})
        
    return user

@app.route('/userprofile',methods=['POST'])
@token_required(['user','admin','patient'])
def userProfile():
    userName = request.user['user_name']
    roleId = request.user['role_id']
    anonymous = request.user['user_id']
    from db import fetchRoleById
    role = fetchRoleById({'roleId':roleId})
    print('>>>>>>>',userName,role['log'],anonymous)
    return jsonify({'status':True, "userName":userName,"role":role['log'],'userId':anonymous})


@app.route('/test',methods=['POST'])
def test():
    from db import checkAppointmentWithin35Minutes
    role = checkAppointmentWithin35Minutes("1",'2024-07-02 00:00:00.000000',"16:22:00")
    print('>>>>>>>>>>>>>>>>>>>>>',role)
    return jsonify(role)

@app.route('/createUser', methods=['POST'])
@role_required(['admin'])
def createUser():
    userDetails = request.json
    errors = validate_request(UserSchema, userDetails)
    if errors:
        return {'status':False,'log':errors
        }
    from db import insertUser  # Lazy import
    newUser = insertUser(userDetails)
    # print('>>>>>>>>>>>>>>>>',newUser)
    return jsonify(
        {"status":True,
         "log":f"user {newUser.firstName},{newUser.lastName} has been created "}), 201



@app.route('/fetchAllUsers', methods=['POST'])
def fetchAllUsers():
    from db import fetchAllUsers  # Lazy import
    users = fetchAllUsers()
    return jsonify(users), 200

@app.route('/fetchUserByPhoneNumber', methods=['POST'])
def fetchUserByPhoneNumber():
    userDetails = request.json
    errors = validate_request(UserSchema, userDetails)
    if errors:
        return errors
    
    from db import fetchUserByPhoneNumber  # Lazy import
    user = fetchUserByPhoneNumber(userDetails)
    return jsonify(user), 200

@app.route('/fetchUserById', methods=['POST'])
def fetchUserById():
    userDetails = request.json
    # Assuming userDetails contains user_id key
    errors = validate_request(Schema.from_dict({'user_id': fields.Int(required=True)}), userDetails)
    if errors:
        return errors
    
    from db import fetchUserById  # Lazy import
    user = fetchUserById(userDetails)
    return jsonify(user), 200

# ---- Doctors endpoints ----
@app.route('/createDoctor', methods=['POST'])
# @role_required(['admin'])
def createDoctor():
    doctorDetails = request.json
    errors = validate_request(DoctorSchema, doctorDetails)
    if errors:
        return {
            'status':False,
            'log':errors
        }
    
    from db import insertDoctor  # Lazy import
    newDoctor = insertDoctor(doctorDetails)
    return jsonify({
        'status':True,
        'log':f"{newDoctor.firstName} has been created"}), 201

@app.route('/fetchAllDoctors', methods=['POST'])
def fetchAllDoctors():
    from db import fetchAllDoctors  # Lazy import
    doctors = fetchAllDoctors()
    if not len(doctors):
        return {'status':False,'log':'no doctors registered as yet'}
    print('>>>>>>>>>>',doctors)
     
    return jsonify(doctors), 200

@app.route('/fetchDoctorByPhoneNumber', methods=['POST'])
def fetchDoctorByPhoneNumber():
    doctorDetails = request.json
    errors = validate_request(DoctorSchema, doctorDetails)
    if errors:
        return errors
    
    from db import fetchDoctorByPhoneNumber  # Lazy import
    doctor = fetchDoctorByPhoneNumber(doctorDetails)
    return jsonify(doctor), 200

@app.route('/fetchDoctorById', methods=['POST'])
def fetchDoctorById():
    doctorDetails = request.json
    errors = validate_request(Schema.from_dict({'doctorId': fields.Int(required=True)}), doctorDetails)
    if errors:
        return {'status':False,'log':errors}
    
    from db import fetchDoctorById  # Lazy import
    print('>>>>>>>>>>>>>>>>>>>>>>>',doctorDetails)
    doctor = fetchDoctorById(doctorDetails)
    return {'status':True,'log':'','data':{'firstName':doctor['firstName'],'lastName':doctor['lastName']}}, 200

# ---- Patients endpoints ----
@app.route('/createPatient', methods=['POST'])
def createPatient():
    patientDetails = request.json
    errors = validate_request(PatientSchema, patientDetails)
    if errors:
        return {'status':False,'log':errors}
    
    from db import insertPatient  # Lazy import
    newPatient = insertPatient(patientDetails)
    return jsonify({'status':True,'log':f"{newPatient.firstName},has been registered successfully"}), 201

@app.route('/fetchAllPatients', methods=['POST'])
def fetchAllPatients():
    from db import fetchAllPatients  # Lazy import
    patients = fetchAllPatients()
    return jsonify(patients), 200

# ---- Appointments endpoints ----
@app.route('/createAppointment', methods=['POST'])
def createAppointment():
    appointmentDetails = request.json
    print('payload>>>>>>',appointmentDetails)
    errors = validate_request(AppointmentSchema, appointmentDetails)
    if errors:
        print('errors',errors)
        return {'status':False,
                'log':errors}
    
    from db import insertAppointment  # Lazy import
    newAppointment = insertAppointment(appointmentDetails)
    if not newAppointment['status']:
        print('false',newAppointment)
        return newAppointment
    # print('true',newAppointment)
    return jsonify({
        'status':newAppointment['status'],'log':newAppointment['log']}), 201


@app.route('/fetchAppointmentsByDoctorIdAndStatus', methods=['POST'])
def fetchAppointmentsByDoctorIdAndStatus():
    appointmentDetails = request.json
    errors = validate_request(Schema.from_dict({
        'doctor_id': fields.Int(required=True),
        'status': fields.Str(required=True)
    }), appointmentDetails)
    if errors:
        return errors
    
    from db import fetchAppointmentsByDoctorIdAndStatus  # Lazy import
    appointments = fetchAppointmentsByDoctorIdAndStatus(appointmentDetails)
    return jsonify(appointments), 200

@app.route('/fetchAppointmentsByPatientId', methods=['POST'])
def fetchAppointmentsByPatientId():
    appointmentDetails = request.json
    errors = validate_request(Schema.from_dict({'patientId': fields.Int(required=True)}), appointmentDetails)
    if errors:
        return {'status':False, 'log':errors}
    
    from db import fetchConfirmedAppointmentsByPatientId
    appointments = fetchConfirmedAppointmentsByPatientId(appointmentDetails)
    return jsonify({'status':True,'log':'','data':appointments}), 200

@app.route('/fetchCancelledAppointmentsByPatientId', methods=['POST'])
def fetchCancelledAppointmentsByPatientId():
    appointmentDetails = request.json
    errors = validate_request(Schema.from_dict({'patientId': fields.Int(required=True)}), appointmentDetails)
    if errors:
        return {'status':False, 'log':errors}
    
    from db import fetchCancelledAppointmentsByPatientId
    appointments = fetchCancelledAppointmentsByPatientId(appointmentDetails)
    return jsonify({'status':True,'log':'','data':appointments}), 200

@app.route('/confirmAppointment', methods=['POST'])
def confirm_appointment_endpoint():
    from db import confirmAppointment
    schema = AppointmentConfirmationSchema()
    try:
        # Validate input JSON against the schema
        appointment_details = schema.load(request.json)
    except ValidationError as err:
        # Return validation errors in a clean format
        return jsonify({"errors": err.messages}), 400

    # Call the confirmAppointment function
    result, status_code = confirmAppointment(appointment_details)
    print(result)
    return jsonify(result), status_code

@app.route('/cancelAppointment', methods=['POST'])
def cancelAppointment():
    from db import cancelAppointment
    schema = AppointmentConfirmationSchema()
    try:
        # Validate input JSON against the schema
        appointment_details = schema.load(request.json)
    except ValidationError as err:
        # Return validation errors in a clean format
        print('>>>>>>>>>>>>>>>>>>>>>>>',err.messages)
        return jsonify({"errors": err.messages}), 400

    # Call the confirmAppointment function
    result, status_code = cancelAppointment(appointment_details)
    print(result)
    return jsonify(result), status_code



# ---- Roles endpoints ----
@app.route('/createRole', methods=['POST'])
def createRole():
    roleDetails = request.json
    errors = validate_request(RoleSchema, roleDetails)
    if errors:
        return errors
    
    from db import insertRole  # Lazy import
    newRole = insertRole(roleDetails)
    return jsonify({
        'status':True,
        'data':f'{newRole.id}'}), 201

# ---- Specialisation endpoints ----
@app.route('/createSpecialisation', methods=['POST'])
@role_required(['admin'])
def createSpecialisation():
    specialisationDetails = request.json
    errors = validate_request(SpecialisationSchema, specialisationDetails)
    if errors:
        return {
            'status':False,
            'log':errors
        }
    
    from db import insertSpecialisation  # Lazy import
    newSpecialisation = insertSpecialisation(specialisationDetails)
    print('>>>>>>>>>>>>>>>>>',newSpecialisation.specializationName)
    return jsonify({
        'status':True,
        'log':f"specialisation {newSpecialisation.specializationName} has been created"}), 201

@app.route('/fetchAllSpecialisations', methods=['POST'])
def fetchAllSpecialisations():
    from db import fetchAllSpecialisations  # Lazy import
    specialisations = fetchAllSpecialisations()
    return jsonify(specialisations), 200

@app.route('/fetchSpecialisationById', methods=['POST'])
def fetchSpecialisationById():
    specialisationDetails = request.json
    errors = validate_request(Schema.from_dict({'specialisation_id': fields.Int(required=True)}), specialisationDetails)
    if errors:
        return errors
    
    from db import fetchSpecialisationById  # Lazy import
    specialisation = fetchSpecialisationById(specialisationDetails)
    return jsonify(specialisation), 200

# ---- Doctor Availability endpoints ----
@app.route('/createDoctorAvailability', methods=['POST'])
def createDoctorAvailability():
    availabilityDetails = request.json
    errors = validate_request(DoctorAvailabilitySchema, availabilityDetails)
    if errors:
        return errors
    
    from db import insertDoctorAvailability  # Lazy import
    newAvailability = insertDoctorAvailability(availabilityDetails)
    return jsonify(newAvailability), 201

@app.route('/fetchDoctorByDoctorId', methods=['POST'])
def fetchDoctorByDoctorId():
    availabilityDetails = request.json
    errors = validate_request(Schema.from_dict({'doctorId': fields.Int(required=True)}), availabilityDetails)
    if errors:
        return {'status':False,'log':errors}
    
    from db import fetchDoctorById  # Lazy import
    response = fetchDoctorById(availabilityDetails)
    return jsonify({'status':True,'log':'','data':response}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, host='0.0.0.0', port = 5000)
