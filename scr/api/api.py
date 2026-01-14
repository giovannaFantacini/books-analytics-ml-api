import logging
from pathlib import Path
from typing import Optional

from fastapi.security import OAuth2PasswordRequestForm
import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, Query, HTTPException, status, Depends
import datetime
from dotenv import load_dotenv

from scr.scripts import data_analysis
from scr.scraping import scraping
from scr.schema.PredictRequest import PredictRequest
from scr.features.extract_features import extract_features_for_rating_prediction
from sklearn.model_selection import train_test_split
from scr.auth.authentication import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES,
)


app = FastAPI(
    title="Tech Challenge Fiap",
    description="Esta é uma API contruida para o Tech Challenge da Fiap. Ela realiza web scraping no site 'Books to Scrape' para coletar informações sobre livros, como título, preço, avaliação, disponibilidade, categoria e imagem. Os dados coletados são armazenados em um arquivo CSV chamado 'books.csv'.",
    version="1.0.0"
)

BASE_DIR = Path(__file__).resolve().parents[2]   # api.py -> api -> scr -> MODULO1
MODEL_PATH = BASE_DIR / "models" / "modelo_avaliacao_books.joblib"
DATA_PATH = BASE_DIR / "data" / "books.csv"

model_bundle = joblib.load(MODEL_PATH)
pipeline = model_bundle["pipeline"]
label_encoder = model_bundle["label_encoder"]

books = pd.read_csv(DATA_PATH).to_dict(orient="records")

load_dotenv(Path(__file__).resolve().parents[2] / ".env")



@app.post("/api/v1/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    ok = authenticate_user(form_data.username, form_data.password)
    if not ok:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = datetime.timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": form_data.username},
        expires_delta=access_token_expires,
    )
    refresh_token = create_refresh_token(
        data={"sub": form_data.username},
        expires_delta=refresh_token_expires,
    )

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# @app.post("/api/v1/auth/refresh")
# async def refresh_token(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         if payload.get("type") != "refresh":
#             raise credentials_exception
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


books = pd.read_csv('data/books.csv').to_dict(orient='records')

@app.get("/api/v1/books")
async def get_books():
    return books


@app.get("/api/v1/books/search")
async def get_books_by_title_or_category(
        title: Optional[str] = Query(None),
        category: Optional[str] = Query(None)):

    filtered_books = books

    if title:
        filtered_books = [
            book for book in filtered_books
            if title.lower() in book["Título"].lower()
        ]

    if category:
        filtered_books = [
            book for book in filtered_books
            if category.lower() in book["Categoria"].lower()
        ]

    return filtered_books


@app.get("/api/v1/categories")
async def get_categories():
    return list({book["Categoria"] for book in books})


@app.get("/api/v1/health", status_code=status.HTTP_200_OK)
async def get_health():
    try:
        if not books:
            raise ValueError("Books list is empty")

        required_fields = {"Título", "Preço", "Categoria"}
        if not required_fields.issubset(books[0].keys()):
            raise ValueError("Invalid data structure")

        return {
            "status": "healthy",
            "books_loaded": len(books)
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )
    

@app.get("/api/v1/stats/overview")
async def get_stats_overview():
    return data_analysis.analise_dados(books)


@app.get("/api/v1/stats/categories/{category}")
async def get_stats_by_category(category: str = None):
    return data_analysis.analise_dados(books, categoria=category)


@app.get("/api/v1/books/top-rated")
async def get_top_rated_books(limit: int = 5):
    sorted_books = sorted(
        books,
        key=lambda x: ["Zero", "One", "Two", "Three", "Four", "Five"].index(x["Avaliação"]),
        reverse=True
    )
    return sorted_books[:int(limit)]


@app.get("/api/v1/books/price-range")
async def get_stats_by_category(
    min: float = 0,
    max: float = 100000
):
    filtered_books = [
        book for book in books
        if min <= float(book["Preço"][1:]) <= max
    ]

    return filtered_books

@app.get("/api/v1/books/{item_id}")
async def get_books_by_id(item_id: int):
    return books[item_id]

@app.post("/api/v1/scraping/trigger")
async def trigger_scraping():
    return {"message": scraping.scrape_books()}

@app.get("/api/v1/ml/features")
async def get_features():
    return extract_features_for_rating_prediction(pd.DataFrame(books)).to_dict(orient='records')

@app.get("/api/v1/ml/training-data")
async def get_training_data():
    features = extract_features_for_rating_prediction(pd.DataFrame(books))
    train, test = train_test_split(features, test_size=0.2, random_state=42)
    return {
        "train": train.to_dict(orient='records'),
        "test": test.to_dict(orient='records')
    }

predictions_cache = {}

@app.post("/api/v1/ml/predict")
def predict(payload: PredictRequest):

    """
    Expects JSON:
    {
        "preco": 25.99,
        "disponibilidade": 1,
        "categoria": "Science"
    }
    """

    preco = float(payload.preco)
    disponibilidade = int(payload.disponibilidade)
    categoria = str(payload.categoria)

    input_key = (preco, disponibilidade, categoria)

    if input_key in predictions_cache:
        predicted_rating = predictions_cache[input_key]
        return {"predicted_rating": predicted_rating}

    input_df = pd.DataFrame([{
        "Preço": preco,
        "Disponibilidade": disponibilidade,
        "Categoria": categoria
    }])

    y_pred_enc = pipeline.predict(input_df)[0]
    predicted_rating = label_encoder.inverse_transform([y_pred_enc])[0]

    predictions_cache[input_key] = predicted_rating

    return {"predicted_rating": str(predicted_rating)}