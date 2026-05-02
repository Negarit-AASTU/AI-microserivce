from sentence_transformers import SentenceTransformer
import numpy as np


model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text: str):
    return model.encode(text, convert_to_numpy=True)

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))