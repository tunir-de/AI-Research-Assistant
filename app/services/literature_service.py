import os
import numpy as np
from groq import Groq
from serpapi import GoogleSearch
from app.services.research_gap_service import detect_research_gaps
from app.services.arxiv_service import fetch_arxiv_papers

from app.utils.config import GROQ_API_KEY, SERP_API_KEY
from app.services.embedding_service import embed_texts
from app.services.vector_store import build_index, search_index


# Initialize Groq client
groq_client = Groq(api_key=GROQ_API_KEY)


import requests
from app.utils.config import SERP_API_KEY

def fetch_papers(query: str, num_papers: int = 10):

    url = "https://google.serper.dev/search"

    payload = {
        "q": query + " research paper",
        "num": num_papers
    }

    headers = {
        "X-API-KEY": SERP_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    papers = []

    if "organic" not in data:
        print("Serper response:", data)
        return papers

    for result in data["organic"][:num_papers]:

        papers.append({
            "title": result.get("title", ""),
            "summary": result.get("snippet", ""),
            "link": result.get("link", "")
        })

    return papers


def generate_literature_review(query: str, num_papers: int, top_k: int):
    """
    Full RAG pipeline for literature review generation.
    """

    # Step 1: Fetch papers
    papers = fetch_arxiv_papers(query, num_papers)

    if len(papers) == 0:
        return {
            "papers": [],
            "literature_review": "No papers found for the given query."
        }

    # Step 2: Extract summaries
    summaries = [paper["summary"] for paper in papers]

    # Step 3: Generate embeddings
    embeddings = embed_texts(summaries)

    # Step 4: Build FAISS index
    index = build_index(embeddings)

    # Step 5: Embed query
    query_embedding = embed_texts([query])

    # Step 6: Retrieve top-k relevant papers
    indices = search_index(index, np.array(query_embedding), top_k)

    top_papers = [papers[i] for i in indices]

    summaries = [paper["summary"] for paper in top_papers]

    research_gaps = detect_research_gaps(query, summaries)

    # Step 7: Combine summaries
    combined_text = ""

    for paper in top_papers:
        combined_text += paper["summary"] + "\n"

    # Step 8: Prompt for LLM
    prompt = f"""
You are an academic research assistant.

Write a structured literature review for the research topic:

{query}

Based on the following paper summaries:

{combined_text}

Structure the response as:

1. Introduction
2. Overview of Existing Research
3. Key Techniques and Approaches
4. Limitations of Current Work
5. Future Research Directions

Make the review clear, academic, and concise.
"""

    # Step 9: Generate review using Groq
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    review = response.choices[0].message.content

    return {
    "papers": top_papers,
    "literature_review": review,
    "research_gaps": research_gaps
}