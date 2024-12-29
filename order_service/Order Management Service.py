from flask import Flask, request, jsonify
from datetime import datetime  # Import datetime for timestamping
import os
import sys
import signal
from flask_sqlalchemy import SQLAlchemy
from models import db  # Import the db instance from models.py
from flask_migrate import Migrate  # Import Flask-Migrate

print("Starting Order Management Service...")
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/Study/Fourth year/СОАПЗ/STO_project/databases/order_service.db'  
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  
app.config['JWT_HEADER_NAME'] = 'Authorization'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)
from flask_jwt_extended import jwt_required
# Initialize Flask-Migrate
migrate = Migrate(app, db)  # Link Flask app and SQLAlchemy database
from swagger_config import init_swagger  
from sqlalchemy import inspect
import requests

# Initialize Swagger
init_swagger(app) 

# Client model
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

# Order model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)  # Foreign key to Client
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Create tables if they do not exist
@app.before_first_request
def create_tables():
    print("Creating tables...")
    print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])
    
    try:
        # Drop existing tables
        db.drop_all()  # Drop all tables if they exist
        db.create_all()  # Create all tables
        print("Tables created successfully.")
    except Exception as e:
        print("Error creating tables:", e)

# Register service with the service registry
def register_service():
    service_info = {
        'name': 'Order Management Service',
        'url': 'http://localhost:5002',
        'status': 'active'
    }
    # Register the service with the service registry
    response = requests.post('http://localhost:5000/services', json=service_info)
    if response.status_code == 201:
        print('Order Management Service registered successfully.')
    else:
        print('Failed to register Order Management Service:', response.text)  # Changed to response.text
        print('Response Status Code:', response.status_code)
        print('Response Content:', response.content)

# Add signal handler for graceful shutdown
signal.signal(signal.SIGINT, lambda s, f: stop_service())
signal.signal(signal.SIGTERM, lambda s, f: stop_service())

if __name__ == '__main__':
    register_service()  # Ensure the service registers itself
    app.run(port=5002, debug=True)

# Ensure all functions are correctly integrated with necessary models and relationships
# Example endpoint to create an order request
@app.route('/order_requests', methods=['POST'])
def create_order_request():
    data = request.get_json()
    new_order_request = OrderRequest(
        client_id=data['client_id'],
        car_id=data['car_id'],
        service_type=data['service_type'],
        issue_description=data['issue_description'],
        created_at=datetime.utcnow()
    )
    db.session.add(new_order_request)
    db.session.commit()
    return {'message': 'Order request created successfully', 'order_request_id': new_order_request.id}, 201

# Endpoint to retrieve all order requests
@app.route('/order_requests', methods=['GET'])
def get_order_requests():
    order_requests = OrderRequest.query.all()
    return jsonify([{
        'id': order_request.id,
        'client_id': order_request.client_id,
        'car_id': order_request.car_id,
        'service_type': order_request.service_type,
        'issue_description': order_request.issue_description,
        'status': order_request.status,
        'created_at': order_request.created_at
    } for order_request in order_requests]), 200

# Endpoint to retrieve an order request by ID
@app.route('/order_requests/<int:order_request_id>', methods=['GET'])
def get_order_request(order_request_id):
    order_request = OrderRequest.query.get_or_404(order_request_id)
    return {
        'id': order_request.id,
        'client_id': order_request.client_id,
        'car_id': order_request.car_id,
        'service_type': order_request.service_type,
        'issue_description': order_request.issue_description,
        'status': order_request.status,
        'created_at': order_request.created_at
    }, 200

# Endpoint to update an order request
@app.route('/order_requests/<int:order_request_id>', methods=['PUT'])
@jwt_required()
def update_order_request(order_request_id):
    order_request = OrderRequest.query.get_or_404(order_request_id)
    data = request.get_json()
    order_request.service_type = data.get('service_type', order_request.service_type)
    order_request.issue_description = data.get('issue_description', order_request.issue_description)
    order_request.status = data.get('status', order_request.status)
    db.session.commit()
    return {'message': 'Order request updated successfully'}, 200

# Endpoint to delete an order request
@app.route('/order_requests/<int:order_request_id>', methods=['DELETE'])
@jwt_required()
def delete_order_request(order_request_id):
    order_request = OrderRequest.query.get_or_404(order_request_id)
    db.session.delete(order_request)
    db.session.commit()
    return {'message': 'Order request deleted successfully'}, 200

def stop_service():
    print("Stopping Order Management Service...")
    sys.exit(0)

def restart_service():
    print("Restarting Order Management Service...")
    stop_service()
    os.execv(sys.executable, ['python'] + sys.argv)
