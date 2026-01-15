import pandas as pd
from fastapi import APIRouter
from sklearn.model_selection import train_test_split

from src.api.deps import get_books_cached, get_model_cached, get_features_df
from src.schema.PredictRequest import PredictRequest

router = APIRouter(prefix="/api/v1/ml", tags=["ML"])

predictions_cache = {}

@router.get("/features")
async def get_features():
    features = get_features_df()
    return features.to_dict(orient="records")

@router.get("/training-data")
async def get_training_data():
    features = get_features_df()
    train, test = train_test_split(features, test_size=0.2, random_state=42)
    return {"train": train.to_dict(orient="records"), "test": test.to_dict(orient="records")}

@router.post("/predict")
def predict(payload: PredictRequest):
    """
    Expects JSON:
    {
        "preco": 25.99,
        "disponibilidade": 1,
        "categoria": "Science"
    }
    """
    pipeline, label_encoder = get_model_cached()

    preco = float(payload.preco)
    disponibilidade = int(payload.disponibilidade)
    categoria = str(payload.categoria)

    key = (preco, disponibilidade, categoria)
    if key in predictions_cache:
        return {"predicted_rating": predictions_cache[key]}

    input_df = pd.DataFrame([{
        "Preço": preco,
        "Disponibilidade": disponibilidade,
        "Categoria": categoria
    }])

    y_pred_enc = pipeline.predict(input_df)[0]
    predicted_rating = label_encoder.inverse_transform([y_pred_enc])[0]

    predictions_cache[key] = str(predicted_rating)
    return {"predicted_rating": str(predicted_rating)}
