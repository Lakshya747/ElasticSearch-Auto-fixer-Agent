from typing import List, Dict, Any
from app.services.es_client import es_wrapper

KNOWLEDGE_INDEX = ".autofixer-knowledge"

class ESREService:
    """
    Manages the Knowledge Base (ESRE) for Retrieval Augmented Generation.
    Stores expert advice on how to fix specific Elasticsearch errors.
    """
    
    def __init__(self):
        self.client = None

    async def _get_client(self):
        if not self.client:
            self.client = await es_wrapper.get_client()
        return self.client

    async def initialize_knowledge_base(self):
        """
        Creates the index and populates it with default expert rules.
        """
        client = await self._get_client()
        exists = await client.indices.exists(index=KNOWLEDGE_INDEX)
        
        if not exists:
            # Create index with semantic-friendly settings
            await client.indices.create(
                index=KNOWLEDGE_INDEX,
                body={
                    "mappings": {
                        "properties": {
                            "topic": {"type": "keyword"},
                            "content": {"type": "text", "analyzer": "english"},
                            "solution_template": {"type": "text"}
                        }
                    }
                }
            )
            
            # Seed with default expert knowledge
            docs = [
                {
                    "topic": "wildcard",
                    "content": "Leading wildcards (e.g., *query) cause full term dictionary scans, killing CPU.",
                    "solution_template": "Use 'prefix' query or 'match_phrase_prefix' instead of leading wildcards."
                },
                {
                    "topic": "pagination",
                    "content": "Deep pagination using from/size > 10,000 causes OOM (Out of Memory) errors.",
                    "solution_template": "Use 'search_after' with a PIT (Point in Time) for deep scrolling."
                },
                {
                    "topic": "mapping",
                    "content": "Mapping explosion occurs when too many dynamic fields are created.",
                    "solution_template": "Set 'dynamic': 'strict' and explicitly map known fields."
                },
                 {
                    "topic": "ilm",
                    "content": "Indices growing indefinitely cause shard imbalance and slow recovery.",
                    "solution_template": "Apply an ILM policy with rollover at 50GB or 30 days."
                }
            ]
            
            # Bulk index the knowledge
            body = []
            for doc in docs:
                body.append({"index": {"_index": KNOWLEDGE_INDEX}})
                body.append(doc)
            
            await client.bulk(body=body)
            print(f"📚 ESRE Knowledge Base seeded with {len(docs)} expert rules.")

    async def retrieve_context(self, query_text: str) -> str:
        """
        Searches the knowledge base for relevant advice based on the error description.
        """
        client = await self._get_client()
        
        # Simple BM25 search (can be upgraded to ELSER/Vector later)
        resp = await client.search(
            index=KNOWLEDGE_INDEX,
            body={
                "query": {
                    "match": {
                        "content": query_text
                    }
                },
                "size": 1
            }
        )
        
        hits = resp.get("hits", {}).get("hits", [])
        if hits:
            doc = hits[0]["_source"]
            return f"EXPERT ADVICE: {doc['content']} SOLUTION: {doc['solution_template']}"
        
        return "No specific expert advice found."

esre = ESREService()