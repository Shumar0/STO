from flask import Flask, request, jsonify, send_from_directory
from flask_restful import Api, Resource
from flasgger import Swagger
from database import db, create_tables, add_client, get_all_clients, add_service_request, get_all_service_requests, Client, ServiceRequest

app = Flask(__name__)
swagger = Swagger(app)  # Initialize Swagger

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sto.db'  # Використовуємо SQLite для зберігання даних
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

api = Api(app)

# Serve the HTML form
@app.route('/')
def serve_form():
    return send_from_directory('', 'index.html')

# Serve Swagger UI documentation
@app.route('/swagger/')
def serve_swagger():
    return swagger.get_swaggerui_blueprint()

# Remove duplicate model definitions

# Ініціалізація бази даних
@app.before_first_request
def create_tables():
    db.create_all()

# Мікросервіс для створення клієнта
class CreateClient(Resource):
    def post(self):
        """
        Create a new client
        ---
        parameters:
          - name: first_name
            type: string
            required: true
            description: The first name of the client
          - name: last_name
            type: string
            required: true
            description: The last name of the client
          - name: phone_number
            type: string
            required: true
            description: The phone number of the client
          - name: email
            type: string
            required: false
            description: The email of the client
          - name: address
            type: string
            required: false
            description: The address of the client
        responses:
          200:
            description: Client created successfully
            schema:
              id: Client
              properties:
                client_id:
                  type: integer
                  description: The ID of the created client
                unique_number:
                  type: string
                  description: The unique number assigned to the client
                status:
                  type: string
                  description: The status of the request
        """
        data = request.get_json()
        new_client = Client(
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone_number=data['phone_number'],
            email=data.get('email'),
            address=data.get('address')
        )
        db.session.add(new_client)
        db.session.commit()
        return jsonify({'client_id': new_client.id, 'unique_number': new_client.unique_number, 'status': 'created'})

# Мікросервіс для створення заявки
class CreateServiceRequest(Resource):
    def post(self):
        """
        Create a new service request
        ---
        parameters:
          - name: client_id
            type: integer
            required: true
            description: The ID of the client
          - name: car_id
            type: integer
            required: true
            description: The ID of the car
          - name: service_type
            type: string
            required: true
            description: The type of service
          - name: issue_description
            type: string
            required: true
            description: Description of the issue
        responses:
          200:
            description: Request created successfully
            schema:
              id: ServiceRequest
              properties:
                request_id:
                  type: integer
                  description: The ID of the created request
                status:
                  type: string
                  description: The status of the request
        """
        data = request.get_json()
        new_request = ServiceRequest(
            client_id=data['client_id'],
            car_id=data['car_id'],
            service_type=data['service_type'],
            issue_description=data['issue_description']
        )
        db.session.add(new_request)
        db.session.commit()
        return jsonify({'request_id': new_request.id, 'status': 'created'})

# Мікросервіс для оновлення статусу заявки
class UpdateServiceRequestStatus(Resource):
    def put(self, request_id):
        """
        Update the status of a service request
        ---
        parameters:
          - name: request_id
            type: integer
            required: true
            description: The ID of the request
          - name: status
            type: string
            required: true
            description: The new status of the request
        responses:
          200:
            description: Status updated successfully
            schema:
              id: StatusUpdate
              properties:
                status:
                  type: string
                  description: The updated status of the request
        """
        data = request.get_json()
        request_to_update = ServiceRequest.query.get_or_404(request_id)
        request_to_update.status = data['status']
        db.session.commit()
        return jsonify({'status': request_to_update.status})

# Мікросервіс для перегляду історії заявок
class ViewServiceRequestHistory(Resource):
    def get(self, client_id):
        """
        View the history of service requests for a client
        ---
        parameters:
          - name: client_id
            type: integer
            required: true
            description: The ID of the client
        responses:
          200:
            description: List of service requests
            schema:
              type: array
              items:
                id: ServiceRequestHistory
                properties:
                  request_id:
                    type: integer
                    description: The ID of the request
                  service_type:
                    type: string
                    description: The type of service
                  status:
                    type: string
                    description: The status of the request
        """
        requests = ServiceRequest.query.filter_by(client_id=client_id).all()
        requests_list = [{'request_id': req.id, 'service_type': req.service_type, 'status': req.status} for req in requests]
        return jsonify(requests_list)

# Мікросервіс для призначення майстра для заявки
class AssignMasterToRequest(Resource):
    def post(self, request_id):
        """
        Assign a master to a service request
        ---
        parameters:
          - name: request_id
            type: integer
            required: true
            description: The ID of the request
        responses:
          200:
            description: Master assigned successfully
            schema:
              id: MasterAssignment
              properties:
                status:
                  type: string
                  description: The assignment status
                request_id:
                  type: integer
                  description: The ID of the request
        """
        data = request.get_json()
        request_to_assign = ServiceRequest.query.get_or_404(request_id)
        request_to_assign.status = 'assigned'
        db.session.commit()
        return jsonify({'status': 'master assigned', 'request_id': request_to_assign.id})

# Мікросервіс для розрахунку вартості заявки
class CalculateServiceCost(Resource):
    def post(self, request_id):
        """
        Calculate the cost of a service request
        ---
        parameters:
          - name: request_id
            type: integer
            required: true
            description: The ID of the request
        responses:
          200:
            description: Cost calculated successfully
            schema:
              id: ServiceCost
              properties:
                request_id:
                  type: integer
                  description: The ID of the request
                cost:
                  type: number
                  description: The calculated cost
        """
        data = request.get_json()
        cost = data['service_type'] == 'repair' and 100 or 50  # 100 для ремонту, 50 для звичайного обслуговування
        return jsonify({'request_id': request_id, 'cost': cost})

# Реєстрація маршрутів для кожного мікросервісу
api.add_resource(CreateClient, '/clients')
api.add_resource(CreateServiceRequest, '/service-requests')
api.add_resource(UpdateServiceRequestStatus, '/service-requests/<int:request_id>/status')
api.add_resource(ViewServiceRequestHistory, '/service-requests/history/<int:client_id>')
api.add_resource(AssignMasterToRequest, '/service-requests/<int:request_id>/assign-master')
api.add_resource(CalculateServiceCost, '/service-requests/<int:request_id>/calculate-cost')

if __name__ == '__main__':
    app.run(debug=True)
