import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_coaches():
    return pd.read_csv(DATA_DIR / "coaches.csv")