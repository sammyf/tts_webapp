## TTS Webapp

Just a small webapp to generate Text2Speech wav files using a specific voice from coqui's *tts* package.

This app is also used as a companion for ollamaui ( https://github.com/sammyf/ollamaui ) to help it access the internet and, of course, to generate TTS Files.

**IMPORTANT** : if you need this for ollamaui but don't want or can't use the TTS output, then clone the branch `companion-light`  
### Requirements
* python < 3.11 (as a tts package doesn't exist for python3.11 or 3.12)

### Installation

**GNU/Linux :**

* clone this repo, change the URLs and ports in main.py and html/index.html to match your requirements.

* create a virtual environment with

`python3.10 -m venv .venv`

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
