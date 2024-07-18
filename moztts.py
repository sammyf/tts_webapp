import torch
from TTS.api import TTS

class MozTTS:
    tts = None
    devide = None

    bot_voice="tts_models/en/vctk/vits"
    bot_language="en"
    use_cuda=True

    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def load_model( self, model_name):
        self.tts = TTS(model_name).to(self.device)

    def moztts(self, sentence, bot_speaker, outpath):
        if self.tts is None:
            self.load_model(self.bot_voice)
        self.tts.tts_to_file(text=sentence, speaker=bot_speaker, file_path=outpath)

