import boto3
import botocore
import os
from flask import flash, redirect, request, url_for
from time import time
from urllib.parse import urlparse
from werkzeug import secure_filename


s3 = boto3.client("s3", aws_access_key_id=os.getenv("S3_ACCESS_KEY"), aws_secret_access_key=os.getenv("S3_SECRET_ACCESS_KEY"))


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# Handle aspect ratios here?

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def handle_file(file_form_name):
    if file_form_name not in request.files:
        flash("File not found", "info")
        return None

    files = request.files.getlist('user_image')
    print(files)

    for file in files:
        if file.filename == "":
            flash("Please provide a file name", "info")
            return None

        if file and allowed_file(file.filename):
            print(file)
            file.filename = secure_filename(file.filename)
            # file.filename = str(round(time()*987654321))[10:]
            print(file)
    return files

def upload_to_s3(file, bucket_name, acl="public-read"):
    try:
        s3.upload_fileobj(file, bucket_name, file.filename, ExtraArgs={"ACL": acl, "ContentType": file.content_type})

    
    except Exception as e:
        print(e)
        flash(str(e), "danger")
        return redirect(url_for("images.new"))
    
    return file.filename

def handle_upload(file_form_name):
    files = handle_file(file_form_name)
    if not files:
        return None
    
    paths = []
    for file in files: 
        paths.append(upload_to_s3(file, os.getenv("S3_BUCKET")))
    return paths


def full_paths(paths):
    bucket = os.getenv('S3_BUCKET')
    AWS_DOMAIN = f'https://s3.amazonaws.com/{bucket}'
    full_paths = []
    for path in paths:
        full_paths.append(f"{AWS_DOMAIN}/{path}")
    return full_paths