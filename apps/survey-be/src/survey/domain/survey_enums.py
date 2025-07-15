from enum import Enum

class SurveyStatus(Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    CLOSED = "closed"

class QuestionType(Enum):
    TEXT = "text"
    SINGLE_CHOICE = "single_choice"
    MULTIPLE_CHOICE = "multiple_choice"
