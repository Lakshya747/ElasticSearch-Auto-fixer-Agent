from pydantic import BaseModel

class HealthCheck(BaseModel):
    status: str
    es_version: str
    cluster_name: str