from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from survey.infrastructure.survey_model import Base

class OptionModel(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    text = Column(String, nullable=False)

    question = relationship("QuestionModel", back_populates="options")
