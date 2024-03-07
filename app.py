from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import NoCredentialsError

app = Flask(__name__)

# AWS S3 Configuration
S3_BUCKET = 'your-s3-bucket-name'
S3_ACCESS_KEY = 'your-s3-access-key'
S3_SECRET_KEY = 'your-s3-secret-key'

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        if file:
            s3 = boto3.client('s3', aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_KEY)
            s3.upload_fileobj(file, S3_BUCKET, file.filename)
            return jsonify({"message": "File uploaded successfully"})
    except NoCredentialsError:
        return jsonify({"error": "AWS credentials not available"})

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        s3 = boto3.client('s3', aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_KEY)
        response = s3.get_object(Bucket=S3_BUCKET, Key=filename)
        return response['Body'].read()
    except NoCredentialsError:
        return jsonify({"error": "AWS credentials not available"})

@app.route('/query/<filename>', methods=['GET'])
def query_file(filename):
    # Add your CSV querying logic here
    #for example 
    #''' SELECT * FROM s3object s LIMIT 5'''
    return jsonify({"message": "Query logic to be implemented"})

if __name__ == '__main__':
    app.run(debug=True)