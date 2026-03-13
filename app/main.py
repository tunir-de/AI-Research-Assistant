from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="AI Research Assistant",
    description="Literature Review Generator",
    version="1.0"
)

app.include_router(router)