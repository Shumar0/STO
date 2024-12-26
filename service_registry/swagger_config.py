from flasgger import Swagger

def init_swagger(app):
    """Ініціалізувати Swagger для Flask додатку."""
    swagger = Swagger(app, template={
        "swagger": "2.0",
        "info": {
            "title": "API реєстрації сервісів",
            "version": "1.0",
            "description": "API для управління реєстраціями сервісів"
        },
        "basePath": "/",
        "paths": {
            "/services": {  # Endpoint for managing services
                "get": {
                    "summary": "Список всіх зареєстрованих сервісів",  # Retrieves all registered services
                    "responses": {
                        "200": {
                            "description": "Список сервісів",
                            "schema": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "integer", "description": "ID сервісу"},
                                        "name": {"type": "string", "description": "Назва сервісу"},
                                        "url": {"type": "string", "description": "URL сервісу"},
                                        "status": {"type": "string", "description": "Статус сервісу"},
                                        "description": {"type": "string", "description": "Опис сервісу"},
                                        "version": {"type": "string", "description": "Версія сервісу"}
                                    }
                                }
                            }
                        }
                    }
                },
                "post": {
                    "summary": "Зареєструвати новий сервіс",  # Register a new service
                    "parameters": [
                        {
                            "name": "service",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string", "description": "Назва сервісу"},
                                    "url": {"type": "string", "description": "URL сервісу"},
                                    "status": {"type": "string", "description": "Статус сервісу"}
                                }
                            }
                        }
                    ],
                    "responses": {
                        "201": {"description": "Сервіс успішно зареєстровано"},
                        "400": {"description": "Відсутні обов’язкові поля"}
                    }
                }
            },
            "/health": {
                "get": {
                    "summary": "Перевірка стану реєстрації сервісу",  # Health check for the service registry
                    "responses": {
                        "200": {
                            "description": "Сервіс здоровий"  # Service is healthy
                        }
                    }
                }
            }
        }
    })
    return swagger
