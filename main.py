from flask import Flask, redirect,url_for, render_template, request,jsonify
import random
from tensorflow import keras
import cv2
import numpy as np
import base64

from tensorflow.keras.models import load_model
app = Flask(__name__)

model = keras.models.load_model('./mnist_classification.h5')
randoml=[]

@app.route("/home")
@app.route("/",methods=['GET'])
def home():
    if len(randoml)>0:
        randoml.clear()
    else:
        rando=random.randint(0, 9)
        randoml.append(rando)
    random_no=randoml[0]
    print(f"first random : {str(random_no)}")
    return render_template("home.html",random_no=random_no)

@app.route('/', methods=['POST'])
def canvas():
    # Recieve base64 data from the user form
    canvasdata = request.form['canvasimg']
    encoded_data = request.form['canvasimg'].split(',')[1]

    # Decode base64 image to python array
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Convert 3 channel image (RGB) to 1 channel image (GRAY)
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Resize to (28, 28)
    gray_image = cv2.resize(gray_image, (28, 28), interpolation=cv2.INTER_LINEAR)

    # Expand to numpy array dimenstion to (1, 28, 28)
    img = np.expand_dims(gray_image, axis=0)

    try:
        prediction = np.argmax(model.predict(img))
        print(f"Prediction Result : {str(prediction)}")
        pred=int(prediction)
        random_no=randoml[0]
        print(f"Second random no : {str(random_no)}")
        if pred ==random_no:
            response="Successfully Solved"
        else:
            response="Captcha is wrong"
        randoml.pop()
        return redirect(url_for("predict", response=response))
        # return render_template('result.html', response=prediction, success=True)
    except Exception as e:
        return render_template('home.html', response=str(e))

@app.route("/<response>")
def predict(response):
    return render_template("result.html", response=response)
if __name__ == "__main__":
    app.run(debug=True)