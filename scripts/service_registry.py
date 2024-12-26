from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///service_registry.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    url = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/services', methods=['GET'])
def list_services():
    services = Service.query.all()
    return jsonify([{ 'name': service.name, 'url': service.url, 'status': service.status } for service in services]), 200

@app.route('/services', methods=['POST'])
def register_service():
    data = request.get_json()
    if not all(key in data for key in ['name', 'url', 'status']):
        return {'error': 'Missing required fields'}, 400
    new_service = Service(name=data['name'], url=data['url'], status=data['status'])
    db.session.add(new_service)
    db.session.commit()
    return {'message': 'Service registered successfully'}, 201

@app.route('/health', methods=['GET'])
def health_check():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
