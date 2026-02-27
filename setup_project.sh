#!/bin/bash

# Define root
ROOT_DIR="elastic-autofixer-agent"
mkdir -p $ROOT_DIR

echo "🚀 Initializing Elastic Auto-Fixer Agent in $ROOT_DIR..."

# ---------------------------------------------------------
# 1. Backend Structure
# ---------------------------------------------------------
mkdir -p $ROOT_DIR/backend/app/core
mkdir -p $ROOT_DIR/backend/app/services
mkdir -p $ROOT_DIR/backend/app/models
mkdir -p $ROOT_DIR/backend/tests

# Create Backend Files
touch $ROOT_DIR/backend/Dockerfile
touch $ROOT_DIR/backend/app/__init__.py
touch $ROOT_DIR/backend/app/main.py
touch $ROOT_DIR/backend/app/config.py

touch $ROOT_DIR/backend/app/core/__init__.py
touch $ROOT_DIR/backend/app/core/diagnostic.py
touch $ROOT_DIR/backend/app/core/fix_generator.py
touch $ROOT_DIR/backend/app/core/validator.py
touch $ROOT_DIR/backend/app/core/benchmarker.py

touch $ROOT_DIR/backend/app/services/__init__.py
touch $ROOT_DIR/backend/app/services/es_client.py
touch $ROOT_DIR/backend/app/services/esre.py
touch $ROOT_DIR/backend/app/services/inference.py
touch $ROOT_DIR/backend/app/services/agent_flow.py

touch $ROOT_DIR/backend/app/models/__init__.py
touch $ROOT_DIR/backend/app/models/api.py
touch $ROOT_DIR/backend/app/models/es_types.py

# ---------------------------------------------------------
# 2. Kibana Plugin Structure
# ---------------------------------------------------------
PLUGIN_ROOT="$ROOT_DIR/kibana-plugin/autofixer_kibana"
mkdir -p $PLUGIN_ROOT/common
mkdir -p $PLUGIN_ROOT/public/services
mkdir -p $PLUGIN_ROOT/public/components
mkdir -p $PLUGIN_ROOT/server/routes

# Create Plugin Files
touch $PLUGIN_ROOT/kibana.json
touch $PLUGIN_ROOT/package.json
touch $PLUGIN_ROOT/tsconfig.json
touch $PLUGIN_ROOT/common/index.ts
touch $PLUGIN_ROOT/common/types.ts

touch $PLUGIN_ROOT/public/index.ts
touch $PLUGIN_ROOT/public/plugin.ts
touch $PLUGIN_ROOT/public/application.tsx
touch $PLUGIN_ROOT/public/services/api.ts

touch $PLUGIN_ROOT/server/index.ts
touch $PLUGIN_ROOT/server/plugin.ts
touch $PLUGIN_ROOT/server/routes/index.ts
touch $PLUGIN_ROOT/server/routes/autofixer.ts

# ---------------------------------------------------------
# 3. Root Files
# ---------------------------------------------------------
mkdir -p $ROOT_DIR/scripts
touch $ROOT_DIR/.env
touch $ROOT_DIR/docker-compose.yml
touch $ROOT_DIR/README.md
touch $ROOT_DIR/scripts/setup_cloud.sh
touch $ROOT_DIR/scripts/generate_bad_data.py
touch $ROOT_DIR/scripts/run_demo.sh

echo "✅ Folder structure created successfully."