import boto3

# Your AWS access and secret keys
access_key = 'AKIA6JQ44V4GPDRHX5FL'
secret_key = ''
bucket_name = 'plantanthracnose'
file_name = r"D:\pycharm_projects\leaf\detected"
folder_name = 'green/'  # Specify the folder within the bucket
object_name = f'{folder_name}uploaded_image.jpg'  # The path in the bucket

# Create a session using your credentials
session = boto3.Session(
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
)

# Create an S3 client
s3 = session.client('s3')

# Upload the file
try:
    s3.upload_file(file_name, bucket_name, object_name)
    print(f'Successfully uploaded {file_name} to {bucket_name}/{object_name}')
except Exception as e:
    print(f'Error uploading file: {e}')