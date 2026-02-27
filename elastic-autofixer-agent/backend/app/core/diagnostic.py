import asyncio
from typing import List, Dict, Any
from app.services.es_client import es_wrapper
from app.models.es_types import DiagnosticResult

class ClusterScanner:
    def __init__(self):
        self.client = None

    async def _get_client(self):
        if not self.client:
            self.client = await es_wrapper.get_client()
        return self.client

    async def scan_all(self) -> List[DiagnosticResult]:
        print("🔍 Scanning Cluster (Simplified Mode)...")
        client = await self._get_client()
        issues = []
        
        try:
            # Get all indices
            indices = await client.cat.indices(format="json")
            print(f"📊 Total indices found: {len(indices)}")
            
            for idx in indices:
                name = idx['index']
                print(f"   Scanning index: {name}")
                
                # CRUCIAL: Check for "bad-" prefix in index name
                if "bad-" in name:
                    print(f"   ✓ Detected 'bad-' prefix in index: {name}")
                    
                    # MAPPING CHECK: Handle bad-mapping indices
                    if "mapping" in name:
                        try:
                            mapping = await client.indices.get_mapping(index=name)
                            props = mapping[name]['mappings'].get('properties', {})
                            count = len(props)
                            print(f"   ⚠️ Bad Mapping Issue: {name} has {count} fields")
                            
                            issues.append(DiagnosticResult(
                                issue_id=f"mapping_{name}",
                                severity="critical",
                                category="mapping",
                                description=f"Mapping Explosion: Index has {count} fields (Limit 1000).",
                                affected_resource=name,
                                detected_at="now",
                                metrics={"field_count": count}
                            ))
                        except Exception as e:
                            print(f"   ❌ Error checking mapping for {name}: {e}")
                    
                    # ILM CHECK: Handle bad-ilm indices
                    if "ilm" in name:
                        try:
                            # Treat missing ILM as critical issue
                            size = idx.get('store.size', 'unknown')
                            print(f"   ⚠️ Bad ILM Issue: {name} has no lifecycle policy (Size: {size})")
                            
                            issues.append(DiagnosticResult(
                                issue_id=f"missing_ilm_{name}",
                                severity="critical",
                                category="ilm",
                                description="Missing ILM Policy: Index will grow indefinitely.",
                                affected_resource=name,
                                detected_at="now",
                                metrics={"size": size}
                            ))
                        except Exception as e:
                            print(f"   ❌ Error checking ILM for {name}: {e}")
                else:
                    print(f"   ○ Skipping normal index: {name}")
                    
        except Exception as e:
            print(f"❌ Scan Failed: {e}")
            
        print(f"✅ Scan Complete. Found {len(issues)} issues.")
        return issues

scanner = ClusterScanner()