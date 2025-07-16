from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from survey.infrastructure.survey_model import Base

class QuestionModel(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("surveys.id"), nullable=False)
    text = Column(String, nullable=False)
    question_type = Column(String, nullable=False)
    required = Column(Boolean, default=False, nullable=False)

    survey = relationship("SurveyModel", back_populates="questions")
    options = relationship(
        "OptionModel",
        back_populates="question",
        cascade="all, delete-orphan"
    )
