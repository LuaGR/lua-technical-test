from pydantic import BaseModel

class OptionCreateRequest(BaseModel):
    text: str

class OptionResponse(BaseModel):
    id: int
    question_id: int
    text: str
