from typing import List
from survey.domain.survey_entity import Survey
from survey.infrastructure.survey_repository import SurveyRepository

class ListSurveysUseCase:
    def __init__(self, repository: SurveyRepository):
        self.repository = repository

    def execute(self) -> List[Survey]:
        return self.repository.list_surveys()
