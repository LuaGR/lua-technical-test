from typing import Optional
from survey.domain.survey_entity import Survey
from survey.infrastructure.survey_repository import SurveyRepository

class GetSurveyByIdUseCase:
    def __init__(self, repository: SurveyRepository):
        self.repository = repository

    def execute(self, survey_id: int) -> Optional[Survey]:
        return self.repository.get_by_id(survey_id)
