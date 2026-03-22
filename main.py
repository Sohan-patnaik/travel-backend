import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator

from agents.travel_agent import get_agent_executor, run_agent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Warming up agent executor...")
    get_agent_executor()    
    logger.info("Agent executor ready.")
    yield
    logger.info("Shutting down.")

app = FastAPI(
    title="AI Travel Agent",
    version="1.0.0",
    description="Agentic travel planner — flights, trains, hotels, weather.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class Query(BaseModel):
    query: str

    @field_validator("query")
    @classmethod
    def query_must_not_be_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("query must not be empty.")
        if len(v) > 1000:
            raise ValueError("query must be at most 1000 characters.")
        return v


class AgentResponse(BaseModel):
    reply: str
    duration_ms: int

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    ms = int((time.perf_counter() - start) * 1000)
    logger.info("%s %s → %s (%d ms)", request.method, request.url.path, response.status_code, ms)
    return response


@app.get("/", tags=["health"])
async def health_check():
    return {"status": "ok", "service": "AI Travel Agent"}


@app.post("/agent", response_model=AgentResponse, tags=["agent"])
async def run_agent_endpoint(request: Query):
    logger.info("Received query: %s", request.query)
    start = time.perf_counter()

    reply = run_agent(request.query)

    duration_ms = int((time.perf_counter() - start) * 1000)
    logger.info("Query answered in %d ms", duration_ms)
    return AgentResponse(reply=reply, duration_ms=duration_ms)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception on %s", request.url.path)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error. Please try again later."},
    )