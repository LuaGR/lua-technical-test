from typing import Optional, List
from .question_enums import QuestionType

class Option:
    def __init__(self, id: int, question_id: int, text: str):
        self.id = id
        self.question_id = question_id
        self.text = text

    def __repr__(self):
        return f"<Option id={self.id} text={self.text}>"

class Question:
    def __init__(
        self,
        id: int,
        survey_id: int,
        text: str,
        question_type: QuestionType,
        options: Optional[List[Option]] = None,
        required: bool = False
    ):
        self.id = id
        self.survey_id = survey_id
        self.text = text
        self.question_type = question_type
        self.options = options if options is not None else []
        self.required = required

    def __repr__(self):
        return f"<Question id={self.id} text={self.text} type={self.question_type.value}>"

    def add_option(self, option: Option):
        if self.question_type not in [QuestionType.SINGLE_CHOICE, QuestionType.MULTIPLE_CHOICE]:
            raise ValueError("Solo las preguntas de tipo choice pueden tener opciones.")
        self.options.append(option)
