import pandas as pd
from sklearn.cluster import KMeans
import joblib

from db_config import load_laptop_data

def train_kmeans():
    df = load_laptop_data()
    fitur = df[['harga', 'ram', 'prosesor', 'penyimpanan']]
    kmeans = KMeans(n_clusters=3, random_state=42)
    kmeans.fit(fitur)
    df['cluster'] = kmeans.labels_
    joblib.dump(kmeans, 'model_cluster.pkl')
    return df

if __name__ == "__main__":
    df_clustered = train_kmeans()
    print(df_clustered.head())
