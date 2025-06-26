from fastapi import APIRouter, Depends, HTTPException, status
from app.services.ml_model import ml_model
from pydantic import BaseModel
from typing import List

router = APIRouter()

# Modelo para recibir nuevos datos
class TrainData(BaseModel):
    X: List[str]  # Lista de textos con estados emocionales
    y: List[str]  # Lista de etiquetas recomendación

@router.post("/retrain")
async def retrain_model(data: TrainData):
    if len(data.X) != len(data.y):
        raise HTTPException(status_code=400, detail="X e y deben tener la misma longitud")

    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.ensemble import RandomForestClassifier

    vectorizer = CountVectorizer()
    X_vec = vectorizer.fit_transform(data.X)

    model = RandomForestClassifier()
    model.fit(X_vec, data.y)

    ml_model.model = model
    ml_model.vectorizer = vectorizer
    ml_model.save_model()

    return {"message": "Modelo reentrenado y guardado correctamente"}
