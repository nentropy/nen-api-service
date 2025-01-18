import os
import uvicorn
from fastapi import FastAPI
from app.routes import llm_router, agent_network
from app.routes.llm import llm_router
from app.routes.agent_network import 

app = FastAPI(
    title="Advanced LLM and Agent Network API",
    version="1.0.0",
    description="API for managing LangChain, Portkey, Redis, and GCP agents"
)

# Include routes
app.include_router(llm_router, prefix="/api/v1/llm", tags=["LLM"])
app.include_router(agent_network.router, prefix="/api/v1/agent", tags=["Agent Network"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
