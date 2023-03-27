from flask import Flask 
from flask_restx import Api, Resource  
from user import User
from danger import Danger
from realty import Realty

# Create Flask app instance
app = Flask(__name__)  

# Create Flask-RestX API instance
api = Api(
    app,
    version='0.1',  # API version
    title="HOMEY",  # API title
    description="HOMEY",  # API description
    terms_url="/",  # URL for API terms and conditions
    contact="seungjaelim@kaist.ac.kr",  # API contact email
    license="MIT"  # API license
)

# Add namespace to the API
api.add_namespace(User, '/user')
api.add_namespace(Realty, '/realty')
api.add_namespace(Danger, '/danger')

# Start the Flask app
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
