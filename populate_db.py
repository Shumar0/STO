from database import db, Client, ServiceRequest
import json

# Load input data
with open('new_input_data.json') as f:
    input_data = json.load(f)

# Insert clients
for client in input_data['clients']:
    try:
        existing_client = Client.query.filter_by(id=client['id']).first()
        if existing_client is None:  # Only add if the client does not exist
            new_client = Client(
                id=client['id'],
                first_name=client['first_name'],
                last_name=client['last_name'],
                phone_number=client['phone_number'],
                email=client.get('email'),
                address=client.get('address')
            )
            db.session.add(new_client)
            db.session.commit()
    except Exception as e:
        print(f"Error adding client: {str(e)}")

# Insert service requests
for request in input_data['service_requests']:
    try:
        # Check if the client exists before adding the service request
        existing_client = Client.query.filter_by(id=request['client_id']).first()
        if existing_client is not None:  # Only add if the client exists
            new_request = ServiceRequest(
                client_id=request['client_id'],
                car_id=request['car_id'],
                service_type=request['service_type'],
                issue_description=request['issue_description']
            )
            db.session.add(new_request)
            db.session.commit()
    except Exception as e:
        print(f"Error adding service request: {str(e)}")
