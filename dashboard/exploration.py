"""Deterministic descriptive calculations used only for dashboard exploration."""
import numpy as np
import pandas as pd

def descriptive_summary(frame, target="Crop_Yield_ton_per_hectare"):
    s = frame[target].dropna()
    return {"n": int(s.size), "mean": float(s.mean()) if len(s) else None, "median": float(s.median()) if len(s) else None, "sd": float(s.std()) if len(s) > 1 else None, "q1": float(s.quantile(.25)) if len(s) else None, "q3": float(s.quantile(.75)) if len(s) else None}

def safe_pearson(frame, x, y):
    pair = frame[[x, y]].dropna()
    if len(pair) < 3 or pair[x].nunique() < 2 or pair[y].nunique() < 2: return None
    return float(pair[x].corr(pair[y]))

def outlier_flags(frame, column):
    s = frame[column]
    q1, q3 = s.quantile(.25), s.quantile(.75)
    iqr = q3 - q1
    return (s < q1 - 1.5 * iqr) | (s > q3 + 1.5 * iqr)

def numeric_columns(frame):
    return frame.select_dtypes(include=np.number).columns.tolist()

