import pandas as pd
import joblib
import numpy as np
from pathlib import Path
from datetime import datetime

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# =========================
# KONFIGURACJA
# =========================
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "pos_estimations.csv"
MODEL_DIR = Path(__file__).resolve().parent

# =========================
# 1. WCZYTANIE DANYCH
# =========================
df = pd.read_csv(
    DATA_PATH,
    sep=";",
    encoding="utf-8-sig",
    dtype=str
)

df = df.apply(
    lambda col: col.map(
        lambda x: x.strip().replace("\xa0", "") if isinstance(x, str) else x
    )
)

# =========================
# 2. KOLUMNY NUMERYCZNE
# =========================
numeric_features = [
    "naklad_szt",
    "objetosc_m3",
    "konstrukcja_kg",
    "sklejka_m3",
    "drewno_m3",
    "plyta_m2",
    "druk_m2",
    "led_mb",
    "tworzywa_m2",
    "koszty_pozostale",
    "stopien_skomplikowania",
    "cena"
]

for col in numeric_features:
    df[col] = pd.to_numeric(
        df[col].str.replace(",", ".", regex=False),
        errors="coerce"
    )

df[numeric_features] = df[numeric_features].fillna(
    df[numeric_features].mean()
)

# =========================
# 3. KOLUMNY KATEGORYCZNE
# =========================
categorical_features = [
    "rodzaj_tworzywa",
    "rodzaj_displaya"
]

df[categorical_features] = df[categorical_features].fillna("Unknown")

# =========================
# 4. FUNKCJA TRENUJĄCA MODEL (bez log)
# =========================
def train_model(df_train):
    # Target wprost, bez log
    y = df_train["cena"]
    X = df_train.drop(columns=["cena"])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", "passthrough", numeric_features[:-1]),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ]
    )

    # Parametry modelu
    rf_params = dict(
        n_estimators=600,
        max_depth=10,
        min_samples_leaf=3,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1
    )

    model = RandomForestRegressor(**rf_params)

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    mae_test = mean_absolute_error(y_test, y_pred)
    r2_test = r2_score(y_test, y_pred)

    mae_cv = -cross_val_score(
        pipeline,
        X,
        y,
        scoring="neg_mean_absolute_error",
        cv=5,
        n_jobs=-1
    )

    # Dodajemy datę do nazwy modelu
    model_name = f"MODEL_GLOBAL_{datetime.now().strftime('%Y%m%d')}"

    print(f"\n📊 WYNIKI – {model_name}")
    print("MAE test:", round(mae_test, 2))
    print("R2 test:", round(r2_test, 3))
    print("MAE CV mean:", round(mae_cv.mean(), 2))
    print("MAE CV std:", round(mae_cv.std(), 2))

    return {
        "name": model_name,
        "pipeline": pipeline,
        "mae": round(mae_test, 2),
        "r2": round(r2_test, 3),
        "model_type": type(model).__name__,
        "model_params": rf_params
    }

# =========================
# 5. TRENING MODELU
# =========================
model_global = train_model(df)

# =========================
# 6. ZAPIS MODELU
# =========================
joblib.dump(
    {"model_global": model_global},
    MODEL_DIR / "model_global.pkl"
)

print("\n✅ Model zapisany: model_global.pkl")
