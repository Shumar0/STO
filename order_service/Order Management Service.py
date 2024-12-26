from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import jwt_required
from swagger_config import init_swagger  # Import Swagger config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/shared_service.db'  # Use a shared database
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Set your JWT secret key
app.config['JWT_HEADER_NAME'] = 'Authorization'  # Set JWT header name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize Swagger
init_swagger(app)  # Initialize Swagger using the imported config

# Order model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)  # Foreign key to Client
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Create tables
@app.before_first_request
def create_tables():
    db.create_all()  # Create all tables
    db.session.commit()  # Commit changes to ensure tables are created
    if not Order.query.first():  # Check if there are no orders
        sample_order = Order(user_id=1, product_name='Sample Product', quantity=10)
        db.session.add(sample_order)
        db.session.commit()  # Add a sample order

# Example endpoint to create an order
@app.route('/orders', methods=['POST'])
# Remove JWT authentication
def create_order():
    data = request.get_json()
    new_order = Order(
        user_id=data['user_id'],
        product_name=data['product_name'],
        quantity=data['quantity']
    )
    db.session.add(new_order)
    db.session.commit()
    return {'message': 'Order created successfully', 'order_id': new_order.id}, 201

# Endpoint to retrieve all orders
@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([{'id': order.id, 'user_id': order.user_id, 'product_name': order.product_name, 'quantity': order.quantity} for order in orders]), 200

# Endpoint to retrieve an order by ID
@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return {
        'id': order.id,
        'user_id': order.user_id,
        'product_name': order.product_name,
        'quantity': order.quantity
    }, 200

# Endpoint to update an order
@app.route('/orders/<int:order_id>', methods=['PUT'])
@jwt_required()
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    order.product_name = data.get('product_name', order.product_name)
    order.quantity = data.get('quantity', order.quantity)
    db.session.commit()
    return {'message': 'Order updated successfully'}, 200

# Endpoint to delete an order
@app.route('/orders/<int:order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return {'message': 'Order deleted successfully'}, 200

if __name__ == '__main__':
    app.run(port=5002, debug=True)
