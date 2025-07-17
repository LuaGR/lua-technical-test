from typing import Optional
from sqlalchemy.orm import Session

from ..domain.question_entity import Question
from ..domain.question_enums import QuestionType
from .question_model import QuestionModel

class QuestionRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create(self, question: Question) -> Question:
        question_model = QuestionModel(
            survey_id=question.survey_id,
            text=question.text,
            question_type=question.question_type.value,
            required=question.required
        )
        self.db.add(question_model)
        self.db.commit()
        self.db.refresh(question_model)
        return Question(
            id=question_model.id,
            survey_id=question_model.survey_id,
            text=question_model.text,
            question_type=QuestionType(question_model.question_type),
            required=question_model.required
        )

    def get_by_id(self, question_id: int) -> Optional[Question]:
        question_model = self.db.query(QuestionModel).filter(QuestionModel.id == question_id).first()
        if not question_model:
            return None
        return Question(
            id=question_model.id,
            survey_id=question_model.survey_id,
            text=question_model.text,
            question_type=QuestionType(question_model.question_type),
            required=question_model.required
        )
