from flasgger import Swagger

def init_swagger(app):
    """
    Initialize Swagger for the application.
    """
    # Ініціалізувати Swagger без аргументу імені
    swagger = Swagger(app, template={
        "swagger": "2.0",
        "info": {
            "title": "STO Service API Documentation",
            "version": "1.0.0",
            "description": "API для управління заявками на обслуговування в STO"
        },
        "basePath": "/",
        "schemes": ["http"],
        "paths": {
            "/clients": {
                "post": {
                    "summary": "Створити нового клієнта",
                    "parameters": [
                        {
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "first_name": {"type": "string"},
                                    "last_name": {"type": "string"},
                                    "phone_number": {"type": "string"},
                                    "email": {"type": "string"},
                                    "address": {"type": "string"}
                                }
                            }
                        }
                    ],
                    "responses": {
                        "201": {"description": "Клієнта успішно створено"},
                        "400": {"description": "Відсутні обов'язкові поля"},
                        "500": {"description": "Помилка при створенні клієнта"}
                    }
                }
            },
            "/service-requests": {
                "post": {
                    "summary": "Створити нову заявку на обслуговування",
                    "parameters": [
                        {
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "client_id": {"type": "integer"},
                                    "car_id": {"type": "integer"},
                                    "service_type": {"type": "string"},
                                    "issue_description": {"type": "string"}
                                }
                            }
                        }
                    ],
                    "responses": {
                        "201": {"description": "Заявку на обслуговування успішно створено"},
                        "400": {"description": "Помилка при створенні заявки на обслуговування"},
                        "500": {"description": "Помилка обробки запиту"}
                    }
                }
            }
        }
    })
    
    # Зареєструвати Swagger blueprint вручну, якщо потрібно
    if 'flasgger' not in app.blueprints:
        app.register_blueprint(swagger.blueprint)
