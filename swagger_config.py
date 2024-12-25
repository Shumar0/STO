from flasgger import Swagger

def init_swagger(app):
    """
    Initialize Swagger for the application.
    """
    Swagger(app, template={
        "swagger": "2.0",
        "info": {
            "title": "STO Service API Documentation",
            "version": "1.0.0",
            "description": "API for managing service requests at an STO"
        },
        "basePath": "/",
        "schemes": ["http"],
        "paths": {}
    })
