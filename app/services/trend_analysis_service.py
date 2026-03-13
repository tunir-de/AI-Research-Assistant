from groq import Groq
from app.utils.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def analyze_research_trends(topic, summaries):

    if not summaries:
        return "No research trends could be identified."

    # Combine paper summaries
    combined_text = "\n".join(summaries[:10])

    prompt = f"""
You are an academic research analyst.

Research Topic:
{topic}

Below are summaries of recent research papers:

{combined_text}

Write ONE concise paragraph (4–5 sentences) describing the main research trends in this field.

The paragraph should:
- Highlight key methods used in recent papers
- Mention common techniques or models
- Discuss the direction of current research

Do NOT list bullet points.
Do NOT create headings.
Return only a clean paragraph suitable for a research report.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    trends = response.choices[0].message.content.strip()

    return trends