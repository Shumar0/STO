import requests

class OrderServiceAccess:
    def __init__(self):
        self.order_service_url = 'http://localhost:5002'

    def create_order(self, client_id, product_name, quantity):
        response = requests.post(f'{self.order_service_url}/orders', json={'client_id': client_id, 'product_name': product_name, 'quantity': quantity})
        return response.json()

    def get_orders(self):
        response = requests.get(f'{self.order_service_url}/orders')
        return response.json()

    def update_order(self, order_id, product_name=None, quantity=None):
        data = {}
        if product_name:
            data['product_name'] = product_name
        if quantity:
            data['quantity'] = quantity
        response = requests.put(f'{self.order_service_url}/orders/{order_id}', json=data)
        return response.json()

    def delete_order(self, order_id):
        response = requests.delete(f'{self.order_service_url}/orders/{order_id}')
        return response.json()
