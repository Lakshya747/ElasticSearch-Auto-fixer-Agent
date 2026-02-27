import asyncio
import os
from pathlib import Path
from elasticsearch import AsyncElasticsearch, BadRequestError
from dotenv import load_dotenv

# 1. Load Environment Variables safely
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

ELASTIC_ENDPOINT = os.getenv("ELASTIC_ENDPOINT")
ELASTIC_API_KEY = os.getenv("ELASTIC_API_KEY")

async def ruin_cluster():
    if not ELASTIC_ENDPOINT or not ELASTIC_API_KEY:
        print("❌ Error: .env variables are missing.")
        return

    print(f"🔌 Connecting to: {ELASTIC_ENDPOINT}")
    
    client = AsyncElasticsearch(
        hosts=ELASTIC_ENDPOINT,
        api_key=ELASTIC_API_KEY
    )

    try:
        # ---------------------------------------------------------
        # SCENARIO 1: Mapping Explosion (1500 fields)
        # ---------------------------------------------------------
        index_name = "bad-mapping-logs"
        print(f"💥 creating '{index_name}'...")
        
        # Delete if exists
        if await client.indices.exists(index=index_name):
            await client.indices.delete(index=index_name)

        # CRITICAL FIX: We create the index explicitly with a higher limit
        # so we can insert the bad data without getting a 400 Error.
        await client.indices.create(
            index=index_name,
            settings={
                "index.mapping.total_fields.limit": 5000  # Allow up to 5000 fields
            }
        )

        # Generate the payload with 1500 fields
        doc = {f"field_{i}": f"value_{i}" for i in range(1500)}
        doc["@timestamp"] = "2024-01-01T00:00:00Z"
        
        await client.index(index=index_name, document=doc)
        print(f"✅ Created {index_name} with 1500 dynamic fields (Mapping Explosion)")

        # ---------------------------------------------------------
        # SCENARIO 2: ILM Missing (Large Index)
        # ---------------------------------------------------------
        index_name_ilm = "bad-ilm-logs-000001"
        print(f"📉 creating '{index_name_ilm}'...")
        
        if await client.indices.exists(index=index_name_ilm):
            await client.indices.delete(index=index_name_ilm)
            
        # Create without settings (defaults to no ILM)
        await client.indices.create(index=index_name_ilm)
        
        # Insert some dummy data
        bulk_data = []
        for i in range(50):
            bulk_data.append({"index": {"_index": index_name_ilm}})
            bulk_data.append({"message": "Log without lifecycle policy", "count": i})
        
        await client.bulk(operations=bulk_data)
        print(f"✅ Created {index_name_ilm} without ILM policy")

        print("\n🔥 Cluster is successfully sabotaged! Ready for Auto-Fixer Demo.")

    except Exception as e:
        print(f"❌ Error during sabotage: {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(ruin_cluster())