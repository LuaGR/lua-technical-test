from datetime import datetime, timezone
from typing import Optional

from ..domain.survey_entity import Survey
from ..domain.survey_enums import SurveyStatus
from ..infrastructure.survey_repository import SurveyRepository


class CreateSurveyUseCase:
    def __init__(self, repository: SurveyRepository):
        self.repository = repository

    def execute(self, title: str, description: Optional[str] = None) -> Survey:
        survey = Survey(
            id=None,
            title=title,
            description=description or "",
            created_at=datetime.now(timezone.utc),
            status=SurveyStatus.DRAFT
        )
        return self.repository.create(survey)
