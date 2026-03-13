import numpy as np
from groq import Groq

from app.services.embedding_service import embed_texts
from app.utils.config import GROQ_API_KEY


# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


def analyze_novelty_plagiarism(topic, summaries):
    """
    Combined Research Novelty, Plagiarism Risk,
    and Ethical AI Analysis Agent.
    """

    # If no papers found
    if len(summaries) == 0:
        return {
            "similarity_score": 0.0,
            "novelty_score": 1.0,
            "plagiarism_risk": "Low",
            "ethical_analysis": "No ethical risks detected due to lack of comparable research."
        }

    # ---------------------------------
    # STEP 1: Generate Embeddings
    # ---------------------------------

    topic_embedding = embed_texts([topic])[0]

    paper_embeddings = embed_texts(summaries)

    similarities = []

    # ---------------------------------
    # STEP 2: Compute Cosine Similarity
    # ---------------------------------

    for emb in paper_embeddings:

        similarity = np.dot(topic_embedding, emb) / (
            np.linalg.norm(topic_embedding) * np.linalg.norm(emb)
        )

        similarities.append(similarity)

    avg_similarity = sum(similarities) / len(similarities)

    novelty_score = 1 - avg_similarity

    # ---------------------------------
    # STEP 3: Determine Plagiarism Risk
    # ---------------------------------

    if avg_similarity > 0.85:
        risk = "High"

    elif avg_similarity > 0.65:
        risk = "Moderate"

    else:
        risk = "Low"

    # ---------------------------------
    # STEP 4: Ethical AI Analysis
    # ---------------------------------

    summaries_text = "\n".join(summaries[:5])

    prompt = f"""
You are an AI ethics and research integrity expert.

Research Topic:
{topic}

Related Research Summaries:
{summaries_text}

Evaluate the ethical implications of this research topic.

Provide the following:

1. Ethical Concerns
2. Potential Misuse Risks
3. Responsible AI Recommendations

Keep the explanation concise and suitable for an academic report.
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        ethical_analysis = response.choices[0].message.content

    except Exception:

        ethical_analysis = "Ethical analysis could not be generated due to API limitations."

    # ---------------------------------
    # STEP 5: Return Final Evaluation
    # ---------------------------------

    return {
        "similarity_score": float(round(avg_similarity, 3)),
        "novelty_score": float(round(novelty_score, 3)),
        "plagiarism_risk": risk,
        "ethical_analysis": ethical_analysis
    }