import json
import os
import boto3

def load_file_from_S3(key, bucket):
    """Download file from S3 to /tmp/ folder"""
    local_path = key.split('/')[-1]
    filename = f'/tmp/{local_path}'
    s3 = boto3.client('s3')
    s3.download_file(bucket, key, f'/tmp/{local_path}')

def upload_file_to_s3(key, bucket):
    """Upload local file in /tmp/ to S3 bucket"""
    local_path = key.split('/')[-1]
    s3 = boto3.client('s3')
    with open(f'/tmp/{local_path}', "rb") as f:
        s3.upload_fileobj(f, bucket, key)


def lambda_handler(event, context):
    """Main function run when Lambda is invoked"""
    # Get variables from payload    
    key_in = event.get('file_key_input')
    bucket_in = event.get('bucket_input')
    key_out = event.get('file_key_output')
    bucket_out = event.get('bucket_output')
    
    # Get the filename
    file_name = key_in.split('/')[-1]
    
    # Load files on local temp folder
    load_file_from_S3(key_in, bucket_in)
    
    # List files on /tmp/
    os.system('ls -la /tmp/')

    # Change permission for executing wkhtmltopdf
    os.system('cp -r ./wkhtmltox /tmp/')
    os.system('ls -la /tmp/')
    os.system('chmod -R 755 /tmp/wkhtmltox')
    
    # Run wkhtmltopdf
    os.system(f"/tmp/wkhtmltox/bin/wkhtmltopdf --help")
    os.system(f"/tmp/wkhtmltox/bin/wkhtmltopdf /tmp/{file_name} /tmp/{file_name.replace('.html', '.pdf')}")

    # Upload output file to S3
    upload_file_to_s3(key_out, bucket_out)

    return {'statusCode':200,
        'body':'wkhtmltopdf Lambda success!'}