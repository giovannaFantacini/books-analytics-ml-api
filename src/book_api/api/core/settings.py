from pathlib import Path
from dotenv import load_dotenv
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[4] 
MODEL_PATH = BASE_DIR / "models" / "modelo_avaliacao_books.joblib"
DATA_PATH = BASE_DIR / "data" / "books.csv"


def load_model_bundle():
    model_bundle = joblib.load(MODEL_PATH)
    pipeline = model_bundle["pipeline"]
    label_encoder = model_bundle["label_encoder"]
    return pipeline, label_encoder

def load_books():
    return pd.read_csv(DATA_PATH).to_dict(orient="records")
