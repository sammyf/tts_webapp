from typing import List


class Messages:
    def __init__(self):
        self.index: int = 0
        self.role: str = ""
        self.content: str = ""
        self.persona: str = 'Diem'

class LLMAnswer:
    def __init__(self) -> None:
        self.model: str = ""
        self.created_at: str = ""
        self.message: Messages = Messages()
        self.done: bool = False
        self.total_duration: int = 0
        self.load_duration: int = 0
        self.prompt_eval_count: int = 0
        self.prompt_eval_duration: int = 0
        self.eval_count: int = 0
        self.eval_duration: int = 0

    def jsonify(self):
        return {
            "model": self.model,
            "created_at": self.created_at,
            "message": {
                "index": self.message.index,
                "role": self.message.role,
                "content": self.message.content,
                "persona": self.message.persona
            },
            "done": self.done,
            "total_duration": self.total_duration,
            "load_duration": self.load_duration,
            "prompt_eval_count": self.prompt_eval_count,
            "prompt_eval_duration": self.prompt_eval_duration,
            "eval_count": self.eval_count,
            "eval_duration": self.eval_duration
        }