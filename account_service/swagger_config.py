from flasgger import Swagger

def init_swagger(app):
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
        "paths": {
            "/accounts/register": {
                "post": {
                    "summary": "Register a new user",
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
                                    "email": {"type": "string"},
                                    "phone_number": {"type": "string"},
                                    "password": {"type": "string"}
                                }
                            }
                        }
                    ],
                    "responses": {
                        "201": {"description": "User registered successfully"},
                        "400": {"description": "Missing required fields"},
                        "409": {"description": "Email already exists"}
                    }
                }
            },
            "/accounts/login": {
                "post": {
                    "summary": "Login a user",
                    "parameters": [
                        {
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "email": {"type": "string"},
                                    "password": {"type": "string"}
                                }
                            }
                        }
                    ],
                    "responses": {
                        "200": {"description": "Login successful"},
                        "401": {"description": "Invalid credentials"}
                    }
                }
            },
            "/accounts/reset-password": {
                "post": {
                    "summary": "Reset user password",
                    "parameters": [
                        {
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "email": {"type": "string"}
                                }
                            }
                        }
                    ],
                    "responses": {
                        "200": {"description": "Password reset link sent"},
                        "404": {"description": "User not found"}
                    }
                }
            },
            "/accounts/{user_id}": {
                "get": {
                    "summary": "Get user profile",
                    "parameters": [
                        {
                            "name": "user_id",
                            "in": "path",
                            "required": True,
                            "type": "integer"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "User profile retrieved successfully",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "first_name": {"type": "string"},
                                    "last_name": {"type": "string"},
                                    "email": {"type": "string"},
                                    "phone_number": {"type": "string"}
                                }
                            }
                        },
                        "403": {"description": "Unauthorized access"},
                        "404": {"description": "User not found"}
                    }
                },
                "put": {
                    "summary": "Update user profile",
                    "parameters": [
                        {
                            "name": "user_id",
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
                                    "first_name": {"type": "string"},
                                    "last_name": {"type": "string"},
                                    "email": {"type": "string"},
                                    "phone_number": {"type": "string"}
                                }
                            }
                        }
                    ],
                    "responses": {
                        "200": {"description": "Profile updated successfully"},
                        "403": {"description": "Unauthorized access"},
                        "404": {"description": "User not found"}
                    }
                }
            },
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
                                    "name": {"type": "string"},
                                    "email": {"type": "string"}
                                }
                            }
                        }
                    ],
                    "responses": {
                        "201": {"description": "Client created successfully"},
                        "400": {"description": "Missing required fields"}
                    }
                },
                "get": {
                    "summary": "Retrieve all clients",
                    "responses": {
                        "200": {"description": "Clients retrieved successfully"}
                    }
                }
            },
            "/clients/{client_id}": {
                "get": {
                    "summary": "Get client by ID",
                    "parameters": [
                        {
                            "name": "client_id",
                            "in": "path",
                            "required": True,
                            "type": "integer"
                        }
                    ],
                    "responses": {
                        "200": {"description": "Client retrieved successfully"},
                        "404": {"description": "Client not found"}
                    }
                },
                "put": {
                    "summary": "Update client",
                    "parameters": [
                        {
                            "name": "client_id",
                            "in": "path",
                            "required": True,
                            "type": "integer"
                        },
                        {
                            "name": "body",
                            "in": "body",
                            "required": False,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "email": {"type": "string"}
                                }
                            }
                        }
                    ],
                    "responses": {
                        "200": {"description": "Client updated successfully"},
                        "404": {"description": "Client not found"}
                    }
                },
                "delete": {
                    "summary": "Delete client",
                    "parameters": [
                        {
                            "name": "client_id",
                            "in": "path",
                            "required": True,
                            "type": "integer"
                        }
                    ],
                    "responses": {
                        "200": {"description": "Client deleted successfully"},
                        "404": {"description": "Client not found"}
                    }
                }
            }
        }
    })

    # Register Swagger blueprint if needed
    if 'flasgger' not in app.blueprints:
        app.register_blueprint(swagger.blueprint)
