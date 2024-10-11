from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, User, Doctor, Patient, Department, Appointment
from flask_cors import CORS
import kisa_utils as kutils


# Initialize Flask application
app = Flask(__name__)
CORS(app)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinicAppointment.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and migration tool
db.init_app(app)
migrate = Migrate(app, db)

# Define routes (example route for testing)
@app.route('/')
def home():
    return "Welcome to the Clinic Appointment System!"

@app.route('/addUser', methods=['POST'])
def add_user():
    from db import insertUser
    user_data = request.json  # Get the user data from the request body

    if not user_data or not all(key in user_data for key in ['userName', 'password', 'email', 'phoneNumber', 'roleId']):
        return jsonify({"error": "Missing required fields"}), 400  # Return an error if any field is missing

    try:
        new_user = insertUser(user_data)  # Call the insertUser function
        return jsonify({
            "status": "success",
            "user": {
                "username": new_user.username,
                "email": new_user.email
            }
        }), 201  # Return a success response with the created user's info
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle any unexpected errors
    
@app.route('/fetchAllUsers',methods=['POST'])
def fetchAllUsers():
    from db import fetchAllUsers
    response = fetchAllUsers()
    return response

@app.route('/fetchUserByPhoneNumber', methods=['POST'])
def fetchUserByPhoneNUmber():
    from db import fetchUserByPhoneNumber
    payload = request.get_json()
    payloadStructure = {
        "phoneNumber":str
    }
    payloadValidationRespose = kutils.structures.validator.validate(payload,payloadStructure)
    if payloadValidationRespose['status']:
        for key in payload:
            if not payload[key]:
                return{'status':False, 'log':f'the value for {key} is missing please provide it '}
        response = fetchUserByPhoneNumber(payload)
        return jsonify(response)
 
# --the endpoints below are responsible handling doctor routes 
@app.route('/addDoctor', methods=['POST'])
def add_doctor():
    from db import insertDoctor
    doctor_data = request.json  # Get the doctor data from the request body

    if not doctor_data or not all(key in doctor_data for key in ['name', 'email', 'phone', 'specialization', 'password', 'department_id']):
        return jsonify({"error": "Missing required fields"}), 400  # Return an error if any field is missing

    try:
        new_doctor = insertDoctor(doctor_data)  # Call the insertDoctor function
        return jsonify({
            "status": "success",
            "doctor": {
                "name": new_doctor.name,
                "email": new_doctor.email
            }
        }), 201  # Return a success response with the created doctor's info
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle any unexpected errors

@app.route('/fetchAllDoctors',methods=['POST'])
def fetchAllDoctors():
    from db import fetchAllDoctors
    response = fetchAllDoctors()
    return response
    
@app.route('/fetchDoctorById', methods=['POST'])
def fetchDoctorByIdRoute():
    from db import fetchDoctorById
    doctorDetails = request.get_json()  # Get the doctor details from the request body
    if 'doctorId' not in doctorDetails or not doctorDetails['doctorId']:
        return jsonify({"error": "doctorId is required"}), 400  # Check if doctorId is provided

    try:
        response = fetchDoctorById(doctorDetails)  # Call the fetchDoctorById function
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle any errors
    
@app.route('/fetchDoctorsBySpecialization', methods=['POST'])
def fetchDoctorsBySpecializationRoute():
    from db import fetchDoctorsBySpecialization
    doctorDetails = request.get_json()  # Get the doctor details from the request body
    if 'specialization' not in doctorDetails or not doctorDetails['specialization']:
        return jsonify({"error": "specialization is required"}), 400  # Check if specialization is provided

    try:
        doctors = fetchDoctorsBySpecialization(doctorDetails)  # Call the fetchDoctorsBySpecialization function
        response = doctors
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle any errors
    
@app.route('/fetchDoctorByDepartment', methods=['POST'])
def fetchDoctorByDepartmentRoute():
    from db import fetchDoctorByDepartment
    doctorDetails = request.get_json()  # Get the doctor details from the request body
    if 'departmentId' not in doctorDetails or not doctorDetails['departmentId']:
        return jsonify({"error": "departmentId is required"}), 400  # Check if departmentId is provided

    try:
        response = fetchDoctorByDepartment(doctorDetails)  # Call the fetchDoctorByDepartment function
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle any errors
        
        
# ---the routes below are responsible for handling patient routes    
@app.route('/addPatient', methods=['POST'])
def add_patient():
    from db import insertPatient
    patient_data = request.json
    if not patient_data or not all(key in patient_data for key in ['name', 'email', 'phone', 'password']):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        new_patient = insertPatient(patient_data)
        return jsonify({"status": "success", "patient": {"name": new_patient.name, "email": new_patient.email}}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/fetchAllPatients', methods=['POST'])
def fetchAllPatientsRoute():
    from db import fetchAllPatients
    try:
        response = fetchAllPatients()  # Call the fetchAllPatients function
        return jsonify(response), 200  # Return success response
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle any errors

@app.route('/fetchPatientsById', methods=['POST'])
def fetchPatientsByIdRoute():
    from db import fetchPatientsById
    patientDetails = request.get_json()  # Get the patient details from the request body
    
    if 'patientId' not in patientDetails or not patientDetails['patientId']:
        return jsonify({"error": "patientId is required"}), 400  # Check if patientId is provided

    try:
        response = fetchPatientsById(patientDetails)  # Call the fetchPatientsById function
        return jsonify(response), 200  # Return success response
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle any errors

# -----the end[points below are responsible for handling department routes 
@app.route('/addDepartment', methods=['POST'])
def add_department():
    from db import insertDepartment
    department_data = request.json
    if not department_data or 'name' not in department_data:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        new_department = insertDepartment(department_data)
        return jsonify({"status": "success", "department": {"name": new_department.name}}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/fetchAllDepartments', methods=['POST'])
def fetchAllDepartmentsRoute():
    from db import fetchAllDepartments
    try:
        response = fetchAllDepartments()  # Call the fetchAllDepartments function
        return jsonify(response), 200  # Return success response
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle any errors

@app.route('/departmentById', methods=['POST'])
def departmentByIdRoute():
    from db import departmentById
    departmentDetails = request.get_json()  # Get department details from the request body
    
    if 'departmentId' not in departmentDetails or not departmentDetails['departmentId']:
        return jsonify({"error": "departmentId is required"}), 400  # Check if departmentId is provided

    try:
        response = departmentById(departmentDetails)  # Call the departmentById function
        return jsonify(response), 200  # Return success response
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle any errors

# --the endpoints below are responsible for handing appointment routes ----- 
@app.route('/addAppointment', methods=['POST'])
def add_appointment():
    from db import insertAppointment
    appointment_data = request.json
    if not appointment_data or not all(key in appointment_data for key in ['doctor_id', 'patient_id', 'appointment_date', 'appointment_time', 'appointment_status']):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        new_appointment = insertAppointment(appointment_data)
        return jsonify({"status": "success", "appointment": {"doctor_id": new_appointment.doctor_id,
                                                             "patient_id": new_appointment.patient_id}}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/fetchSpecificAppointments', methods=['POST'])
def fetchSpecificAppointmentsRoute():
    from db import fetchAllSpecificAppointments
    appointment_details = request.get_json()  # Get the doctor and patient IDs from the request body
    
    if 'doctorId' not in appointment_details or 'patientId' not in appointment_details:
        return jsonify({"error": "Both doctorId and patientId are required"}), 400  # Ensure both IDs are provided

    try:
        response = fetchAllSpecificAppointments(appointment_details)  # Call the function
        return jsonify(response), 200  # Return the fetched appointments
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle unexpected errors
    
@app.route('/fetchAppointmentsByPatientId', methods=['POST'])
def fetchAppointmentsByPatientIdRoute():
    from db import fetchAppointmentsByPatientId
    appointment_details = request.get_json()  # Get the patientId from the request body

    if 'patientId' not in appointment_details:
        return jsonify({"error": "patientId is required"}), 400  # Ensure patientId is provided

    try:
        response = fetchAppointmentsByPatientId(appointment_details)  # Call the function
        return jsonify(response), 200  # Return the fetched appointments
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle unexpected errors

@app.route('/fetchAppointmentsByPatientIdAndStatus', methods=['POST'])
def fetchAppointmentsByPatientIdAndStatusRoute():
    from db import fetchAppointmentsByPatientIdAndStatus
    appointment_details = request.get_json()  # Get the patientId and status from the request body

    if 'patientId' not in appointment_details or 'status' not in appointment_details:
        return jsonify({"error": "Both patientId and status are required"}), 400  # Ensure patientId and status are provided

    try:
        response = fetchAppointmentsByPatientIdAndStatus(appointment_details)  # Call the function
        return jsonify(response), 200  # Return the fetched appointments
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle unexpected errors
    
@app.route('/fetchAppointmentsByDoctorIdAndStatus', methods=['POST'])
def fetchAppointmentsByDoctorIdAndStatusRoute():
    from db import fetchAppointmentsByDoctorIdAndStatus
    appointment_details = request.get_json()  # Get the doctorId and status from the request body

    if 'doctorId' not in appointment_details or 'status' not in appointment_details:
        return jsonify({"error": "Both doctorId and status are required"}), 400  # Ensure doctorId and status are provided

    try:
        response = fetchAppointmentsByDoctorIdAndStatus(appointment_details)  # Call the function
        return jsonify(response), 200  # Return the fetched appointments
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle unexpected errors




@app.route('/addRole', methods=['POST'])
def add_role():
    from db import insertRole
    role_data = request.json
    if not role_data or 'roleName' not in role_data:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        new_role = insertRole(role_data)
        return jsonify({"status": "success", "role": {"roleName": new_role.roleName}}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# Register Blueprints if you have them (uncomment and add your blueprints as needed)
# from routes.users import users_bp
# from routes.appointments import appointments_bp
# from routes.doctors import doctors_bp
# app.register_blueprint(users_bp, url_prefix='/users')
# app.register_blueprint(appointments_bp, url_prefix='/appointments')
# app.register_blueprint(doctors_bp, url_prefix='/doctors')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
