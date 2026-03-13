import os
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def load_templates():

    template_folder = "app/data/proposal_templates"

    templates = []
    texts = []

    for file in os.listdir(template_folder):

        path = os.path.join(template_folder, file)

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        templates.append({
            "name": file,
            "content": text
        })

        texts.append(text)

    return templates, texts


def build_template_index():

    templates, texts = load_templates()

    embeddings = model.encode(texts)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings).astype("float32"))

    return index, templates


def retrieve_template(query):

    index, templates = build_template_index()

    query_embedding = model.encode([query])

    D, I = index.search(np.array(query_embedding).astype("float32"), 1)

    return templates[I[0][0]]