import pickle
from pathlib import Path
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier

MODEL_PATH = Path("app/models/recommendation_model.pkl")
VECTORIZER_PATH = Path("app/models/vectorizer.pkl")

class MLModel:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.load_model()

    def load_model(self):
        if MODEL_PATH.exists() and VECTORIZER_PATH.exists():
            with open(MODEL_PATH, "rb") as f:
                self.model = pickle.load(f)
            with open(VECTORIZER_PATH, "rb") as f:
                self.vectorizer = pickle.load(f)
        else:
            # Entrenamiento inicial básico (igual que antes)
            from sklearn.feature_extraction.text import CountVectorizer
            from sklearn.ensemble import RandomForestClassifier

            X_train = [
                "triste ansioso",
                "feliz tranquilo",
                "ansioso preocupado",
                "feliz contento",
                "triste deprimido",
            ]
            y_train = [
                "respiracion",
                "seguir_así",
                "meditación",
                "seguir_así",
                "respiracion",
            ]

            self.vectorizer = CountVectorizer()
            X_train_vec = self.vectorizer.fit_transform(X_train)
            self.model = RandomForestClassifier()
            self.model.fit(X_train_vec, y_train)

            self.save_model()

    def save_model(self):
        with open(MODEL_PATH, "wb") as f:
            pickle.dump(self.model, f)
        with open(VECTORIZER_PATH, "wb") as f:
            pickle.dump(self.vectorizer, f)

    def predict(self, moods):
        if not self.model or not self.vectorizer:
            raise Exception("Modelo no cargado")

        text = " ".join(moods)
        x_vec = self.vectorizer.transform([text])
        prediction = self.model.predict(x_vec)[0]
        return prediction

ml_model = MLModel()
