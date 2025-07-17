from fastapi import APIRouter, HTTPException, status, Depends

from ..application.add_option import AddOptionUseCase
from infrastructure.dependencies import get_option_repository, get_question_repository
from .option_schema import OptionCreateRequest, OptionResponse

router = APIRouter(
    prefix="/questions/{question_id}/options",
    tags=["options"],
)

@router.post(
    "/",
    response_model=OptionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add an option to a question"
)
def add_option(
    question_id: int,
    body: OptionCreateRequest,
    option_repository = Depends(get_option_repository),
    question_repository = Depends(get_question_repository)
):
    use_case = AddOptionUseCase(option_repository, question_repository)
    try:
        option = use_case.execute(
            question_id=question_id,
            text=body.text
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return OptionResponse(
        id=option.id,
        question_id=option.question_id,
        text=option.text
    )
