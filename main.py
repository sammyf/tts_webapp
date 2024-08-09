from flask import Flask, request, send_from_directory, send_file, jsonify
import requests
import os
import datetime
import glob
import uuid
from celery import Celery
import json
import redis
from flask_cors import CORS
from bs4 import BeautifulSoup
import QueueObject
import Queue
from LLMAnswer import LLMAnswer
import sqlite3

import time

OLLAMA_URL="http://ollama.local:11111"

app = Flask(__name__)
CORS(app)

# Celery configuration
# Celery configuration
app.config['CELERY_broker_url'] = 'redis://localhost:6379/0'
app.config['result_backend'] = 'redis://localhost:6379/0'

# Initialise Celery
celery = Celery(app.name, broker=app.config['CELERY_broker_url'])
celery.conf.update(app.config)

DB_NAME='/tmp/beezleQueue.db'
con=sqlite3.connect(DB_NAME)
cur=con.cursor()

# cur.execute("DROP TABLE IF EXISTS queue")
cur.execute('CREATE TABLE IF NOT EXISTS  "queue" (	"uuid"	TEXT NOT NULL UNIQUE, 	"prompt"	TEXT,	"answer"	TEXT,	PRIMARY KEY("uuid"))')
con.commit()
con.close()

@app.route('/')
def index():
    return send_from_directory('html', 'index.html')


@app.route('/output/<fn>', methods=['GET', 'POST'])
def return_wave_file(fn):

    return send_file("audio/ping.wav", mimetype='audio/x-wav')

@app.route('/generate', methods=['POST'])
def generate_wave_file():

    return ('http://tts.cosmic-bandito.com/output/ping'),200


@app.route('/companion/tts/output/<fn>', methods=['GET'])
def return_wave_file_beezle(fn):
    return send_file("audio/ping.wav", mimetype='audio/x-wav')

@app.route('/companion/tts/generate', methods=['POST'])
def generate_wave_file_beezle():
    text = request.json.get('text')
    voice = request.json.get('voice')

    fname = "ping.wav"

    return jsonify(url=fname), 200

@app.route('/companion/spider', methods=['POST'])
def get_url_content():


    url = request.json.get('url')

    print(url+" <- URL found!")
    try:
        # Make a GET request to the url
        response = requests.get(url)


        returnCode = response.status_code
        # Parse the web page content
        soup = BeautifulSoup(response.text, 'html.parser')
        # Get textual part of the page
        content = soup.get_text()

        # Return the content
        return jsonify({"content": content, "returnCode": returnCode}), 200
    except Exception as e:
        return jsonify({"content": "error :"+str(e), "returnCode": 500}), 400


@app.before_request
def log_request_info():
    return

@app.route('/companion/ps', methods=['GET'])
def get_current_model():
    response = requests.get( OLLAMA_URL+'/api/ps')
    return response

@app.route('/companion/tags', methods=['GET'])
def get_models():
    response = requests.get( OLLAMA_URL+'/api/tags')
    return response

@celery.task(bind=True)
def post_to_chat_api(self, uid, prompt):
    response = requests.post( OLLAMA_URL+'/api/chat', json=prompt)
    answer = response.text

    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()

    if response.status_code == 200:
        res = cur.execute('SELECT * FROM queue WHERE uuid = ?', (uid,))
        res.fetchone()
        if res != None:
            cur.execute('UPDATE queue SET answer=? WHERE uuid = ?', (answer, uid,))
    else:
        cur.execute('UPDATE queue SET answer=? WHERE uuid = ?', (answer, uid,))
    con.commit()
    con.close()

@app.route('/companion/request', methods=['POST'])
def queue_request():
    prompt = request.get_json()
    raw = str(json.dumps(prompt))

    uid = str(uuid.uuid4())

    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute("INSERT INTO queue ( uuid, prompt, answer ) VALUES ( ?, ?, '')", (uid,raw))
    con.commit()

    post_to_chat_api.apply_async(args=[uid, prompt])

    print("\n\nUUID : ",uid,"\n\n")
    return jsonify({"uuid": uid}), 200

StillProcessingMsg = LLMAnswer()
StillProcessingMsg.model = "still processing"

@app.route('/companion/response/<uid>', methods=['GET'])
def get_response(uid):
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()

    res = cur.execute('SELECT answer FROM queue WHERE uuid = ?', (uid,))
    sqlAnswer = res.fetchone()
    if sqlAnswer != None:
        if(sqlAnswer == ''):
            con.close()
            return StillProcessingMsg.jsonify(), 200
        try:
            answer = json.loads(sqlAnswer[0])
        except Exception as e:
            con.close()
            return StillProcessingMsg.jsonify(), 200

        cur.execute('DElETE FROM queue WHERE uuid = ?', (uid,))
        con.commit()
        con.close()
        return answer, 200
    else:
        rs = LLMAnswer()
        rs.model = "not found"
        con.close()
        return rs.jsonify(), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=21998)
