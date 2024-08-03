from flask import Flask, request, send_from_directory, send_file, jsonify
import requests
import os
import moztts
import datetime
from flask_cors import CORS
from bs4 import BeautifulSoup

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

    return ('http://tts.cosmic-bandito.com/output/')+fname,200


@app.route('/companion/tts/output/<fn>', methods=['GET'])
def return_wave_file_beezle(fn):

    return send_file("voices/"+fn, mimetype='audio/x-wav')

@app.route('/companion/tts/generate', methods=['POST'])
def generate_wave_file_beezle():
    text = request.json.get('text')
    voice = request.json.get('voice')

    # get current date and time
    now = datetime.datetime.now()
    fname = now.strftime("%Y%m%d%H%M%S%f") + "_"+voice+".wav"

    mozTTS.moztts(text,voice,"voices/"+fname)

    return jsonify(url=fname), 200

@app.route('/companion/spider/<cache>', methods=['POST'])
def get_url_content(cache):
    # Extract url from posted json
    data = request.get_json()
    url = data.get('url', '')

    try:
        # Make a GET request to the url
        response = requests.get(url)

        # Parse the web page content
        soup = BeautifulSoup(response.text, 'html.parser')
        # Get textual part of the page
        content = soup.get_text()

        # Return the content
        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.before_request
def log_request_info():
    print('Headers: %s', request.headers)
    print('Body: %s', request.get_data())
    print('--------------')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=21998)