from __future__ import division, print_function
# coding=utf-8
import os
import numpy as np

# Flask utils
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import tensorflow as tf

import cv2


from tensorflow.keras.models import model_from_json

app = Flask(__name__)

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights("model11.h5")
print("Loaded model from disk")

HEIGHT, WIDTH = 256, 256
post_model = tf.keras.models.load_model('model2.h5',custom_objects=None,compile=True)

model._make_predict_function()



print('Model loaded. Check http://127.0.0.1:5000/')


def imagePreprocessing(image, normalize=True):

    image = cv2.resize(image, (WIDTH, HEIGHT))
    
    # Applying GaussianBlur.
    blurred = cv2.blur(image, ksize=(int(WIDTH / 6), int(HEIGHT / 6)))
    image = cv2.addWeighted(image, 4, blurred, -4, 128)
    
    try:
        if normalize:
            image = image / 255
            image -= image.mean()
            return image
        else:
            return image
    except:
        return np.zeros((WIDTH, HEIGHT, 3))


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']

        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        img=cv2.imread(file_path)
    
    
        preds = model.predict(np.array([imagePreprocessing(img)]))
        ii = post_model.predict(preds)

        Y_sub = np.argmax(ii, axis=1)
        if(Y_sub[0]==0):
            result = 'no DR'
        elif(Y_sub[0]==1):
            result = 'Mild'
        elif(Y_sub[0]==2):
            result='Moderate'
        elif(Y_sub[0]==3):
            result='Severe'
        else:
            result='Proliferative DR'
        result =str(ii[0][0])+","+ str(ii[0][1])+","+ str(ii[0][2])+","+str(ii[0][3])+","+str(ii[0][4])+","+result            
        return result
    return None


if __name__ == '__main__':
    app.run(debug=True)

