from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter(
    prefix="/surveys",
    tags=["surveys"],
)

@router.post("/", summary="Crear una nueva encuesta")
def create_survey():
    return {"message": "Endpoint para crear encuesta"}

@router.get("/", summary="Listar encuestas")
def list_surveys():
    return {"message": "Endpoint para listar encuestas"}
