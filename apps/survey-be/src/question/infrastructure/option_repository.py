from sqlalchemy.orm import Session

from ..domain.option_entity import Option
from .option_model import OptionModel

class OptionRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create(self, option: Option) -> Option:
        option_model = OptionModel(
            question_id=option.question_id,
            text=option.text
        )
        self.db.add(option_model)
        self.db.commit()
        self.db.refresh(option_model)
        return Option(
            id=option_model.id,
            question_id=option_model.question_id,
            text=option_model.text
        )
