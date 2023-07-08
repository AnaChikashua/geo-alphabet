import cv2
import numpy as np
from flask import Flask, render_template, request
from ultralytics import YOLO
from keras.models import load_model
from split_word import split_word
from config import ConstantConfig, ModelConfig

yolo_model_path = ModelConfig().yolo_model
digit_model = ModelConfig().digit_model
print(yolo_model_path)
model = YOLO(yolo_model_path)
dig_model = load_model(digit_model, compile=False)

ENCODER = ConstantConfig().ENCODER
app = Flask(__name__)
app.secret_key = 'quiz'


@app.route('/')
def index():
    return render_template('index.html')


def yolo_prediction(img):
    results = model.predict(source=img)
    names_dict = results[0].names
    probs = results[0].probs.numpy()
    pred_letter = ENCODER.inverse[int(names_dict[probs.top1])]
    return pred_letter


@app.route('/check_letter', methods=['POST'])
def check_result():
    _type = request.form['type']
    img = cv2.imdecode(np.frombuffer(request.files['file'].read(), np.uint8), cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    pred_letter = yolo_prediction(img)
    return render_template('index.html', result=pred_letter, type=_type)


@app.route('/check_digit', methods=['POST'])
def check_digit_result():
    _type = request.form['type']
    img = cv2.imdecode(np.fromstring(request.files['file'].read(), np.uint8), cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
    img = cv2.bitwise_not(img)
    img = cv2.resize(img, (28, 28), interpolation=cv2.INTER_NEAREST)
    img = img.reshape(1, 28, 28, 1)
    predict_value = dig_model.predict(img)
    result = np.argmax(predict_value)
    return render_template('index.html', result=result, type=_type)


@app.route('/check_word', methods=['POST'])
def check_word_result():
    _type = request.form['type']
    img = cv2.imdecode(np.fromstring(request.files['file'].read(), np.uint8), cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    chars = split_word(image=img, save_chars=False)
    result = []
    for char in chars:
        predict_letter = yolo_prediction(char)
        result.append(predict_letter)
    return render_template('index.html', result=''.join(result), type=_type)


if __name__ == '__main__':
    app.run(debug=True)
