from flask import request
from flask_restx import Resource, Api, Namespace
import random

# Define a Flask-RestX Namespace for the VAD Analyzer API
Danger = Namespace(
    name='Danger',
    description='Danger Analysis API'
)

@Danger.route('')
class DangerAnalyzer(Resource):
    def get(self):  
        response_data = {
            "response": "Hello"
        }
        return response_data
    