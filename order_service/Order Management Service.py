from flask import Flask, request, jsonify
import os  # Import os module for file operations
import sys
import signal
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import jwt_required
from swagger_config import init_swagger  
from sqlalchemy import inspect
import requests

print("Starting Order Management Service...")
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/Study/Fourth year/СОАПЗ/STO_project/databases/order_service.db'  
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  
app.config['JWT_HEADER_NAME'] = 'Authorization'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

# Example endpoint to create an order
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    new_order = Order(
        client_id=data['client_id'],
        product_name=data['product_name'],
        quantity=data['quantity']
    )
    db.session.add(new_order)
    db.session.commit()
    return {'message': 'Order created successfully', 'order_id': new_order.id}, 201

# Endpoint to retrieve all orders
@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([{'id': order.id, 'client_id': order.client_id, 'product_name': order.product_name, 'quantity': order.quantity} for order in orders]), 200

# Endpoint to retrieve an order by ID
@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return {
        'id': order.id,
        'client_id': order.client_id,
        'product_name': order.product_name,
        'quantity': order.quantity
    }, 200

# Endpoint to update an order
@app.route('/orders/<int:order_id>', methods=['PUT'])
@jwt_required()
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    order.product_name = data.get('product_name', order.product_name)
    order.quantity = data.get('quantity', order.quantity)
    db.session.commit()
    return {'message': 'Order updated successfully'}, 200

# Endpoint to delete an order
@app.route('/orders/<int:order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return {'message': 'Order deleted successfully'}, 200

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
        print('Failed to register Order Management Service:', response.json())
        print('Response Status Code:', response.status_code)
        print('Response Content:', response.content)
    service_info = {
        'name': 'Order Management Service',
        'url': 'http://localhost:5002',
        'status': 'active'
    }

def stop_service():
    print("Stopping Order Management Service...")
    sys.exit(0)

def restart_service():
    print("Restarting Order Management Service...")
    stop_service()
    os.execv(sys.executable, ['python'] + sys.argv)

# Add signal handler for graceful shutdown
signal.signal(signal.SIGINT, lambda s, f: stop_service())
signal.signal(signal.SIGTERM, lambda s, f: stop_service())

if __name__ == '__main__':
    app.run(port=5002, debug=True)
