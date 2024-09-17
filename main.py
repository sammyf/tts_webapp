from http.client import responses
from urllib.parse import urljoin

from flask import Flask, request, send_from_directory, send_file, jsonify
import requests
import os
import datetime
import glob
import json
import ollama
import chromadb

from flask_cors import CORS
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

CORS(app)


EMBED_MODEL = "nomic-embed-text:latest"
@app.route('/')
def index():
    return send_from_directory('html', 'index.html')


@app.route('/output/<fn>', methods=['GET', 'POST'])
def return_wave_file(fn):
    return send_file("voices/" + fn, mimetype='audio/x-wav')


@app.route('/generate', methods=['POST'])
def generate_wave_file():
    return ('http://tts.cosmic-bandito.com/assets/ping'), 200


@app.route('/companion/tts/output/<fn>', methods=['GET'])
def return_wave_file_beezle(fn):
    return send_file("assets/ping.wav", mimetype='audio/x-wav')


@app.route('/companion/tts/generate', methods=['POST'])
def generate_wave_file_beezle():
    text = request.json.get('text')
    voice = request.json.get('voice')

    fname = "ping.wav"

    return jsonify(url=fname), 200


@app.route('/companion/spider', methods=['POST'])
def get_url_content():
    url = request.json.get('url')
    print(url + " <- URL found!")
    try:
        # Make a GET request to the url
        response = requests.get(url)
        returnCode = response.status_code
        # Parse the web page content
        soup = BeautifulSoup(response.text, 'html.parser')
        linkList = ""
        for a in soup.findAll('a'):
            link = urljoin(url, a.get('href'))
            a.string = " "+a.text + "(href: '" + link + "') "
        # Get textual part of the page
        content = soup.get_text()
        # Return the content
        return jsonify({"content": content, "returnCode": returnCode}), 200
    except Exception as e:
        return jsonify({"content": "error :" + str(e), "returnCode": 500}), 200


@app.before_request
def log_request_info():
    return

def purge_voices():
    # get all .wav files in the voices directory
    files = glob.glob('voices/*.wav')

    # sort files by date (descending)
    files.sort(key=os.path.getmtime, reverse=True)

    # delete all except the newest 10 files
    for file in files[10:]:
        os.remove(file)

@app.route('/companion/embed_memory', methods=['POST'])
def embed_memories():
    print("embedding ...")
    summary = request.json.get('summary')
    uid = request.json.get('uid')
    memid = request.json.get('memid')

    print(uid)
    print(memid)
    client = chromadb.PersistentClient(path="/mnt/beezledb/beezle_"+str(uid)+".db")
    collection = client.get_or_create_collection(name='memories')
    response = ollama.embeddings(model=EMBED_MODEL, prompt=summary)
    embedding = response['embedding']
    print('embeddings : ',embedding)
    if embedding is None:
        print("empty embedding")
        return jsonify("no embed"), 200
    collection.add(
        ids=[str(memid)],
        embeddings=[embedding],
        documents=[str(memid)]
    )
    return jsonify("ok"), 200


@app.route('/companion/retrieve_memory', methods=['POST'])
def retrieve_memories():
    print("\nretrieving ...")
    prompt = request.json.get('prompt')
    uid = request.json.get('uid')
    response =ollama.embeddings(
        prompt=prompt,
        model=EMBED_MODEL
    )
    client = chromadb.PersistentClient(path="/mnt/beezledb/beezle_"+str(uid)+".db")
    collection = client.get_collection(name='memories')
    results = collection.query(
        query_embeddings = [response['embedding']],
        n_results = 1
    )
    print(results)
    data = results['documents'][0][0]
    print("retrieved!\n")
    return jsonify({ 'id': int(data) } ), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=21998)
