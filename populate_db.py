from database import db, Client, ServiceRequest
import json

# Завантажити вхідні дані
with open('new_input_data.json') as f:
    input_data = json.load(f)

# Вставити клієнтів
for client in input_data['clients']:
    try:
        existing_client = Client.query.filter_by(id=client['id']).first()
        if existing_client is None:  # Додавати тільки якщо клієнт не існує
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
        print(f"Помилка при додаванні клієнта: {str(e)}")

# Вставити заявки на обслуговування
for request in input_data['service_requests']:
    try:
        # Перевірити, чи існує клієнт перед додаванням заявки
        existing_client = Client.query.filter_by(id=request['client_id']).first()
        if existing_client is not None:  # Додавати тільки якщо клієнт існує
            new_request = ServiceRequest(
                client_id=request['client_id'],
                car_id=request['car_id'],
                service_type=request['service_type'],
                issue_description=request['issue_description']
            )
            db.session.add(new_request)
            db.session.commit()
    except Exception as e:
        print(f"Помилка при додаванні заявки: {str(e)}")
