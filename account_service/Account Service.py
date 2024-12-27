from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from swagger_config import init_swagger 
import requests

print("Account Service...")
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/Study/Fourth year/СОАПЗ/STO_project/databases/shared_service.db'  
app.config['JWT_HEADER_NAME'] = 'Authorization'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize Swagger
init_swagger(app)  

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)  # Store hashed password

# Client model
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

# Create tables
@app.before_first_request
def create_tables():
    db.create_all()  # Create all tables
    db.session.commit()  # Commit changes to ensure tables are created

# Register service with the service registry
def register_service():
    service_info = {
        'name': 'Account Service',
        'url': 'http://localhost:5001',
        'status': 'active'
    }
    # Register the service with the service registry
    response = requests.post('http://localhost:5000/services', json=service_info)
    existing_services = requests.get('http://localhost:5000/services').json()
    if any(service['name'] == service_info['name'] for service in existing_services):
        print('Service is already registered.')
        return

    if response.status_code == 201:
        print('Service registered successfully.')
    else:
        print('Failed to register service:', response.json())

# Endpoint to register a new user
@app.route('/accounts/register', methods=['POST'])
def register():
    data = request.get_json()
    if not all(k in data for k in ("first_name", "last_name", "email", "phone_number", "password")):
        return {'message': 'Missing required fields'}, 400

    if User.query.filter_by(email=data['email']).first():
        return {'message': 'Email already exists'}, 409

    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=generate_password_hash(data['password'])
    )
    db.session.add(new_user)
    db.session.commit()
    return {'message': 'User registered successfully'}, 201

# Endpoint to login a user
@app.route('/accounts/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}, 200
    return {'message': 'Invalid credentials'}, 401

# Endpoint to reset user password
@app.route('/accounts/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return {'message': 'User not found'}, 404

    # Here you would typically send an email with a reset link
    return {'message': 'Password reset link sent'}, 200

# Endpoint to get user profile
@app.route('/accounts/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_profile(user_id):
    user = User.query.get_or_404(user_id)
    return {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone_number': user.phone_number
    }, 200

# Endpoint to update user profile
@app.route('/accounts/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user_profile(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.email = data.get('email', user.email)
    user.phone_number = data.get('phone_number', user.phone_number)
    db.session.commit()
    return {'message': 'Profile updated successfully'}, 200

# Endpoint to create a new client
@app.route('/clients', methods=['POST'])
def create_client():
    data = request.get_json()
    if not all(k in data for k in ("name", "email")):
        return {'message': 'Missing required fields'}, 400

    new_client = Client(
        name=data['name'],
        email=data['email']
    )
    db.session.add(new_client)
    db.session.commit()
    return {'message': 'Client created successfully'}, 201

# Endpoint to retrieve all clients
@app.route('/clients', methods=['GET'])
def get_clients():
    clients = Client.query.all()
    return jsonify([{'id': client.id, 'name': client.name, 'email': client.email} for client in clients]), 200

# Endpoint to get client by ID
@app.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    client = Client.query.get_or_404(client_id)
    return {'id': client.id, 'name': client.name, 'email': client.email}, 200

# Endpoint to update client
@app.route('/clients/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    client = Client.query.get_or_404(client_id)
    data = request.get_json()
    client.name = data.get('name', client.name)
    client.email = data.get('email', client.email)
    db.session.commit()
    return {'message': 'Client updated successfully'}, 200

# Endpoint to delete client
@app.route('/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    return {'message': 'Client deleted successfully'}, 200

if __name__ == '__main__':
    register_service() 
    app.run(port=5001, debug=True)
