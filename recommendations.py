import pickle
import numpy as np
import streamlit as st


@st.cache_resource
def load_data():
    cfg_path = "data_for_recommendations/best_knn_hybrid_config.pkl"
    with open(cfg_path, "rb") as f:
        config = pickle.load(f)

    ae_embeddings_np = np.load("data_for_recommendations/ae_hybrid_embeddings.npy")
    siam_embeddings_np = np.load("data_for_recommendations/hybrid_embeddings.npy")

    with open("data_for_recommendations/id_to_pos.pkl", "rb") as f:
        id_to_pos = pickle.load(f)

    with open("data_for_recommendations/pos_to_id.pkl", "rb") as f:
        pos_to_id = pickle.load(f)

    return config, ae_embeddings_np, siam_embeddings_np, id_to_pos, pos_to_id


def user_recommendation(likes, config, ae_embeddings_np, id_to_pos, pos_to_id):
    from sklearn.neighbors import NearestNeighbors

    knn = NearestNeighbors(
        n_neighbors=50,
        metric=config.get("metric", "cosine"),
        algorithm=config.get("algorithm", "auto")
    )

    knn.fit(ae_embeddings_np)

    favorite_poses = [
        id_to_pos[track_id]
        for track_id in likes
        if track_id in id_to_pos
    ]

    if not favorite_poses:
        return []

    favorite_vectors = ae_embeddings_np[favorite_poses]
    user_emb = favorite_vectors.mean(axis=0).reshape(1, -1)

    _, idx = knn.kneighbors(user_emb, n_neighbors=50)

    return [pos_to_id[i] for i in idx[0]]


def track_recommendation(track_id, config, siam_embeddings_np, id_to_pos, pos_to_id):
    from sklearn.neighbors import NearestNeighbors

    if track_id not in id_to_pos:
        return []

    knn = NearestNeighbors(
        n_neighbors=50,
        metric=config.get("metric", "cosine"),
        algorithm=config.get("algorithm", "auto")
    )

    knn.fit(siam_embeddings_np)

    track_pos = id_to_pos[track_id]
    track_emb = siam_embeddings_np[track_pos].reshape(1, -1)

    _, idx = knn.kneighbors(track_emb, n_neighbors=50)

    return [pos_to_id[i] for i in idx[0]]


# загружаем один раз
config, ae_embeddings_np, siam_embeddings_np, id_to_pos, pos_to_id = load_data()