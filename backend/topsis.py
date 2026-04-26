import numpy as np
import pandas as pd

def calculate_topsis(data, criteria_cols, weights, benefit_flags):
    """
    data          : list of dicts or DataFrame
    criteria_cols : list of column names
    weights       : list of floats (sum should be 1.0)
    benefit_flags : list of bool (True = benefit, False = cost)
    """
    if isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        df = data.copy()

    X = df[criteria_cols].values.astype(float)

    # Step 1: Normalisasi
    # Gunakan small epsilon untuk menghindari pembagian dengan nol
    norm = np.sqrt((X ** 2).sum(axis=0))
    norm[norm == 0] = 1e-9
    R = X / norm

    # Step 2: Bobot
    W = np.array(weights)
    V = R * W

    # Step 3: Solusi ideal
    A_pos = np.where(benefit_flags, V.max(axis=0), V.min(axis=0))
    A_neg = np.where(benefit_flags, V.min(axis=0), V.max(axis=0))

    # Step 4: Jarak
    D_pos = np.sqrt(((V - A_pos) ** 2).sum(axis=1))
    D_neg = np.sqrt(((V - A_neg) ** 2).sum(axis=1))

    # Step 5: Nilai preferensi
    # Jika D_pos + D_neg = 0, berikan 0
    C = np.divide(D_neg, (D_pos + D_neg), out=np.zeros_like(D_neg), where=(D_pos + D_neg)!=0)

    df["topsis_score"] = C
    df["rank"] = df["topsis_score"].rank(ascending=False).astype(int)
    
    return df.sort_values("rank")
