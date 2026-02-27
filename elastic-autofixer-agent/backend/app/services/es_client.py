import asyncio
from elasticsearch import AsyncElasticsearch
from app.config import settings

class ESClientWrapper:
    client: AsyncElasticsearch = None

    async def connect(self):  # <--- Make this async explicitly
        """Initializes the Async Elasticsearch client."""
        if self.client is None and settings.ELASTIC_ENDPOINT:
            print(f"🔌 Connecting to Elastic Cloud: {settings.ELASTIC_ENDPOINT}...")
            self.client = AsyncElasticsearch(
                hosts=settings.ELASTIC_ENDPOINT,
                api_key=settings.ELASTIC_API_KEY,
                request_timeout=30,
                max_retries=3,
                retry_on_timeout=True
            )
            # Verify connection immediately
            try:
                info = await self.client.info()
                print(f"✅ Client initialized. Connected to: {info['cluster_name']}")
            except Exception as e:
                print(f"❌ Connection Check Failed: {e}")
                self.client = None # Reset so we retry later

    async def close(self):
        if self.client:
            await self.client.close()
            print("🔌 Client closed.")
            self.client = None

    async def get_client(self) -> AsyncElasticsearch:
        if self.client is None:
            await self.connect()  # <--- Await this call
        
        if self.client is None:
            raise Exception("❌ CRITICAL: Could not connect to Elasticsearch.")
            
        return self.client

# Singleton instance
es_wrapper = ESClientWrapper()