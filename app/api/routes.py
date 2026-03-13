from fastapi import APIRouter
from app.models.schemas import LiteratureRequest
from app.services.literature_service import generate_literature_review
from app.services.proposal_service import generate_grant_proposal
from app.services.master_agent import run_research_pipeline

router = APIRouter()

@router.post("/generate-literature")

def generate_lit_review(request: LiteratureRequest):

    result = generate_literature_review(
        request.query,
        request.num_papers,
        request.top_k
    )

    return result

@router.post("/generate-proposal")

def proposal_generator(request: dict):

    proposal = generate_grant_proposal(
        request["topic"],
        request["agency"],
        request["duration"],
        request["domain"]
    )

    return {"proposal": proposal}

@router.post("/generate-full-report")
def generate_full_report(request: dict):

    result = run_research_pipeline(
        request["topic"],
        request["agency"],
        request["duration"],
        request["domain"],
        request["top_k"]   
    )

    return result