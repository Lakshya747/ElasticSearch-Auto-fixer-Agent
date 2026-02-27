from typing import Dict, Any, Optional
from app.services.es_client import es_wrapper
from app.config import settings
import json

class InferenceService:
    """
    Wraps the Elasticsearch Inference API to generate fixes using an LLM.
    """
    
    def __init__(self):
        self.client = None

    async def _get_client(self):
        if not self.client:
            self.client = await es_wrapper.get_client()
        return self.client

    async def generate_fix_proposal(self, context: str, bad_code: str) -> Dict[str, Any]:
        """
        Sends a prompt to the Inference API.
        """
        client = await self._get_client()
        
        # 1. Construct the Prompt
        prompt = f"""
        You are an Elasticsearch Expert.
        Context: {context}
        Problem Code: {bad_code}
        
        Task: 
        1. Fix the problem code.
        2. Return ONLY a valid JSON object.
        3. Structure: {{ "fixed_code": {{...}}, "explanation": "..." }}
        """

        try:
            # 2. Call Inference API (Requires ES 8.12+)
            # Note: This assumes you have a model deployed named 'gpt-4' or similar
            # If not configured, this will throw an error, and we catch it below.
            if settings.ELASTIC_API_KEY and settings.INFERENCE_MODEL_ID:
                response = await client.inference.inference(
                    task_type="completion",
                    inference_id=settings.INFERENCE_MODEL_ID,
                    body={"input": prompt}
                )
                
                # Parse the LLM response
                result_text = response.get("inference_results", [{}])[0].get("predicted_value", "{}")
                return json.loads(result_text)
                
        except Exception as e:
            print(f"⚠️ Inference API failed (using fallback rules): {e}")
            
        # 3. Fallback Mechanism (If Inference API is not set up)
        return self._fallback_logic(bad_code)

    def _fallback_logic(self, bad_code: str) -> Dict[str, Any]:
        """
        Hardcoded rules to ensure the Demo works even without an LLM connected.
        """
        bad_code_lower = bad_code.lower()

        # 1. Mapping Fix (Detects 'mapping' in the resource name)
        if "mapping" in bad_code_lower:
            return {
                "fixed_code": {
                    "dynamic": "strict",
                    "properties": {
                        "@timestamp": {"type": "date"},
                        "message": {"type": "text"},
                        "log.level": {"type": "keyword"}
                    }
                },
                "explanation": "Fallback: Detected Mapping Explosion. Solution: Disable dynamic mapping ('strict') to prevent new fields from being created automatically."
            }

        # 2. ILM Fix (Detects 'ilm' in the resource name)
        if "ilm" in bad_code_lower:
            return {
                "fixed_code": {
                    "policy": {
                        "phases": {
                            "hot": {
                                "actions": {
                                    "rollover": {
                                        "max_size": "50GB",
                                        "max_age": "30d"
                                    }
                                }
                            },
                            "delete": {
                                "min_age": "90d",
                                "actions": {
                                    "delete": {}
                                }
                            }
                        }
                    }
                },
                "explanation": "Fallback: Detected missing Lifecycle Policy. Solution: Apply standard Hot-Warm-Delete ILM policy to manage index size."
            }

        # 3. Wildcard Fix Fallback
        if "*" in bad_code:
            return {
                "fixed_code": {
                    "query": {
                        "match_phrase_prefix": {
                            "field": "message",
                            "query": "search_term"
                        }
                    }
                },
                "explanation": "Fallback: Replaced wildcard with match_phrase_prefix."
            }
        
        # 4. Pagination Fix Fallback
        if "from" in bad_code and "10000" in bad_code:
            return {
                "fixed_code": {
                    "search_after": ["<last_sort_value>"],
                    "size": 10,
                    "sort": [{"@timestamp": "desc"}]
                },
                "explanation": "Fallback: Replaced deep pagination with search_after."
            }

        return {
            "fixed_code": {}, 
            "explanation": "No fix could be generated (Fallback mode)."
        }

inference_service = InferenceService()