from typing import Optional, List
from sqlalchemy.orm import Session, joinedload

from ..domain.survey_entity import Survey
from ..domain.survey_enums import SurveyStatus
from .survey_model import SurveyModel
from question.domain.question_entity import Question
from question.domain.option_entity import Option
from question.domain.question_enums import QuestionType
from question.infrastructure.question_model import QuestionModel

class SurveyRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create(self, survey: Survey) -> Survey:
        survey_model = SurveyModel(
            title=survey.title,
            description=survey.description,
            created_at=survey.created_at,
            status=survey.status.value
        )
        self.db.add(survey_model)
        self.db.commit()
        self.db.refresh(survey_model)
        return Survey(
            id=survey_model.id,
            title=survey_model.title,
            description=survey_model.description,
            created_at=survey_model.created_at,
            status=SurveyStatus(survey_model.status)
        )

    def get_by_id(self, survey_id: int) -> Optional[Survey]:
        survey_model = (
            self.db.query(SurveyModel)
            .options(
                joinedload(SurveyModel.questions).joinedload(QuestionModel.options)
            )
            .filter(SurveyModel.id == survey_id)
            .first()
        )
        if not survey_model:
            return None

        questions = []
        for q in survey_model.questions:
            options = [
                Option(
                    id=o.id,
                    question_id=o.question_id,
                    text=o.text
                )
                for o in q.options
            ]
            questions.append(
                Question(
                    id=q.id,
                    survey_id=q.survey_id,
                    text=q.text,
                    question_type=QuestionType(q.question_type),
                    options=options,
                    required=q.required
                )
            )

        return Survey(
            id=survey_model.id,
            title=survey_model.title,
            description=survey_model.description,
            created_at=survey_model.created_at,
            status=SurveyStatus(survey_model.status),
            questions=questions
        )

    def list_all(self) -> List[Survey]:
        surveys = self.db.query(SurveyModel).all()
        return [
            Survey(
                id=s.id,
                title=s.title,
                description=s.description,
                created_at=s.created_at,
                status=SurveyStatus(s.status)
            )
            for s in surveys
        ]
