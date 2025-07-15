from datetime import datetime
from .survey_enums import SurveyStatus
from typing import Optional

class Survey:
    def __init__(
        self,
        id: int,
        title: str,
        description: str = "",
        created_at: Optional[ datetime ] = None,
        status: SurveyStatus = SurveyStatus.DRAFT,
        questions: Optional[ list ] = None
    ):
        self.id = id
        self.title = title
        self.description = description
        self.created_at = created_at or datetime.now()
        self.status = status
        self.questions = questions if questions is not None else []

    def __repr__(self):
        return f"<Survey id={self.id} title={self.title}>"

    def add_question(self, question):
        self.questions.append(question)

    def activate(self):
        if not self.questions:
            raise ValueError("No se puede activar una encuesta sin preguntas.")
        self.status = SurveyStatus.ACTIVE

    def close(self):
        self.status = SurveyStatus.CLOSED
