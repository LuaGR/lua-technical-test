from typing import List, Optional

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session


from survey.application.create_survey import CreateSurveyUseCase
from survey.application.list_surveys import ListSurveysUseCase
from infrastructure.dependencies import get_survey_repository
from survey.application.get_survey_by_id import GetSurveyByIdUseCase
from question.domain.question_enums import QuestionType

router = APIRouter(
    prefix="/surveys",
    tags=["surveys"],
)

class SurveyCreateRequest(BaseModel):
    title: str
    description: Optional[str] = ""

class SurveyResponse(BaseModel):
    id: int
    title: str
    description: str
    created_at: str
    status: str

@router.post(
    "/",
    response_model=SurveyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new survey"
)
def create_survey(
    body: SurveyCreateRequest,
    survey_repository = Depends(get_survey_repository)
):
    use_case = CreateSurveyUseCase(survey_repository)
    try:
        survey = use_case.execute(
            title=body.title,
            description=body.description
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return SurveyResponse(
        id=survey.id,
        title=survey.title,
        description=survey.description,
        created_at=survey.created_at.isoformat(),
        status=survey.status.value
    )

@router.get(
    "/",
    response_model=List[SurveyResponse],
    summary="List all surveys"
)
def list_surveys(
    survey_repository = Depends(get_survey_repository)
):
    use_case = ListSurveysUseCase(survey_repository)
    surveys = use_case.execute()
    return [
        SurveyResponse(
            id=s.id,
            title=s.title,
            description=s.description,
            created_at=s.created_at.isoformat(),
            status=s.status.value
        )
        for s in surveys
    ]

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

@router.get(
    "/{survey_id}",
    response_model=SurveyDetailResponse,
    summary="Get survey details with questions and options"
)
def get_survey_detail(
    survey_id: int,
    survey_repository = Depends(get_survey_repository)
):
    use_case = GetSurveyByIdUseCase(survey_repository)
    survey = use_case.execute(survey_id)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")

    return SurveyDetailResponse(
        id=survey.id,
        title=survey.title,
        description=survey.description,
        created_at=survey.created_at.isoformat(),
        status=survey.status.value,
        questions=[
            QuestionNestedResponse(
                id=q.id,
                survey_id=q.survey_id,
                text=q.text,
                question_type=q.question_type,
                required=q.required,
                options=[
                    OptionNestedResponse(
                        id=o.id,
                        question_id=o.question_id,
                        text=o.text
                    ) for o in (q.options or [])
                ]
            ) for q in (survey.questions or [])
        ]
    )
