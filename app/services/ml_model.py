import pickle
from pathlib import Path
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import numpy as np

MODEL_PATH = Path("app/models/distilbert_emotion_model")
TOKENIZER_PATH = Path("app/models/distilbert_tokenizer")

class MLModel:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.emotion_labels = ["respiracion", "meditacion", "seguir_asi", "derivar"]  # Ajusta según tus categorías
        self.load_model()

    def load_model(self):
        """Carga el modelo DistilBERT y el tokenizador, o entrena uno inicial si no existe."""
        if MODEL_PATH.exists() and TOKENIZER_PATH.exists():
            self.model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
            self.tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH)
            self.model.to(self.device)
            self.model.eval()
        else:
            # Cargar modelo preentrenado en español
            model_name = "dccuchile/bert-base-spanish-wwm-uncased"
            self.model = AutoModelForSequenceClassification.from_pretrained(
                model_name, num_labels=len(self.emotion_labels)
            )
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)

            # Datos de entrenamiento de ejemplo (reemplaza con tu dataset real)
            X_train = [
                "Me siento muy triste y sin ganas de nada",
                "Estoy feliz y lleno de energía",
                "Todo me preocupa, no puedo relajarme",
                "Me siento bien, todo está tranquilo",
                "No sé cómo seguir, estoy muy ansioso",
                "Necesito ayuda, siento que no puedo más"
            ]
            y_train = ["respiracion", "seguir_asi", "meditacion", "seguir_asi", "meditacion", "derivar"]

            # Preparar datos para fine-tuning
            encodings = self.tokenizer(X_train, truncation=True, padding=True, return_tensors="pt")
            labels = torch.tensor([self.emotion_labels.index(label) for label in y_train])

            # Fine-tuning básico (idealmente usa un dataset más grande y Google Colab)
            from transformers import Trainer, TrainingArguments
            training_args = TrainingArguments(
                output_dir="./results",
                num_train_epochs=3,
                per_device_train_batch_size=8,
                save_steps=1000,
                save_total_limit=2,
            )
            trainer = Trainer(
                model=self.model,
                args=training_args,
                train_dataset=[{"input_ids": encodings["input_ids"][i], "attention_mask": encodings["attention_mask"][i], "labels": labels[i]} for i in range(len(X_train))]
            )
            trainer.train()

            # Guardar modelo y tokenizador
            self.model.save_pretrained(MODEL_PATH)
            self.tokenizer.save_pretrained(TOKENIZER_PATH)

    def predict(self, moods):
        """Predice la recomendación basada en una lista de estados de ánimo."""
        if not self.model or not self.tokenizer:
            raise Exception("Modelo no cargado")

        text = " ".join(moods)
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
        prediction_idx = torch.argmax(outputs.logits, dim=1).item()
        return self.emotion_labels[prediction_idx]

    def save_model(self):
        """Guarda el modelo y el tokenizador."""
        self.model.save_pretrained(MODEL_PATH)
        self.tokenizer.save_pretrained(TOKENIZER_PATH)

ml_model = MLModel()