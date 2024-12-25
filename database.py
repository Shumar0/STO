from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sto.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель для клієнта
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID generated automatically
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    service_requests = db.relationship('ServiceRequest', backref='client', lazy=True)  # Зв'язок з заявками

# Модель для заявки
class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)  # Зв'язок з клієнтом
    car_id = db.Column(db.Integer, nullable=False)
    service_type = db.Column(db.String(50), nullable=False)
    issue_description = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default='new')

# Функція для створення таблиць
def create_tables():
    db.create_all()

# Функція для додавання нового клієнта
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

# Функція для отримання всіх клієнтів
def get_all_clients():
    return Client.query.all()

# Функція для створення нової заявки
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

# Функція для отримання всіх заявок
def get_all_service_requests():
    return ServiceRequest.query.all()

if __name__ == '__main__':
    create_tables()
