import time
from typing import List, Dict, Any
from app.services.es_client import es_wrapper
from app.core.diagnostic import scanner
from app.core.fix_generator import fix_generator
from app.models.es_types import DiagnosticResult, FixProposal

HISTORY_INDEX = ".autofixer-history"

class AgentOrchestrator:
    """
    Manages the lifecycle of the Auto-Fixer Agent.
    1. Ensures history index exists (Memory).
    2. Runs diagnostics.
    3. Selects the most critical issue.
    4. Generates a fix.
    5. Records the plan.
    """
    
    def __init__(self):
        self.client = None

    async def _get_client(self):
        if not self.client:
            self.client = await es_wrapper.get_client()
        return self.client

    async def ensure_memory_index(self):
        """Creates the history index if it doesn't exist."""
        client = await self._get_client()
        exists = await client.indices.exists(index=HISTORY_INDEX)
        
        if not exists:
            await client.indices.create(
                index=HISTORY_INDEX,
                body={
                    "mappings": {
                        "properties": {
                            "timestamp": {"type": "date"},
                            "issue_id": {"type": "keyword"},
                            "action": {"type": "keyword"}, # "diagnosed", "fixed", "failed"
                            "details": {"type": "object"}
                        }
                    }
                }
            )

    async def run_autonomous_cycle(self) -> Dict[str, Any]:
        """
        Runs one full cycle: Diagnose -> Pick Top Issue -> Propose Fix.
        """
        await self.ensure_memory_index()
        client = await self._get_client()
        
        # 1. Diagnose
        issues = await scanner.scan_all()
        if not issues:
            return {"status": "idle", "message": "Cluster is healthy. No issues found."}

        # 2. Prioritize (Pick the first critical issue, or high)
        target_issue = None
        for issue in issues:
            if issue.severity == "critical":
                target_issue = issue
                break
        if not target_issue and issues:
            target_issue = issues[0] # Fallback to first issue

        # 3. Generate Fix
        proposal = await fix_generator.generate_fix(target_issue)
        
        # 4. Record to Memory (History)
        record = {
            "timestamp": int(time.time() * 1000),
            "issue_id": target_issue.issue_id,
            "action": "proposal_generated",
            "details": {
                "issue": target_issue.dict(),
                "proposal": proposal.dict()
            }
        }
        await client.index(index=HISTORY_INDEX, body=record)
        
        return {
            "status": "action_required",
            "target_issue": target_issue,
            "proposal": proposal
        }

    async def get_agent_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves past actions from memory."""
        client = await self._get_client()
        await self.ensure_memory_index()
        
        try:
            resp = await client.search(
                index=HISTORY_INDEX,
                body={
                    "sort": [{"timestamp": "desc"}],
                    "size": limit
                }
            )
            return [hit["_source"] for hit in resp["hits"]["hits"]]
        except Exception:
            return []

agent = AgentOrchestrator()