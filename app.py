from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flasgger import Swagger
from database import db, ServiceRequest, Client
from swagger_config import init_swagger

# Initialize Flask app
app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sto.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Initialize API and Swagger
api = Api(app)
init_swagger(app)

# Initialize database
@app.before_first_request
def init_db():
    db.create_all()

# Microservice: Create a service request
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
            description: Service request created successfully
        """
        data = request.get_json()
        if not all(key in data for key in ['client_id', 'car_id', 'service_type', 'issue_description']):
            return jsonify({'error': 'Invalid input data'}), 400
        
        new_request = ServiceRequest(
            client_id=data['client_id'],
            car_id=data['car_id'],
            service_type=data['service_type'],
            issue_description=data['issue_description']
        )
        db.session.add(new_request)
        db.session.commit()
        return jsonify({'request_id': new_request.id, 'status': 'created'}), 201

# Microservice: Update service request status
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
            description: Status updated successfully
        """
        data = request.get_json()
        if 'status' not in data:
            return jsonify({'error': 'Status is required'}), 400
        
        request_to_update = ServiceRequest.query.get_or_404(request_id)
        request_to_update.status = data['status']
        db.session.commit()
        return jsonify({'status': request_to_update.status}), 200

# Microservice: View service request history
class ViewServiceRequestHistory(Resource):
    def get(self, client_id):
        """
        View service request history for a client
        ---
        parameters:
          - name: client_id
            in: path
            required: true
            type: integer
        responses:
          200:
            description: Service request history retrieved successfully
        """
        requests = ServiceRequest.query.filter_by(client_id=client_id).all()
        if not requests:
            return jsonify({'error': 'No requests found for this client'}), 404
        
        requests_list = [{'request_id': req.id, 'service_type': req.service_type, 'status': req.status} for req in requests]
        return jsonify(requests_list), 200

# Microservice: Assign a master to a request
class AssignMasterToRequest(Resource):
    def post(self, request_id):
        """
        Assign a master to a service request
        ---
        parameters:
          - name: request_id
            in: path
            required: true
            type: integer
        responses:
          200:
            description: Master assigned successfully
        """
        request_to_assign = ServiceRequest.query.get_or_404(request_id)
        request_to_assign.status = 'assigned'
        db.session.commit()
        return jsonify({'status': 'master assigned', 'request_id': request_to_assign.id}), 200

# Microservice: Calculate service cost
class CalculateServiceCost(Resource):
    def post(self, request_id):
        """
        Calculate the cost of a service request
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
            description: Cost calculated successfully
        """
        data = request.get_json()
        if 'service_type' not in data:
            return jsonify({'error': 'Service type is required'}), 400
        
        cost = 100 if data['service_type'] == 'repair' else 50
        return jsonify({'request_id': request_id, 'cost': cost}), 200

# Microservice: Create a new client
class CreateClient(Resource):
    def post(self):
        """
        Create a new client
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
            description: Client created successfully
        """
        data = request.get_json()
        if not all(key in data for key in ['first_name', 'last_name', 'phone_number']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        new_client = Client(
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone_number=data['phone_number'],
            email=data.get('email', None),
            address=data.get('address', None)
        )
        db.session.add(new_client)
        db.session.commit()
        return jsonify({'client_id': new_client.id, 'status': 'created'}), 201

# Register routes
api.add_resource(CreateClient, '/clients')
api.add_resource(CreateServiceRequest, '/service-requests')
api.add_resource(UpdateServiceRequestStatus, '/service-requests/<int:request_id>/status')
api.add_resource(ViewServiceRequestHistory, '/service-requests/history/<int:client_id>')
api.add_resource(AssignMasterToRequest, '/service-requests/<int:request_id>/assign-master')
api.add_resource(CalculateServiceCost, '/service-requests/<int:request_id>/calculate-cost')


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
