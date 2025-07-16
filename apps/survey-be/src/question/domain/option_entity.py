class Option:
    def __init__(self, id: int, question_id: int, text: str):
        self.id = id
        self.question_id = question_id
        self.text = text

    def __repr__(self):
        return f"<Option id={self.id} text={self.text}>"
