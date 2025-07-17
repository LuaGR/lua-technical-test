from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel

from ..application.add_question import AddQuestionUseCase
from ..domain.question_enums import QuestionType
from infrastructure.dependencies import get_question_repository, get_survey_repository

router = APIRouter(
    prefix="/surveys/{survey_id}/questions",
    tags=["questions"],
)

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

@router.post(
    "/",
    response_model=QuestionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a question to a survey"
)
def add_question(
    survey_id: int,
    body: QuestionCreateRequest,
    question_repository = Depends(get_question_repository),
    survey_repository = Depends(get_survey_repository)
):
    use_case = AddQuestionUseCase(question_repository)
    try:
        question = use_case.execute(
            survey_id=survey_id,
            text=body.text,
            question_type=body.question_type,
            required=body.required,
            survey_repository=survey_repository
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return QuestionResponse(
        id=question.id,
        survey_id=question.survey_id,
        text=question.text,
        question_type=question.question_type,
        required=question.required
    )
