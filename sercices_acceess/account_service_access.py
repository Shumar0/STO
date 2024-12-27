import requests

class AccountServiceAccess:
    def __init__(self):
        self.account_service_url = 'http://localhost:5001'

    def create_client(self, name, email):
        response = requests.post(f'{self.account_service_url}/clients', json={'name': name, 'email': email})
        return response.json()

    def get_clients(self):
        response = requests.get(f'{self.account_service_url}/clients')
        return response.json()

    def get_client_by_id(self, client_id):
        response = requests.get(f'{self.account_service_url}/clients/{client_id}')
        return response.json()

    def update_client(self, client_id, name=None, email=None):
        data = {}
        if name:
            data['name'] = name
        if email:
            data['email'] = email
        response = requests.put(f'{self.account_service_url}/clients/{client_id}', json=data)
        return response.json()

    def delete_client(self, client_id):
        response = requests.delete(f'{self.account_service_url}/clients/{client_id}')
        return response.json()

    # New user-related methods
    def register_user(self, first_name, last_name, email, phone_number, password):
        response = requests.post(f'{self.account_service_url}/accounts/register', json={
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone_number': phone_number,
            'password': password
        })
        return response.json()

    def login_user(self, email, password):
        response = requests.post(f'{self.account_service_url}/accounts/login', json={
            'email': email,
            'password': password
        })
        return response.json()

    def reset_password(self, email):
        response = requests.post(f'{self.account_service_url}/accounts/reset-password', json={
            'email': email
        })
        return response.json()

    def get_user_profile(self, user_id):
        response = requests.get(f'{self.account_service_url}/accounts/{user_id}')
        return response.json()

    def update_user_profile(self, user_id, first_name=None, last_name=None, email=None, phone_number=None):
        data = {}
        if first_name:
            data['first_name'] = first_name
        if last_name:
            data['last_name'] = last_name
        if email:
            data['email'] = email
        if phone_number:
            data['phone_number'] = phone_number
        response = requests.put(f'{self.account_service_url}/accounts/{user_id}', json=data)
        return response.json()
