from flask import request
from flask_restx import Resource, Api, Namespace
import random

# Define a Flask-RestX Namespace for the VAD Analyzer API
Realty = Namespace(
    name='Realty',
    description='Realty API'
)

# Define an empty list to store the response strings
responses = []

@Realty.route('')
class RealtyBasic(Resource):
    def get(self):  
        response_data = {
            "response": "Hello"
        }
        return response_data

    def post(self):
        # Extract the response string from the request
        response_str = request.data.decode()

        # Append the response string to the list of responses
        responses.append(response_str)

        # Return a message indicating success
        return {'message': f'Response "{response_str}" saved successfully.'}
