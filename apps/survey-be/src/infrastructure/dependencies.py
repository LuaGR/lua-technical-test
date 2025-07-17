from sqlalchemy.orm import Session
from fastapi import Depends

from .db import get_db
from survey.infrastructure.survey_repository import SurveyRepository
from question.infrastructure.question_repository import QuestionRepository
from question.infrastructure.option_repository import OptionRepository

def get_survey_repository(db: Session = Depends(get_db)):
    return SurveyRepository(db)

def get_question_repository(db: Session = Depends(get_db)):
    return QuestionRepository(db)

def get_option_repository(db: Session = Depends(get_db)):
    return OptionRepository(db)
