#!/bin/bash
echo "🚀 Starting Backend..."
# Run in background
uvicorn app.main:app --reload &

echo "🔥 Generating Bad Data..."
python scripts/generate_bad_data.py

echo "✅ Demo Environment Ready!"
echo "👉 Open Kibana to see the agent working."