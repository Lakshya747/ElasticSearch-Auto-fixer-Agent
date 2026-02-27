import asyncio
import os
from elasticsearch import AsyncElasticsearch
from dotenv import load_dotenv

# Load Admin Credentials
load_dotenv("../.env")

ELASTIC_ENDPOINT = os.getenv("ELASTIC_ENDPOINT")
ELASTIC_API_KEY = os.getenv("ELASTIC_API_KEY") # Must be a superuser key initially

async def create_agent_role():
    if not ELASTIC_ENDPOINT or not ELASTIC_API_KEY:
        print("❌ Please fill in .env first!")
        return

    client = AsyncElasticsearch(
        hosts=ELASTIC_ENDPOINT,
        api_key=ELASTIC_API_KEY
    )

    # Define the precise permissions needed
    # 1. Read cluster health/stats (monitor)
    # 2. Manage system indices for history/knowledge (.autofixer-*)
    # 3. View index metadata (monitor)
    # 4. Update index settings/mappings (manage)
    
    role_descriptor = {
        "cluster": ["monitor", "manage_ilm", "manage_pipeline"],
        "indices": [
            {
                "names": [".autofixer-*"],
                "privileges": ["all"]
            },
            {
                "names": ["*"], # Ideally restricted to specific data streams
                "privileges": ["monitor", "view_index_metadata", "manage"]
            }
        ]
    }
    
    try:
        # Create the API Key
        response = await client.security.create_api_key(
            name="autofixer-agent-key",
            role_descriptors={"autofixer-role": role_descriptor}
        )
        
        print("\n✅ API Key Created Successfully!")
        print(f"ID: {response['id']}")
        print(f"API Key (Save this to .env): {response['encoded']}")
        
    except Exception as e:
        print(f"❌ Error creating key: {e}")
        
    await client.close()

if __name__ == "__main__":
    asyncio.run(create_agent_role())