
import json
import numpy as np
from sentence_transformers import SentenceTransformer

from rag.index import STORAGE, MODEL_NAME


def search(query: str, top_k: int = 3):
    model = SentenceTransformer(MODEL_NAME)

    embeddings = np.load(
        STORAGE / "embeddings.npy"
    )

    chunks = json.loads(
        (STORAGE / "chunks.json").read_text(
            encoding="utf-8"
        )
    )

    query_vector = model.encode(
        query,
        normalize_embeddings=True
    )

    # Producto escalar de vectores normalizados
    # equivale a similitud coseno.
    scores = embeddings @ query_vector

    best_indices = np.argsort(scores)[::-1][:top_k]

    return [
        {
            **chunks[int(i)],
            "score": float(scores[i])
        }
        for i in best_indices
    ]


if __name__ == "__main__":
    question = "¿Qué pasa si el cliente no está en casa?"

    for result in search(question):
        print(result)
