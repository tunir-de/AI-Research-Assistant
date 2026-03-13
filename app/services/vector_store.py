import faiss
import numpy as np

def build_index(embeddings):

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings).astype("float32"))

    return index


def search_index(index, query_embedding, k):

    D, I = index.search(query_embedding.astype("float32"), k)

    return I[0]