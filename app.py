import numpy as np
from random import choice
from bidict import bidict
from flask import Flask, render_template, request, redirect, url_for, session
from PIL import Image, ImageOps
from random import randint
import cv2
from ultralytics import YOLO

ENCODER = bidict({
    'ა': 1, 'ბ': 2, 'გ': 3, 'დ': 4, 'ე': 5, 'ვ': 6,
    'ზ': 7, 'თ': 8, 'ი': 9, 'კ': 10, 'ლ': 11, 'მ': 12,
    'ნ': 13, 'ო': 14, 'პ': 15, 'ჟ': 16, 'რ': 17, 'ს': 18,
    'ტ': 19, 'უ': 20, 'ფ': 21, 'ქ': 22, 'ღ': 23, 'ყ': 24,
    'შ': 25, 'ჩ': 26, 'ც': 27, 'ძ': 28, 'წ': 29, 'ჭ': 30, 'ხ': 31, 'ჯ': 32, 'ჰ': 33
})
app = Flask(__name__)
app.secret_key = 'quiz'
model = YOLO('models/train6/weights/best.pt')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add-data', methods=['GET'])
def add_data_get():
    message = session.get('message', '')
    letter = choice(list(ENCODER.keys()))

    # labels = np.load('data/geo_labels.npy')
    # count = {k:0 for k in ENCODER.keys()}
    # for label in labels:
    #     count[label] += 1
    # count = sorted(count.items(), key=lambda x: x[1])
    # letter = count[0][0]

    return render_template('addData.html', letter=letter, message=message)


@app.route('/add-data', methods=['POST'])
def add_data_post():
    label = request.form['letter']
    label = ENCODER[label]
    # labels = np.load('data/geo_labels.npy')
    # labels = np.append(labels, label)
    # np.save('data/geo_labels.npy', labels)

    pixels = request.form['pixels']
    pixels = pixels.split(',')
    img = np.array(pixels).astype(np.uint8).reshape(50, 50)
    image = Image.fromarray(img)

    # Save the image as a PNG
    parent = r"C:\Users\annch\OneDrive\Desktop\master\ხელნაწერები\board"
    image = ImageOps.invert(image)
    value = randint(0, 1000000000)
    image.save(f"{parent}/{label}/{value}.png")
    # imgs = np.load('data/geo_images.npy')
    # imgs = np.vstack([imgs, img])
    # np.save('data/geo_images.npy', imgs)

    session['message'] = f'"{label}" was added to the training dataset!'
    return redirect(url_for('add_data_get'))


@app.route('/practice', methods=['GET'])
def practice_get():
    letter = choice(list(ENCODER.keys()))
    return render_template('practice.html', letter=letter, correct='')


@app.route('/practice', methods=['POST'])
def practice_post():
    letter = request.form['letter']
    pixels = request.form['pixels']
    pixels = pixels.split(",")
    img = np.array(pixels).astype(np.uint8).reshape(50, 50, 1)
    img = cv2.bitwise_not(cv2.cvtColor(img, cv2.COLOR_GRAY2RGB))
    # model = keras.models.load_model('scripts/geo_model.model')
    # pred_letter = np.argmax(model.predict(img), axis=-1)
    # pred_letter = ENCODER.inverse[pred_letter[0]]
    results = model.predict(source=img)
    names_dict = results[0].names
    probs = results[0].probs.numpy()
    pred_letter = ENCODER.inverse[int(names_dict[probs.top1])]
    correct = 'Yes' if pred_letter == letter else "No"

    letter = choice(list(ENCODER.keys()))
    return render_template('practice.html', letter=letter, correct=correct, pred_letter=pred_letter)


if __name__ == '__main__':
    app.run(debug=True)
