from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/Study/Fourth year/СОАПЗ/STO_project/databases/service_registry.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    url = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200))
    version = db.Column(db.String(20))

class Endpoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    path = db.Column(db.String(200), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(200))
    input_params = db.Column(db.JSON)
    output_params = db.Column(db.JSON)
    auth_required = db.Column(db.Boolean, default=False)

@app.before_first_request
def create_tables():
    db.create_all()

def generate_service_config():
    services = Service.query.all()
    service_config = {}
    for service in services:
        endpoints = Endpoint.query.filter_by(service_id=service.id).all()
        service_config[service.name] = {
            'url': service.url,
            'status': service.status,
            'description': service.description,
            'version': service.version,
            'endpoints': [{
                'path': endpoint.path,
                'method': endpoint.method,
                'description': endpoint.description
            } for endpoint in endpoints]
        }
    return service_config

def list_all_services():
    services = Service.query.all()
    for service in services:
        print(f"Service ID: {service.id}, Name: {service.name}, URL: {service.url}, Status: {service.status}, Description: {service.description}, Version: {service.version}")
        endpoints = Endpoint.query.filter_by(service_id=service.id).all()
        for endpoint in endpoints:
            print(f"  Endpoint: {endpoint.path}, Method: {endpoint.method}, Description: {endpoint.description}")

if __name__ == '__main__':
    create_tables()  # Ensure tables are created
    config = generate_service_config()
    print(config)  # Output the service configuration
    list_all_services()  # List all services and their endpoints
