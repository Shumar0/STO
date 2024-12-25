from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flasgger import Swagger
from database import db, ServiceRequest, Client
from swagger_config import init_swagger

# Ініціалізувати Flask додаток
app = Flask(__name__)

# Налаштування бази даних
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sto.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Ініціалізувати API та Swagger
api = Api(app)
init_swagger(app)

# Ініціалізувати базу даних
@app.before_first_request
def init_db():
    db.create_all()

# Тестовий маршрут для перевірки з'єднання з базою даних
@app.route('/test-db', methods=['GET'])
def test_db():
    try:
        clients = Client.query.all()
        return jsonify({'clients': [client.first_name for client in clients]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Мікросервіс: Створити заявку на обслуговування
class CreateServiceRequest(Resource):
    def post(self):
        """
        Create a new service request
        ---
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                client_id:
                  type: integer
                car_id:
                  type: integer
                service_type:
                  type: string
                issue_description:
                  type: string
        responses:
          201:
            description: Заявку на обслуговування успішно створено
        """
        data = request.get_json()
        if not all(key in data for key in ['client_id', 'car_id', 'service_type', 'issue_description']):
            return {'error': 'Недійсні вхідні дані'}, 400
        
        new_request = ServiceRequest(
            client_id=data['client_id'],
            car_id=data['car_id'],
            service_type=data['service_type'],
            issue_description=data['issue_description']
        )
        db.session.add(new_request)
        db.session.commit()
        return {
            'request_id': new_request.id,
            'client_id': new_request.client_id,
            'service_type': new_request.service_type,
            'status': 'створено'
        }, 201

# Мікросервіс: Оновити статус заявки на обслуговування
class UpdateServiceRequestStatus(Resource):
    def put(self, request_id):
        """
        Update the status of a service request
        ---
        parameters:
          - name: request_id
            in: path
            required: true
            type: integer
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                status:
                  type: string
        responses:
          200:
            description: Статус успішно оновлено
        """
        data = request.get_json()
        if 'status' not in data:
            return {'error': 'Статус є обовязковим'}, 400
        
        request_to_update = ServiceRequest.query.get_or_404(request_id)
        request_to_update.status = data['status']
        db.session.commit()
        return {'status': request_to_update.status}, 200

# Мікросервіс: Переглянути історію заявок на обслуговування
class ViewServiceRequestHistory(Resource):
    def get(self, client_id):
        """
        Переглянути історію заявок на обслуговування для клієнта
        ---
        parameters:
          - name: client_id
            in: path
            required: true
            type: integer
        responses:
          200:
            description: Історію заявок на обслуговування успішно отримано
        """
        requests = ServiceRequest.query.filter_by(client_id=client_id).all()
        if not requests:
            return {'error': 'Заявки для цього клієнта не знайдено'}, 404
        
        requests_list = [{'request_id': req.id, 'service_type': req.service_type, 'status': req.status} for req in requests]
        return requests_list, 200

# Мікросервіс: Призначити майстра для заявки
class AssignMasterToRequest(Resource):
    def post(self, request_id):
        """
        Призначити майстра для заявки на обслуговування
        ---
        parameters:
          - name: request_id
            in: path
            required: true
            type: integer
        responses:
          200:
            description: Майстра успішно призначено
        """
        request_to_assign = ServiceRequest.query.get_or_404(request_id)
        request_to_assign.status = 'призначено'
        db.session.commit()
        return {'status': 'майстра призначено', 'request_id': request_to_assign.id}, 200

# Мікросервіс: Розрахувати вартість обслуговування
class CalculateServiceCost(Resource):
    def post(self, request_id):
        """
        Розрахувати вартість заявки на обслуговування
        ---
        parameters:
          - name: request_id
            in: path
            required: true
            type: integer
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                service_type:
                  type: string
        responses:
          200:
            description: Вартість успішно розраховано
        """
        data = request.get_json()
        if 'service_type' not in data:
            return {'error': 'Тип обслуговування є обовязковим'}, 400
        
        cost = 100 if data['service_type'] == 'repair' else 50
        return {'request_id': request_id, 'cost': cost}, 200

# Мікросервіс: Створити нового клієнта
class CreateClient(Resource):
    def post(self):
        """
        Створити нового клієнта
        ---
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                first_name:
                  type: string
                last_name:
                  type: string
                phone_number:
                  type: string
                email:
                  type: string
                address:
                  type: string
        responses:
          201:
            description: Клієнта успішно створено
        """
        data = request.get_json()
        if not all(key in data for key in ['first_name', 'last_name', 'phone_number']):
            return {'error': 'Відсутні обовязкові поля'}, 400
        
        new_client = Client(
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone_number=data['phone_number'],
            email=data.get('email', None),
            address=data.get('address', None)
        )
        db.session.add(new_client)
        db.session.commit()
        return {
            'client_id': new_client.id,
            'status': 'створено'
        }, 201

# Реєстрація маршрутів
api.add_resource(CreateClient, '/clients')
api.add_resource(CreateServiceRequest, '/service-requests')
api.add_resource(UpdateServiceRequestStatus, '/service-requests/<int:request_id>/status')
api.add_resource(ViewServiceRequestHistory, '/service-requests/history/<int:client_id>')
api.add_resource(AssignMasterToRequest, '/service-requests/<int:request_id>/assign-master')
api.add_resource(CalculateServiceCost, '/service-requests/<int:request_id>/calculate-cost')

# Запустити програму
if __name__ == '__main__':
    app.run(debug=True)
