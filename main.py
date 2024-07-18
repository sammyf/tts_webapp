from flask import Flask, request, send_from_directory, send_file
import os
import moztts
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
mozTTS = moztts.MozTTS()
@app.route('/')
def index():
    return send_from_directory('html', 'index.html')


@app.route('/output/<fn>', methods=['GET', 'POST'])
def return_wave_file(fn):

    return send_file("voices/"+fn, mimetype='audio/x-wav')

@app.route('/generate', methods=['POST'])
def generate_wave_file():
    text = request.form.get('txt')
    voice = request.form.get('voice')

    # get current date and time
    now = datetime.datetime.now()
    fname = now.strftime("%Y%m%d%H%M%S%f") + "_"+voice+".wav"

    mozTTS.moztts(text,voice,"voices/"+fname)

    return ('http://localhost:21998/output/')+fname,200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=21998)