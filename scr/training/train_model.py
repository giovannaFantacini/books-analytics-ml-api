import re
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
from features.extract_features import extract_features_for_rating_prediction


def find_column(columns, candidates):
    cols_lower = {c.lower(): c for c in columns}
    for name in candidates:
        if name.lower() in cols_lower:
            return cols_lower[name.lower()]
    return None

def to_numeric_price(series):
    s = series.astype(str).str.replace(r'[^\d,.-]', '', regex=True).str.replace(',', '.', regex=False)
    return pd.to_numeric(s, errors='coerce')

if __name__ == "__main__":
    df = pd.read_csv("data/books.csv")

    # Ajustar features para modelo
    features = extract_features_for_rating_prediction(df)
    X = features.drop(columns=["Avaliação"])
    y = features["Avaliação"]

    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    # pipeline
    numeric_features = ["Preço", "Disponibilidade"]
    categorical_features = ["Categoria"]

    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    clf = Pipeline(steps=[
        ('pre', preprocessor),
        ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y_enc, test_size=0.2, random_state=42, stratify=y_enc)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    print("Acurácia:", accuracy_score(y_test, y_pred))

    # salvar modelo e encoder de labels
    joblib.dump({"pipeline": clf, "label_encoder": le}, "models/modelo_avaliacao_books.joblib")
    print("Modelo salvo em models/modelo_avaliacao_books.joblib")