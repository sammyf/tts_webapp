import sqlite3

from config import DB_NAME, OLLAMA_URL
import requests
from celery import Celery

from main import celery


