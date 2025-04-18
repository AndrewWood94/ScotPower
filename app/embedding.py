from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(text):
    # Generate vector embedding
    embedding = model.encode(text)

    return embedding.tolist()