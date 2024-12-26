from flasgger import Swagger

def init_swagger(app):
    app.config['SWAGGER'] = {
        'title': 'API Documentation',
        'version': '1.0',
        'description': 'API documentation with JWT authentication',
        'securityDefinitions': {
            'JWT': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header'
            }
        }
    }
    """
    Initialize Swagger for the application.
    """
    swagger = Swagger(app, template={
        "swagger": "2.0",
        "info": {
            "title": "STO Service API Documentation",
            "version": "1.0.0",
            "description": "API для управління заявками на обслуговування в STO"
        },
        "basePath": "/",
        "schemes": ["http"],
        "paths": {  # Ensure this section is properly closed
            "/orders": {
                "post": {
                    "summary": "Create a new order",
                    "parameters": [
                        {
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "user_id": {"type": "integer"},
                                    "product_name": {"type": "string"},
                                    "quantity": {"type": "integer"}
                                }
                            }
                        }
                    ],
                    "responses": {
                        "201": {"description": "Order created successfully"},
                        "400": {"description": "Invalid input"}
                    }
                },
                "get": {
                    "summary": "Retrieve all orders",
                    "responses": {
                        "200": {
                            "description": "A list of orders",
                            "schema": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "integer"},
                                        "user_id": {"type": "integer"},
                                        "product_name": {"type": "string"},
                                        "quantity": {"type": "integer"}
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/orders/<int:order_id>": {
                "get": {
                    "summary": "Retrieve an order by ID",
                    "parameters": [
                        {
                            "name": "order_id",
                            "in": "path",
                            "required": True,
                            "type": "integer"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Order details",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer"},
                                    "user_id": {"type": "integer"},
                                    "product_name": {"type": "string"},
                                    "quantity": {"type": "integer"}
                                }
                            }
                        },
                        "404": {"description": "Order not found"}
                    }
                },
                "put": {
                    "summary": "Update an existing order",
                    "parameters": [
                        {
                            "name": "order_id",
                            "in": "path",
                            "required": True,
                            "type": "integer"
                        },
                        {
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "product_name": {"type": "string"},
                                    "quantity": {"type": "integer"}
                                }
                            }
                        }
                    ],
                    "responses": {
                        "200": {"description": "Order updated successfully"},
                        "404": {"description": "Order not found"}
                    }
                },
                "delete": {
                    "summary": "Delete an order",
                    "parameters": [
                        {
                            "name": "order_id",
                            "in": "path",
                            "required": True,
                            "type": "integer"
                        }
                    ],
                    "responses": {
                        "200": {"description": "Order deleted successfully"},
                        "404": {"description": "Order not found"}
                    }
                }
            }
        }
    })
    
    if 'flasgger' not in app.blueprints:
        app.register_blueprint(swagger.blueprint)
