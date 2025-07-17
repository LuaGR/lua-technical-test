from typing import Optional, List
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

    def get_by_id(self, option_id: int) -> Optional[Option]:
        option_model = self.db.query(OptionModel).filter(OptionModel.id == option_id).first()
        if not option_model:
            return None
        return Option(
            id=option_model.id,
            question_id=option_model.question_id,
            text=option_model.text
        )

    def list_by_question(self, question_id: int) -> List[Option]:
        option_models = self.db.query(OptionModel).filter(OptionModel.question_id == question_id).all()
        return [
            Option(
                id=o.id,
                question_id=o.question_id,
                text=o.text
            )
            for o in option_models
        ]
