from typing import Optional, List
from sqlalchemy.orm import Session

from ..domain.survey_entity import Survey
from ..domain.survey_enums import SurveyStatus
from .survey_model import SurveyModel

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
        survey_model = self.db.query(SurveyModel).filter(SurveyModel.id == survey_id).first()
        if not survey_model:
            return None
        return Survey(
            id=survey_model.id,
            title=survey_model.title,
            description=survey_model.description,
            created_at=survey_model.created_at,
            status=SurveyStatus(survey_model.status)
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
