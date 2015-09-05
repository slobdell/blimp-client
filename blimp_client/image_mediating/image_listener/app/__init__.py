import base64
import os
import uuid

from flask import Flask
from flask import request
# from flask import redirect
# from flask import url_for
# from werkzeug import secure_filename

from blimp_client.image_mediating.tasks import send_photo
from blimp_client.global_settings import APP_SETTINGS

app = Flask(__name__)
# from app import views


UPLOAD_FOLDER = APP_SETTINGS["UPLOAD_FOLDER"]
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def _allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return "Hello world"


@app.route("/picture/", methods=['POST'])
def receive_picture():
    filename = "%s.jpg" % uuid.uuid4()
    full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(full_path, "w+") as f:
        f.write(base64.urlsafe_b64decode(request.form['b64jpeg'].encode("ascii")))
    send_photo.delay(filename, request.form["phone_num_or_email"])
    return "worked"
