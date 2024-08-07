class QueueObject:
    def __init__(self, id=0, prompt=""):
        self._id = id
        self._prompt = prompt
        self._answer = ""

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def prompt(self):
        return self._prompt

    @prompt.setter
    def prompt(self, value):
        self._prompt = value

    @property
    def answer(self):
        return self._answer

    @answer.setter
    def answer(self, value):
        self._answer = value
