from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import jwt_required
from swagger_config import init_swagger  # Import Swagger config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/shared_service.db'  # Use a shared database
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Set your JWT secret key
app.config['JWT_HEADER_NAME'] = 'Authorization'  # Set JWT header name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize Swagger
init_swagger(app)  # Initialize Swagger using the imported config

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

# Example endpoint to create a client
@app.route('/clients', methods=['POST'])
def create_client():
    data = request.get_json()
    new_client = Client(
        name=data['name'],
        email=data['email']
    )
    db.session.add(new_client)
    db.session.commit()
    return {'message': 'Client created successfully', 'client_id': new_client.id}, 201

# Endpoint to retrieve all clients
@app.route('/clients', methods=['GET'])
def get_clients():
    clients = Client.query.all()
    return jsonify([{'id': client.id, 'name': client.name, 'email': client.email} for client in clients]), 200

# Endpoint to retrieve a client by ID
@app.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    client = Client.query.get_or_404(client_id)
    return {
        'id': client.id,
        'name': client.name,
        'email': client.email
    }, 200

# Endpoint to update a client
@app.route('/clients/<int:client_id>', methods=['PUT'])
@jwt_required()
def update_client(client_id):
    client = Client.query.get_or_404(client_id)
    data = request.get_json()
    client.name = data.get('name', client.name)
    client.email = data.get('email', client.email)
    db.session.commit()
    return {'message': 'Client updated successfully'}, 200

# Endpoint to delete a client
@app.route('/clients/<int:client_id>', methods=['DELETE'])
@jwt_required()
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    return {'message': 'Client deleted successfully'}, 200

if __name__ == '__main__':
    app.run(port=5001, debug=True)
