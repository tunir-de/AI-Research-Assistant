from app.services.literature_service import generate_literature_review
from app.services.research_gap_service import detect_research_gaps
from app.services.proposal_service import generate_grant_proposal
from app.services.trend_analysis_service import analyze_research_trends
from app.services.methodology_service import generate_methodology
from app.services.novelty_plagiarism_service import analyze_novelty_plagiarism


def run_research_pipeline(topic, agency, duration, domain, top_k):
    """
    Master agent that orchestrates all agents
    """

    # Agent 1
    literature_result = generate_literature_review(topic, 30, top_k)

    literature_review = literature_result.get("literature_review", "")

    papers = literature_result.get("papers", [])[:top_k]

    # Extract summaries for gap detection
    summaries = [paper["summary"] for paper in papers]

    # Agent 2
    gap_result = detect_research_gaps(topic, summaries)

    gaps = gap_result["gaps"]
    edges = gap_result["edges"]
    nodes = gap_result["nodes"]

    # Agent 3
    proposal = generate_grant_proposal(topic, agency, duration, domain)

    # Agent 4 - Trend Analysis
    trends = analyze_research_trends(topic, summaries)

    # Agent 5 - Methodology Design
    #methodology = generate_methodology(
    #topic,
    #gaps,
    #trends
    #)

    # Agent 6 - Novelty & Plagiarism Estimation
    #summaries = [paper["summary"] for paper in papers]
    #novelty_result = analyze_novelty_plagiarism(
    #methodology,
    #summaries
    #)

    return {
    "literature_review": literature_review,
    "research_gaps": gaps,
    "graph_edges": edges,
    "graph_nodes": nodes,
    "proposal": proposal,
    "papers": papers,
    "trends": trends,
    #"methodology": methodology,
    #"novelty_score": novelty_result["novelty_score"],
    #"similarity_score": novelty_result["similarity_score"],
    #"plagiarism_risk": novelty_result["plagiarism_risk"],
    #"ethical_analysis": novelty_result["ethical_analysis"]
    }