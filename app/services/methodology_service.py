from groq import Groq
from app.utils.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def generate_methodology(topic, gaps, trends):

    prompt = f"""
You are an academic research assistant.

Generate a structured research methodology for the topic:

{topic}

Based on the identified research gaps and trends, design a research methodology.

Do NOT repeat the research gaps or trends in the output.

Follow IEEE/ACM academic format and include:

3. Proposed Methodology
3.1 System Architecture
3.2 Dataset Suggestions
3.3 Baseline Methods
3.4 Proposed Model / Approach
3.5 Evaluation Metrics

Guidelines:
- Suggest realistic public datasets.
- Suggest baseline models used in research.
- Suggest evaluation metrics.
- Align the methodology with the research gaps and trends.
- Write in academic research style.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    methodology = response.choices[0].message.content

    return methodology