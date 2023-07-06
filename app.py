
import numpy as np
from random import choice
from bidict import bidict
from flask import Flask, render_template, request, redirect, url_for, session

"""
ENCODER = bidict({
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6,
    'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12,
    'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18,
    'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24,
    'Y': 25, 'Z': 26
})
"""
ENCODER = bidict({
    'ა': 1, 'ბ': 2, 'გ': 3, 'დ': 4, 'ე': 5, 'ვ': 6,
    'ზ': 7, 'თ': 8, 'ი': 9, 'კ': 10, 'ლ': 11, 'მ': 12,
    'ნ': 13, 'ო': 14, 'პ': 15, 'ჟ': 16, 'რ': 17, 'ს': 18,
    'ტ': 19, 'უ': 20, 'ფ': 21, 'ქ': 22, 'ღ': 23, 'ყ': 24,
    'შ': 25, 'ჩ': 26,'ც':27, 'ძ':28, 'წ':29, 'ჭ':30, 'ხ':31, 'ჯ':32, 'ჰ': 33
})
app = Flask(__name__)
app.secret_key = 'quiz'
@app.route('/')

def index():
    return render_template('index.html')


@app.route('/check_letter', methods=['POST'])
def check_result():
    type = request.form['type'] # ეს არის ტიპი რომელი გაიგზავნა ციფრი, ასო, თუ სიტყვა
    f = request.files['file']
    f.save('new.png')
    
    #model = keras.models.load_model('scripts/geo_model.model')
    #result = np.argmax(model.predict(img), axis=-1)
    result = "test"

    return render_template('index.html', result=result, type = type)


@app.route('/check_digit', methods=['POST'])
def check_digit_result():
    type = request.form['type'] # ეს არის ტიპი რომელი გაიგზავნა ციფრი, ასო, თუ სიტყვა
    f = request.files['file']
    f.save('new.png')
        
    #model = keras.models.load_model('scripts/geo_model.model')
    #result = np.argmax(model.predict(img), axis=-1)
    result = "test"

    return render_template('index.html', result=result, type = type)


@app.route('/check_word', methods=['POST'])
def check_word_result():
    type = request.form['type'] # ეს არის ტიპი რომელი გაიგზავნა ციფრი, ასო, თუ სიტყვა
    f = request.files['file']
    f.save('new.png')
    #model = keras.models.load_model('scripts/geo_model.model')
    #result = np.argmax(model.predict(img), axis=-1)
    result = "test"

    return render_template('index.html', result = result, type = type)


if __name__ == '__main__':
    app.run(debug=True)