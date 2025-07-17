from fastapi import FastAPI

from question.api.question_router import router as question_router
from question.api.option_router import router as option_router

app = FastAPI()

app.include_router(question_router)
app.include_router(option_router)
