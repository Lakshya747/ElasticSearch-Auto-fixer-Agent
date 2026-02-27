import time
import asyncio
from typing import Dict, Any, List
from app.services.es_client import es_wrapper
from app.models.es_types import BenchmarkResult

class Benchmarker:
    """
    Measures the performance impact of a query or mapping change.
    Runs 'before' vs 'after' tests.
    """
    
    def __init__(self):
        self.client = None

    async def _get_client(self):
        if not self.client:
            self.client = await es_wrapper.get_client()
        return self.client

    async def benchmark_query(self, index: str, query_body: Dict[str, Any], runs: int = 5) -> float:
        """
        Runs a query N times and returns average latency in ms.
        """
        client = await self._get_client()
        total_time = 0
        
        for i in range(runs):
            try:
                # Use profile API to get strict execution time
                start = time.perf_counter()
                await client.search(
                    index=index,
                    body=query_body,
                    request_cache=False, # Disable cache for fair test
                    size=10
                )
                end = time.perf_counter()
                total_time += (end - start) * 1000 # convert to ms
            except Exception as e:
                print(f"Benchmark run {i} failed: {e}")
                return -1.0 # Indicate failure
        
        return round(total_time / runs, 2)

    async def compare(self, index: str, original_query: Dict[str, Any], optimized_query: Dict[str, Any]) -> BenchmarkResult:
        """
        Compares original vs optimized query performance.
        """
        latency_before = await self.benchmark_query(index, original_query)
        latency_after = await self.benchmark_query(index, optimized_query)
        
        # Calculate improvement
        improvement = 0.0
        if latency_before > 0:
            improvement = ((latency_before - latency_after) / latency_before) * 100
            
        return BenchmarkResult(
            latency_before_ms=latency_before,
            latency_after_ms=latency_after,
            cpu_before=0.0, # Placeholder (requires extensive monitoring setup)
            cpu_after=0.0,
            improvement_percentage=round(improvement, 2),
            is_safe=(latency_after <= latency_before) # Safe if faster or equal
        )

benchmarker = Benchmarker()