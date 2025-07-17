from typing import Optional, List
from .question_enums import QuestionType
from .option_entity import Option

class Question:
    def __init__(
        self,
        id: Optional[ int ],
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
            raise ValueError("Only choice type questions can have options.")
        self.options.append(option)
