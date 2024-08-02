import cloudinary
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

cloudinary.config(
    cloud_name = os.environ.get("CLOUDINARY_NAME"),
    api_key = os.environ.get("CLOUDINARY_API_KEY"),
    api_secret = os.environ.get("CLOUDINARY_API_SECRET"),
    secure = True
)

import cloudinary.uploader
import cloudinary.api

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cloud_upload(file):
    url = cloudinary.uploader.upload(file)
    return url