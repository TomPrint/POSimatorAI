import joblib
import pandas as pd
from pathlib import Path

# Ścieżka do nowego pickle
MODEL_PATH = Path(__file__).resolve().parent / "model_global.pkl"

# Wczytanie modelu
MODEL_DATA = joblib.load(MODEL_PATH)
MODEL = MODEL_DATA["model_global"]

def predict_price(data: dict) -> dict:
    """
    data = {
        'naklad_szt': int,
        'objetosc_m3': float,
        'konstrukcja_kg': float,
        'sklejka_m3': float,
        'drewno_m3': float,
        'plyta_m2': float,
        'druk_m2': float,
        'led_mb': float,
        'tworzywa_m2': float,
        'koszty_pozostale': float,
        'stopien_skomplikowania': int,
        'rodzaj_tworzywa': str,
        'rodzaj_displaya': str,
    }
    """

    df = pd.DataFrame([data])

    # Predykcja bez logarytmu
    pred = MODEL["pipeline"].predict(df)[0]

    # Zwracamy słownik z predykcją i wszystkimi dodatkowymi informacjami
    return {
        "predicted": round(float(pred), 2),
        "model_name": MODEL["name"],
        "mae": MODEL["mae"],
        "r2": MODEL["r2"],
        "model_type": MODEL["model_type"],
        "model_params": MODEL["model_params"]
    }
