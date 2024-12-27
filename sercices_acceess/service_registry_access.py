import requests

class ServiceRegistryAccess:
    def __init__(self):
        self.service_registry_url = 'http://localhost:5000/services'

    def register_service(self, name, url):
        service_info = {
            'name': name,
            'url': url,
            'status': 'active'
        }
        response = requests.post(self.service_registry_url, json=service_info)
        return response.json()

    def get_services(self):
        response = requests.get(self.service_registry_url)
        return response.json()
