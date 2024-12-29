from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Таблиця Users
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(128), nullable=False)

# Таблиця Clients
class Client(User):  # Inherit from User
    __tablename__ = 'clients'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)  # Use ForeignKey to link to User
    address = db.Column(db.String(200))

# Таблиця Cars
class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    license_plate = db.Column(db.String(20), nullable=False, unique=True)

# Таблиця Order
class OrderRequest(db.Model):
    __tablename__ = 'order_requests'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    service_type = db.Column(db.String(50), nullable=False)
    issue_description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="created")
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime)

# Таблиця Masters
class Master(db.Model):
    __tablename__ = 'masters'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)

# Таблиця RequestAssignments
class RequestAssignment(db.Model):
    __tablename__ = 'request_assignments'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order_requests.id'), nullable=False)
    master_id = db.Column(db.Integer, db.ForeignKey('masters.id'), nullable=False)
    assigned_at = db.Column(db.DateTime, nullable=False)
