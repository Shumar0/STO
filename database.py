from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sto.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model for Client
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID generated automatically
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    service_requests = db.relationship('ServiceRequest', backref='client', lazy=True)  # Relationship with service requests

# Model for ServiceRequest
class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)  # Relationship with client
    car_id = db.Column(db.Integer, nullable=False)
    service_type = db.Column(db.String(50), nullable=False)
    issue_description = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default='new')

# Model for Order
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)  # Relationship with client
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Function to create tables
def create_tables():
    db.create_all()
    print("Tables created successfully.")

# Function to add a new client
def add_client(first_name, last_name, phone_number, email=None, address=None):
    new_client = Client(
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        email=email,
        address=address
    )
    db.session.add(new_client)
    db.session.commit()
    return new_client

# Function to get all clients
def get_all_clients():
    return Client.query.all()

# Function to create a new service request
def add_service_request(client_id, car_id, service_type, issue_description):
    new_request = ServiceRequest(
        client_id=client_id,
        car_id=car_id,
        service_type=service_type,
        issue_description=issue_description
    )
    db.session.add(new_request)
    db.session.commit()
    return new_request

# Function to get all service requests
def get_all_service_requests():
    return ServiceRequest.query.all()

if __name__ == '__main__':
    create_tables()
