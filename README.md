# MWEB-TASK
Prerequite for this project :
(a) AWS Account in place
(b) Assuming you have Python install on your machine install the following libraries 
   (i) Boto3 this allows one to interact with AWS resources including Amazon s3 -- pip install boto3
  (ii) Flask this framework is widely used for building REST APIs --pip install Flask

Once this is done, I have attached two python scripts ; app.py and app_1.py . These can be tested separately

using your shell/bash. 

Most the parameter in the script require your input as I cannot use my own AWS credentials for security reasons.

I have alos attached the CSV file to be uploaded on s3 (Lu-siblings).

For Postman testing please use the below:

Test the API:

Use a tool like Postman or curl to test the API.
To upload a file, send a POST request to http://127.0.0.1:5000/upload with the file attached.
To download a file, send a GET request to http://127.0.0.1:5000/download/filename.
To query a file, send a GET request to http://127.0.0.1:5000/query/filename
