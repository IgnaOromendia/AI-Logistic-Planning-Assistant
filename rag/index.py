
from pathlib import Path
import json
import numpy as np
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "policies"
STORAGE = ROOT / "rag" / "storage"

MODEL_NAME = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)

def chunk_text(text, size=90, overlap=20):
    words = text.split()
    step = size - overlap

    return [
        " ".join(words[i:i + size])
        for i in range(0, len(words), step)
    ]


def build_index():
    chunks = []

    for file in sorted(DOCS.glob("*.md")):
        content = file.read_text(encoding="utf-8")

        for fragment in chunk_text(content):
            chunks.append({
                "source": file.name,
                "text": fragment
            })

    if not chunks:
        raise ValueError("No hay documentos para indexar")

    model = SentenceTransformer(MODEL_NAME)

    vectors = model.encode(
        [chunk["text"] for chunk in chunks],
        normalize_embeddings=True
    )

    STORAGE.mkdir(parents=True, exist_ok=True)

    np.save(STORAGE / "embeddings.npy", vectors)

    (STORAGE / "chunks.json").write_text(
        json.dumps(chunks, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"Indexados {len(chunks)} fragmentos")


if __name__ == "__main__":
    build_index()
