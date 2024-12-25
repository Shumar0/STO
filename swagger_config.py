from flasgger import Swagger

def init_swagger(app):
    """
    Initialize Swagger for the application.
    """
    # Initialize Swagger without the name argument
    swagger = Swagger(app, template={
        "swagger": "2.0",
        "info": {
            "title": "STO Service API Documentation",
            "version": "1.0.0",
            "description": "API for managing service requests at an STO"
        },
        "basePath": "/",
        "schemes": ["http"],
        "paths": {
            "/clients": {
                "post": {
                    "summary": "Create a new client",
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
                        "201": {"description": "Client created successfully"},
                        "400": {"description": "Missing required fields"},
                        "500": {"description": "Error creating client"}
                    }
                }
            },
            "/service-requests": {
                "post": {
                    "summary": "Create a new service request",
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
                        "201": {"description": "Service request created successfully"},
                        "400": {"description": "Error creating service request"},
                        "500": {"description": "Error processing request"}
                    }
                }
            }
        }
    })
    
    # Register Swagger blueprint manually if needed
    if 'flasgger' not in app.blueprints:
        app.register_blueprint(swagger.blueprint)

