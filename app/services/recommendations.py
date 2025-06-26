from typing import List
from app.models.emotions import Emotion
# from app.services.ml_model import predict_recommendation

from app.services.ml_model import ml_model

RECOMMENDATION_TEXTS = {
    "respiracion": "Te recomendamos ejercicios de respiración para mejorar el ánimo.",
    "meditacion": "Prueba la meditación guiada para reducir la ansiedad.",
    "seguir_asi": "¡Sigue así! Mantén actividades que te generan felicidad.",
    "derivar": "Parece que necesitas apoyo adicional. Te recomendamos contactar a un profesional. ¿Quieres que te conectemos con uno?"
}

def generate_recommendations(emotions):
    moods = [e.mood.lower() for e in emotions[-5:]]
    pred = ml_model.predict(moods)
    return [RECOMMENDATION_TEXTS.get(pred, "Mantente atento a tus emociones y registra cómo te sientes cada día.")]

