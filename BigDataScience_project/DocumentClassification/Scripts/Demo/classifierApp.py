import os
import cv2
import base64
from DocClassifier import *

import io

from flask import Flask, request
from flask import render_template

import json

app = Flask(__name__)
classifer = Classifier()

@app.route('/')
def hello():
    return render_template("index.html")  # "Hello World!"

@app.route('/find', methods=["POST"])
def find_cow():
    decoded_data = base64.b64decode(request.form['img'].replace('data:image/jpeg;base64,',''))
    np_data = np.fromstring(decoded_data, np.uint8)
    img = cv2.imdecode(np_data, cv2.IMREAD_COLOR)

    result = classifer.find_category(img)
    print(result)
    return json.dumps(result)

def getData():
    return None

if __name__ == '__main__':
    app.run()