import time
import logging
import json
from fastapi import FastAPI, Request, HTTPException
from contextlib import asynccontextmanager
from typing import List

from app.config import settings
from app.services.es_client import es_wrapper
from app.models.api import HealthCheck
from app.models.es_types import DiagnosticResult, FixProposal, BenchmarkResult
from app.core.diagnostic import scanner
from app.core.fix_generator import fix_generator
from app.core.validator import validator
from app.core.benchmarker import benchmarker
from app.services.agent_flow import agent
from app.services.esre import esre

# Configure Logging (ECS Format Simulation)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("autofixer.agent")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await es_wrapper.connect()
    try:
        await esre.initialize_knowledge_base()
    except Exception:
        pass
    yield
    await es_wrapper.close()

app = FastAPI(
    title="Elastic Auto-Fixer Agent",
    version="1.0.0",
    lifespan=lifespan
)

# Middleware for Logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    log_entry = {
        "event.dataset": "autofixer.api",
        "http.request.method": request.method,
        "url.path": request.url.path,
        "http.response.status_code": response.status_code,
        "event.duration": process_time,
        "message": f"{request.method} {request.url.path} completed in {process_time:.2f}ms"
    }
    logger.info(json.dumps(log_entry))
    
    return response

# --- Routes ---

@app.get("/", response_model=HealthCheck)
async def health_check():
    client = await es_wrapper.get_client()
    try:
        info = await client.info()
        return {
            "status": "healthy",
            "es_version": info['version']['number'],
            "cluster_name": info['cluster_name']
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "error",
            "es_version": "unknown",
            "cluster_name": str(e)
        }

@app.get("/api/v1/diagnose", response_model=List[DiagnosticResult])
async def run_diagnostics():
    logger.info("Starting cluster diagnosis scan")
    return await scanner.scan_all()

@app.post("/api/v1/generate-fix", response_model=FixProposal)
async def generate_fix_endpoint(diagnostic: DiagnosticResult):
    logger.info(f"Generating fix for issue: {diagnostic.issue_id}")
    return await fix_generator.generate_fix(diagnostic)

@app.post("/api/v1/benchmark", response_model=BenchmarkResult)
async def benchmark_fix_endpoint(proposal: FixProposal):
    index = proposal.original_code.get("index", "logs-*")
    if "query" in proposal.fixed_code:
        return await benchmarker.compare(
            index=index,
            original_query={"query": proposal.original_code.get("query", {})},
            optimized_query={"query": proposal.fixed_code.get("query", {})}
        )
    return BenchmarkResult(
        latency_before_ms=0, latency_after_ms=0,
        cpu_before=0, cpu_after=0,
        improvement_percentage=0, is_safe=True
    )

@app.post("/api/v1/apply-fix")
async def apply_fix_endpoint(fix: FixProposal):
    logger.info(f"Applying fix for issue: {fix.issue_id}")
    if not await validator.validate_syntax(fix):
        raise HTTPException(status_code=400, detail="Invalid Elasticsearch syntax.")
    
    result = await validator.apply_fix(fix)
    
    if result["status"] == "error":
        logger.error(f"Fix application failed: {result['message']}")
        raise HTTPException(status_code=500, detail=result["message"])
        
    return result

@app.post("/api/v1/agent/run-cycle")
async def run_agent_cycle():
    logger.info("Triggering autonomous agent cycle")
    return await agent.run_autonomous_cycle()

@app.get("/api/v1/agent/history")
async def get_agent_history():
    return await agent.get_agent_history()