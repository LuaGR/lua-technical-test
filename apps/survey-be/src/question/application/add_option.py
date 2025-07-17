from ..domain.option_entity import Option
from ..infrastructure.option_repository import OptionRepository
from ..infrastructure.question_repository import QuestionRepository
from ..domain.question_enums import QuestionType

class AddOptionUseCase:
    def __init__(self, option_repository: OptionRepository, question_repository: QuestionRepository):
        self.option_repository = option_repository
        self.question_repository = question_repository

    def execute(self, question_id: int, text: str) -> Option:
        question = self.question_repository.get_by_id(question_id)
        if not question:
            raise ValueError("Question does not exist.")

        if question.question_type not in [QuestionType.SINGLE_CHOICE, QuestionType.MULTIPLE_CHOICE]:
            raise ValueError("Options can only be added to single_choice or multiple_choice questions.")

        if not text or not text.strip():
            raise ValueError("Option text cannot be empty.")

        option = Option(
            id=None,
            question_id=question_id,
            text=text.strip()
        )
        created_option = self.option_repository.create(option)
        return created_option
