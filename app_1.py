from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from jose import jwt
import boto3

app = Flask(__name__)
bcrypt = Bcrypt()

# AWS Cognito Configuration
COGNITO_REGION = 'your-cognito-region'
COGNITO_USER_POOL_ID = 'your-user-pool-id'
COGNITO_APP_CLIENT_ID = 'your-app-client-id'

# Bcrypt Configuration
BCRYPT_LOG_ROUNDS = 12

def get_cognito_client():
    return boto3.client('cognito-idp', region_name=COGNITO_REGION)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        cognito_client = get_cognito_client()
        response = cognito_client.sign_up(
            ClientId=COGNITO_APP_CLIENT_ID,
            Username=email,
            Password=password,
            UserAttributes=[
                {'Name': 'email', 'Value': email},
            ]
        )

        return jsonify({"message": "User signed up successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        cognito_client = get_cognito_client()
        response = cognito_client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password,
            },
            ClientId=COGNITO_APP_CLIENT_ID,
        )

        access_token = response['AuthenticationResult']['AccessToken']
        return jsonify({"access_token": access_token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@app.route('/upload', methods=['POST'])
def upload_file():
    # Implement secure access to this endpoint using JWT (access_token)
    # Retrieve access token from the Authorization header and validate it
    access_token = request.headers.get('Authorization')

    if not access_token:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        jwt.decode(access_token, algorithms=['RS256'], options={'verify_aud': False}, verify=False)
        # Add your S3 upload logic here
        return jsonify({"message": "File uploaded successfully"})
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.JWTError:
        return jsonify({"error": "Invalid token"}), 401

if __name__ == '__main__':
    app.run(debug=True)
