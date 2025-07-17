from pydantic import BaseModel
from typing import List
from question.domain.question_enums import QuestionType

class SurveyCreateRequest(BaseModel):
    title: str
    description: str = ""

class SurveyResponse(BaseModel):
    id: int
    title: str
    description: str
    created_at: str
    status: str

class OptionNestedResponse(BaseModel):
    id: int
    question_id: int
    text: str

class QuestionNestedResponse(BaseModel):
    id: int
    survey_id: int
    text: str
    question_type: QuestionType
    required: bool
    options: List[OptionNestedResponse]

class SurveyDetailResponse(BaseModel):
    id: int
    title: str
    description: str
    created_at: str
    status: str
    questions: List[QuestionNestedResponse]
