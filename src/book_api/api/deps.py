from functools import lru_cache
import pandas as pd

from src.book_api.api.core.settings import load_books, load_model_bundle
from src.features.extract_features import extract_features_for_rating_prediction

@lru_cache(maxsize=1)
def get_books_cached():
    return load_books()

@lru_cache(maxsize=1)
def get_model_cached():
    pipeline, label_encoder = load_model_bundle()
    return pipeline, label_encoder

def get_features_df():
    books = get_books_cached()
    return extract_features_for_rating_prediction(pd.DataFrame(books))
