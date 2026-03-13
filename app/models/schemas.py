from pydantic import BaseModel

class LiteratureRequest(BaseModel):
    query: str
    num_papers: int = 20
    top_k: int = 5