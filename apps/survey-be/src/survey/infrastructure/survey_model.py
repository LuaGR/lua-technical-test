from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class SurveyModel(Base):
    __tablename__ = "surveys"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)

    questions = relationship(
        "QuestionModel",
        back_populates="survey",
        cascade="all, delete-orphan"
    )
