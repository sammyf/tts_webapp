## TTS Webapp

This branch of tts_app app is used as a companion for ollamaui ( https://github.com/sammyf/ollamaui ) to help it access and understand the internet.
It doesn't require the TTS package and will only return a ping instead of spoken words!

**IMPORTANT** : if you need this for ollamaui and want the TTS output, then clone the branch `master`  

### Requirements
* python

### Installation

**GNU/Linux :**

* clone this repo, change the URLs and ports in main.py and html/index.html to match your requirements.

* create a virtual environment with

`python -m venv .venv`

* activate it with

`source .venv/bin/activate`

* install the required packages with

`pip install -r requirements.txt`

* and start the server with

`python main.py`



**Windows** 

probably similar to GNU/Linux. No idea really as I don't have a Microsoft Windows partition anymore.

**MacOS**

See Windows, except that I never had a Mac nor an Apple device.
