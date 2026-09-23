import sys
from pathlib import Path
from pydantic import BaseModel, Field, field_validator
from fastapi import FastAPI, HTTPException, Header
import logging
import uuid
import time

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from graph.workflow import run_workflow

app = FastAPI(
    title="Aegis Multi-Agent AI Platform",
    version="1.0.0"
)

logger = logging.getLogger("aegis-api")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

API_KEY = "aegis-key"


class WorkflowRequest(BaseModel):
    request: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Natural-language request for the Aegis workflow"
    )

    @field_validator("request")
    @classmethod
    def validate_request(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Request cannot be empty or whitespace.")

        return value

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "aegis-api"
    }


@app.post("/workflow")
def execute_workflow(
    payload: WorkflowRequest,
    x_api_key: str = Header(...)
):
    request_id = str(uuid.uuid4())
    start_time = time.perf_counter()
    logger.info(f"Workflow execution started with request ID: {request_id}")
    if x_api_key != API_KEY:
        logger.warning(
            "Authentication failed | request_id=%s",
            request_id
        )
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key."
        )
    logger.info(
        "Workflow request received | request_id=%s",
        request_id
    )

    try:
        result = run_workflow(payload.request)
        duration_ms = round((time.perf_counter() - start_time) * 1000,2)
        
        logger.info(
        "Workflow completed | request_id=%s | duration_ms=%s",
        request_id,
        duration_ms
        )        

        return {
           "status": "success",
            "request_id": request_id,
            "duration_ms": duration_ms,
            "answer": result.get("response", ""),
            "execution_plan": result.get("execution_plan", []),
            "agents_used": result.get("execution_plan", [])
                }

    except Exception as exc:
        logger.exception(
            "Workflow failed | request_id=%s",
            request_id
        )
        raise HTTPException(            
            status_code=500,
            detail={
                "status": "error",
                "message": "Workflow execution failed.",
                "error_type": type(exc).__name__
            }
        )