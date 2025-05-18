import pandas as pd

def weighted_product(df, weights):
    # Normalisasi bobot
    total = sum(weights.values())
    normalized_weights = {k: v / total for k, v in weights.items()}

    # Hitung skor WP
    scores = []
    for _, row in df.iterrows():
        score = 1
        for kriteria in weights:
            score *= row[kriteria] ** normalized_weights[kriteria]
        scores.append(score)
    
    df['score'] = scores
    df_sorted = df.sort_values(by='score', ascending=False)
    return df_sorted
