from flask import Flask, render_template, request, redirect, url_for
from tensorflow.keras.preprocessing import image
from keras.models import load_model
import matplotlib.pyplot as plt
import numpy as np
import os

UPLOAD_FOLDER = 'static/file/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/validate', methods=['POST', 'GET'])
def validate():
    if request.method == 'POST':
        username = request.form.get('uname')
        password = request.form.get('upass')

        # Define valid credentials
        valid_users = {
            'admin': 'admin@123'
        }

        if username in valid_users and valid_users[username] == password:
            return render_template('index.html')
        else:
            return render_template('login.html', msg='Invalid Username or Password')

    elif request.method == 'GET':
        return render_template('login.html', msg='Please login')


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        classes = ['Skin cancer begining', 'Skin cancer maligaent', 'Atopic Dermatitis', 'Bullous Disease', 'Cellulitis Impetigo', 'Eczema', 'Exanthems and Drug Eruptions', 'Hair Loss and Alopecia', 'Monkeypox', 'Normal']

        file1 = request.files['filename']
        imgfile = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        
        os.makedirs(os.path.dirname(imgfile), exist_ok=True)
        
        file1.save(imgfile)
        model = load_model(r'D:\skin disease1\skin disease1\skin disease1\model_inception.h5')
        img_ = image.load_img(imgfile, target_size=(224, 224, 3))
        img_array = image.img_to_array(img_)
        img_processed = np.expand_dims(img_array, axis=0)
        img_processed /= 255.
        prediction = model.predict(img_processed)
        index = np.argmax(prediction)
        result = "Unknown"
        percentage = 0.0

        if index < len(classes):
            result = str(classes[index]).title()

        image_url = url_for('static', filename='file/' + file1.filename)

        return render_template('prediction_result.html', msg=result, src=imgfile, view='style=display:block', view1='style=display:none')
    elif request.method == 'GET':
        return render_template('index.html')

@app.route('/prediction_result')
def prediction_result():
    result = request.args.get('result')
    image_url = request.args.get('image_url')
    return render_template('prediction_result.html', result=result, image_url=image_url)

if __name__ == '__main__':
    app.run(debug=True, port=6864)
