from groq import Groq
from sentence_transformers import SentenceTransformer
import numpy as np
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity

from app.utils.config import GROQ_API_KEY
from app.services.embedding_service import embed_texts

# Initialize models
model = SentenceTransformer("all-MiniLM-L6-v2")
client = Groq(api_key=GROQ_API_KEY)


# ---------------------------------------
# Build similarity graph between papers
# ---------------------------------------
def build_paper_graph(summaries):

    embeddings = embed_texts(summaries)

    similarity_matrix = cosine_similarity(embeddings)

    G = nx.Graph()

    # Add nodes
    for i in range(len(summaries)):
        G.add_node(i)

    threshold = 0.6

    # Add edges based on similarity
    for i in range(len(summaries)):
        for j in range(i + 1, len(summaries)):

            if similarity_matrix[i][j] > threshold:
                G.add_edge(i, j)

    return G


# ---------------------------------------
# Detect sparsely connected areas
# ---------------------------------------
def detect_sparse_areas(graph):

    components = list(nx.connected_components(graph))

    sparse_clusters = []

    for comp in components:

        # Small clusters indicate under-explored areas
        if len(comp) <= 2:
            sparse_clusters.append(list(comp))

    return sparse_clusters


# ---------------------------------------
# Main Gap Detection Agent
# ---------------------------------------
def detect_research_gaps(topic, summaries):

    if len(summaries) == 0:
        return "No research papers available to analyze research gaps."

    # Step 1 — Build citation/similarity graph
    graph = build_paper_graph(summaries)

    # Step 2 — Detect weakly connected clusters
    sparse_clusters = detect_sparse_areas(graph)

    gap_text = ""

    # Step 3 — Extract summaries from sparse clusters
    if len(sparse_clusters) > 0:

        for cluster in sparse_clusters:

            gap_text += "\nCluster of under-explored papers:\n"

            for index in cluster:
                gap_text += summaries[index] + "\n"

    else:
        gap_text = "\n".join(summaries[:5])

    # Step 4 — Ask LLM to explain gaps
    prompt = f"""
You are an academic research analyst.

Research Topic:
{topic}

The following paper summaries belong to sparsely connected areas in a citation similarity graph.
These areas often represent under-explored research intersections.

Paper Summaries:
{gap_text}

Identify the most important research gaps in this field.

For each gap provide:

1. Gap Title
2. Explanation of the Gap
3. Why this Gap Exists
4. Potential Research Direction

Generate 3-5 research gaps.

Format the output clearly.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    gaps = response.choices[0].message.content

    return {
    "gaps": gaps,
    "edges": list(graph.edges()),
    "nodes": list(graph.nodes())
    }