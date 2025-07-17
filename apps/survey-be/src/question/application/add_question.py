from typing import Optional
from ..domain.question_entity import Question
from ..domain.question_enums import QuestionType
from ..infrastructure.question_repository import QuestionRepository

class AddQuestionUseCase:
    def __init__(self, repository: QuestionRepository):
        self.repository = repository

    def execute(
        self,
        survey_id: int,
        text: str,
        question_type: QuestionType,
        required: bool = False,
        survey_repository=None
    ) -> Question:
        if survey_repository is not None and not survey_repository.get_by_id(survey_id):
            raise ValueError("Survey does not exist.")

        if question_type not in QuestionType:
            raise ValueError("Invalid question type.")

        if not text or not text.strip():
            raise ValueError("Question text cannot be empty.")

        question = Question(
            id=None,
            survey_id=survey_id,
            text=text,
            question_type=question_type,
            required=required
        )
        created_question = self.repository.create(question)
        return created_question
