from pydantic import BaseModel

from ..domain.question_enums import QuestionType

class QuestionCreateRequest(BaseModel):
    text: str
    question_type: QuestionType
    required: bool = False

class QuestionResponse(BaseModel):
    id: int
    survey_id: int
    text: str
    question_type: QuestionType
    required: bool
