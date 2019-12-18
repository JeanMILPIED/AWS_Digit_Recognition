from flask import Flask, render_template, request
from imageio import imread
from PIL import Image, ImageChops
from keras.preprocessing import image
import sys
import os
import re
import base64
from flask_cors import CORS

from keras.models import load_model
import tensorflow as tf
import numpy as np

app = Flask(__name__)
CORS(app)

# Path to our saved model
sys.path.append(os.path.abspath("./cnn-mnist"))
#Initialize some global variables


global model, graph
model = load_model('./cnn-mnist')
graph = graph = tf.get_default_graph()

@app.route('/')
def index():
    return render_template("index.html")

from PIL import Image

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

def convertImage(imgData1):
  imgstr = re.search(r'base64,(.*)', str(imgData1)).group(1)
  with open('output.png', 'wb') as output:
    output.write(base64.b64decode(imgstr))

def loadImage(filename):
        img_rows = img_cols = 28
        img = Image.open(filename).convert('L')
        img = trim(img)
        img_1 = img.resize((28,28),Image.NEAREST)
        print(img_1.size)
        img_2 = image.img_to_array(img_1)
        print(img_2.size)
        
        #.reshape(img_1.size[1], img_1.size[0])
        img_2 = img_2 / 255
        # Reshape from (28,28) to (1,28,28,1) : 1 sample, 28x28 pixels, 1 channel (B/W)
        img_3 = np.expand_dims(img_2, axis=0)
        img_3 = np.expand_dims(img_3, axis=0)
        img_4 = np.reshape(img_3, (1,img_cols,img_rows,1))
        return np.array(img_4)

@app.route('/predict/', methods=['GET', 'POST'])
def predict():
    print("Leo")

    #print(model.summary())

    imgData = request.get_data()
    convertImage(imgData)


    img = loadImage("output.png")

    with graph.as_default():
        classes = model.predict(img)
        predicted = np.argmax(classes)
        print(predicted)
        return str(predicted)

    return str(response[0])


    print(imgData)

    return "leo"

if __name__ == "__main__":
# run the app locally on the given port
    app.run(host='0.0.0.0', port=5000)
