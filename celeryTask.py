import sqlite3

from config import DB_NAME, OLLAMA_URL
import requests
from celery import Celery

from main import celery


@celery.task(bind=True)
def post_to_chat_api(self, uid, prompt):
    response = requests.post( OLLAMA_URL+'/api/chat', json=prompt)
    answer = response.text

    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()

    if response.status_code == 200:
        res = cur.execute('SELECT * FROM queue WHERE uuid = ?', (uid,))
        res.fetchone()
        if res is not None:
            cur.execute('UPDATE queue SET answer=? WHERE uuid = ?', (answer, uid,))
    else:
        cur.execute('UPDATE queue SET answer=? WHERE uuid = ?', (answer, uid,))
    con.commit()
    con.close()