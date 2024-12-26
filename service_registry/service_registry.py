from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from swagger_config import init_swagger  # Re-importing init_swagger

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/Study/Fourth year/СОАПЗ/STO_project/databases/service_registry.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
init_swagger(app)  # Ініціалізувати Swagger

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

@app.route('/services', methods=['GET'])
def list_services():
    services = Service.query.all()
    return jsonify([{
        'id': service.id,
        'name': service.name,
        'url': service.url,
        'status': service.status,
        'description': service.description,
        'version': service.version
    } for service in services]), 200

@app.route('/services', methods=['POST'])
def register_service():
    data = request.get_json()
    if not all(key in data for key in ['name', 'url', 'status']):
        return {'error': 'Відсутні обов’язкові поля'}, 400
    new_service = Service(name=data['name'], url=data['url'], status=data['status'])
    db.session.add(new_service)
    db.session.commit()
    return {'message': 'Сервіс успішно зареєстровано'}, 201

@app.route('/health', methods=['GET'])
def health_check():
    return {'status': 'здоровий'}, 200

if __name__ == '__main__':
    create_tables()  # Ensure tables are created
    app.run(port=5000, debug=True)
