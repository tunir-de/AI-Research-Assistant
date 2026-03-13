from groq import Groq
from app.utils.config import GROQ_API_KEY
from app.services.template_retriever import retrieve_template

client = Groq(api_key=GROQ_API_KEY)


def generate_grant_proposal(topic, agency, duration, domain):

    template = retrieve_template(agency)

    template_text = template["content"]

    prompt = f"""
You are an expert grant proposal writer.

Research Topic:
{topic}

Funding Agency:
{agency}

Domain:
{domain}

Project Duration:
{duration}

Follow this proposal structure:

{template_text}

Generate a professional academic research grant proposal.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content