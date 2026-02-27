from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class DiagnosticResult(BaseModel):
    """Represents a found issue in the cluster."""
    issue_id: str
    severity: str = Field(..., pattern="^(critical|high|medium|low)$")
    category: str = Field(..., pattern="^(query|mapping|ilm|vector|script|autoscaling)$")
    description: str
    affected_resource: str # index name or pipeline id
    detected_at: str
    metrics: Dict[str, Any] # e.g., {"cpu_usage": "98%", "scan_size": "10GB"}

class FixProposal(BaseModel):
    """Represents the LLM-generated fix."""
    issue_id: str
    original_code: Dict[str, Any]
    fixed_code: Dict[str, Any]
    explanation: str
    estimated_impact: str # e.g. "50% latency reduction"

class BenchmarkResult(BaseModel):
    """Represents the validation test."""
    latency_before_ms: float
    latency_after_ms: float
    cpu_before: float
    cpu_after: float
    improvement_percentage: float
    is_safe: bool