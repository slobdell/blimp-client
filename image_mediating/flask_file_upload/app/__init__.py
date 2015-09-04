import base64
import os
import uuid

from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from werkzeug import secure_filename

app = Flask(__name__)
# from app import views


UPLOAD_FOLDER = './uploads'
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
    print request.form['b64jpeg']
    print request.form['phone_number']
    filename = "%s.jpg" % uuid.uuid4()
    full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(full_path, "w+") as f:
        f.write(base64.urlsafe_b64decode(request.form['b64jpeg'].encode("ascii")))

    return "worked"
    uploaded_file = request.files['file']
    if uploaded_file and _allowed_file(uploaded_file.filename):
        filename = secure_filename(uploaded_file.filename)
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "worked"
    raise Exception("File now allowed")
