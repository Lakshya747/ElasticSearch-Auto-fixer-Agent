# 🛠️ Elastic Auto-Fixer Agent

> **An autonomous AI-powered SRE agent that detects, diagnoses, and fixes Elasticsearch cluster issues in real-time.**

Transform your Elasticsearch operations from reactive troubleshooting to **proactive, self-healing infrastructures**. Meet the agent that never sleeps, never misses a misconfiguration, and continuously optimizes your cluster performance.

---

## 🎯 The Problem

Elasticsearch clusters degrade silently:
- **Mapping explosions** ⚠️ – fields creep up to thousands, strangling query performance
- **Broken ILM policies** 📅 – indices pile up, storage balloons, costs skyrocket  
- **Inefficient queries** 🐌 – wildcard searches and unnecessary aggregations eat CPU
- **Stale settings** ⚙️ – misconfigured replica counts or refresh intervals slip through

SREs manually write runbooks. Teams page oncall engineers at 3 AM. **It doesn't have to be this way.**

---

## 💡 The Solution

**Elastic Auto-Fixer Agent** is a fully autonomous reasoning loop that:

1. **🔍 Continuously Scans** your cluster for misconfigurations
2. **🧠 Reasons Intelligently** using LLM inference (GPT-4 or your model of choice)
3. **🪄 Generates Fixes** in valid Elasticsearch DSL  
4. **⚡ Benchmarks** before & after to guarantee safety
5. **🔒 Applies** with backups and rollback safety
6. **📚 Learns** by storing every fix in a persistent knowledge base

All orchestrated through an **Agent Builder** pattern – your cluster becomes **self-healing**.

---

## 🚀 Key Features

### 🤖 Autonomous Agent Loop
- **Diagnostic Engine** – Scans indices for "bad-" patterns (mapping, ILM, query issues)
- **Fix Generator** – Calls Elasticsearch Inference API to reason about solutions
- **Validator** – Performs syntax checks and dry-runs before applying
- **Benchmarker** – Runs latency tests (before/after) to verify improvements
- **Memory** – Stores all decisions in `.autofixer-history` index for audit trails

### 🧠 LLM Integration
- **Elasticsearch Inference API** – Native integration with your deployed models
- **Intelligent Fallbacks** – Hardcoded expert rules ensure the demo works offline
- **Retrieval-Augmented Generation (RAG)** – Knowledge base index (`.autofixer-knowledge`) for contextualized advice
- **Prompt Engineering** – Structured prompts for consistent, actionable fixes

### 🎨 Multi-Platform UI
- **Kibana Plugin** – Native integration into your Elastic Stack UI
- **Streamlit Dashboard** – Quick local demo and testing interface
- **REST API** – Full programmatic control via FastAPI backend

### ✅ Safety & Compliance
- **Backup Before Apply** – Every fix captures the original state
- **Latency Verification** – Ensures proposed changes don't degrade performance
- **Transaction-Safe** – All operations are idempotent and reversible
- **Audit Trail** – Complete history of every scan, fix proposal, and application

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     ELASTIC AUTO-FIXER AGENT                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐      ┌──────────────┐      ┌─────────────┐      │
│  │  Diagnostic │      │ Fix Generator│      │  Validator  │      │
│  │   Engine    │─────▶│   (Inference)│─────▶│ (Dry-Run)   │      │
│  └─────────────┘      └──────────────┘      └─────────────┘      │
│         ▲                     │                     │              │
│         │                     ▼                     ▼              │
│  ┌─────────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Cluster Scanner │  │ ESRE Knowledge│  │ Benchmarker  │         │
│  │  (cat.indices)  │  │   Base (RAG)  │  │(Query Perf)  │         │
│  └─────────────────┘  └──────────────┘  └──────────────┘         │
│         │                     │                 │                 │
│         └──────────────┬──────┴─────────────────┘                 │
│                        ▼                                           │
│              ┌──────────────────────┐                             │
│              │  Agent Orchestrator  │                             │
│              │   (Memory & Flow)    │                             │
│              └──────────────────────┘                             │
│                        │                                           │
│         ┌──────────────┼──────────────┐                           │
│         ▼              ▼              ▼                           │
│    [Kibana UI]  [REST API]    [Streamlit Demo]                   │
│                                                                   │
└─────────────────────────────────────────────────────────────────────┘
                              ▼
                  Elasticsearch Cloud Serverless
                  (Cluster + Inference API)
```

---

## 🛠️ Tech Stack

| Layer | Technologies |
|-------|--------------|
| **Backend** | Python 3.11, FastAPI, Uvicorn |
| **Database** | Elasticsearch 8.12+ (Async Client) |
| **AI/Inference** | Elasticsearch Inference API (GPT-4, Claude, etc.) |
| **Frontend** | React 18, TypeScript, Kibana Plugin |
| **Demo UI** | Streamlit |
| **Containerization** | Docker, Docker Compose |
| **ORM/Validation** | Pydantic 2.6+ |
| **Environment** | Python-dotenv |

---

## 📦 Installation & Setup

### Prerequisites
- **Elasticsearch 8.12+** (Cloud Serverless recommended)
- **Python 3.11+**
- **Node.js 18+** (for Kibana plugin)
- **Docker & Docker Compose** (optional, for containerized setup)

### 1. Clone & Navigate
```bash
git clone https://github.com/yourusername/elastic-autofixer-agent.git
cd elastic-autofixer-agent
```

### 2. Configure Environment
Copy the template and fill in your Elasticsearch credentials:
```bash
cp .env.example .env
```

Edit `.env`:
```env
ELASTIC_CLOUD_ID=your-cloud-id
ELASTIC_API_KEY=your-api-key
ELASTIC_ENDPOINT=https://your-cluster.es.region.gcp.elastic.cloud:443
INFERENCE_MODEL_ID=gpt-4-turbo
BACKEND_PORT=8000
ENVIRONMENT=production
```

### 3. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

### 4. Start the Backend
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000/api/v1`

Health check:
```bash
curl http://localhost:8000/
```

### 5. (Optional) Kibana Plugin Setup
```bash
cd kibana-plugin/autofixer_kibana
npm install
npm run build
```

Then copy the built plugin into your Kibana `plugins/` directory.

### 6. (Optional) Run with Docker Compose
```bash
docker-compose up --build
```

This launches the FastAPI backend in a container connected to Elasticsearch Cloud.

---

## 🎬 Quick Start Demo

### Generate Test Data (Intentional Cluster Issues)
```bash
python scripts/generate_bad_data.py
```

This creates indices like:
- `bad-mapping-logs` – 1500+ fields (mapping explosion)
- `bad-ilm-timeseries` – misconfigured ILM policies
- `bad-query-performance` – inefficient query patterns

### Run the Agent Diagnostic Cycle
```bash
# Option 1: Via REST API
curl http://localhost:8000/api/v1/diagnose

# Option 2: Trigger autonomous cycle (scans, proposes, applies)
curl -X POST http://localhost:8000/api/v1/agent/run-cycle

# Option 3: View agent history
curl http://localhost:8000/api/v1/agent/history
```

### Launch Streamlit Dashboard
```bash
streamlit run demo_dashboard.py
```

Open `http://localhost:8501` in your browser to:
- 🔍 Scan cluster
- 💡 Generate AI fixes
- ⚡ Benchmark improvements
- ✅ Apply changes with one click

---

## 📡 API Endpoints

### Health & Status
```http
GET /
```
Returns cluster info and connection status.

### Diagnostics
```http
GET /api/v1/diagnose
```
Scans the cluster, returns list of detected issues.

**Response:**
```json
[
  {
    "issue_id": "IDX-001",
    "severity": "critical",
    "category": "mapping",
    "description": "Index bad-mapping-logs has 1500+ fields",
    "affected_resource": "bad-mapping-logs",
    "detected_at": "2024-01-15T10:30:00Z",
    "metrics": {
      "field_count": 1500,
      "mapping_size_mb": 45,
      "query_latency_ms": 2500
    }
  }
]
```

### Fix Generation
```http
POST /api/v1/generate-fix
Content-Type: application/json

{
  "issue_id": "IDX-001",
  "severity": "critical",
  "category": "mapping",
  "description": "Index has too many fields",
  "affected_resource": "bad-mapping-logs",
  "detected_at": "2024-01-15T10:30:00Z",
  "metrics": { "field_count": 1500 }
}
```

**Response:**
```json
{
  "issue_id": "IDX-001",
  "original_code": {
    "index": "bad-mapping-logs",
    "category": "mapping"
  },
  "fixed_code": {
    "index_settings": {
      "number_of_replicas": 1,
      "index.mapping.total_fields.limit": 3000
    }
  },
  "explanation": "Increased field limit and optimized replica settings.",
  "estimated_impact": "High - AI optimized."
}
```

### Benchmark Fix
```http
POST /api/v1/benchmark
Content-Type: application/json

{
  "issue_id": "IDX-001",
  "original_code": { ... },
  "fixed_code": { ... },
  "explanation": "...",
  "estimated_impact": "..."
}
```

**Response:**
```json
{
  "latency_before_ms": 2500.0,
  "latency_after_ms": 850.0,
  "cpu_before": 92.5,
  "cpu_after": 45.0,
  "improvement_percentage": 66.0,
  "is_safe": true
}
```

### Apply Fix
```http
POST /api/v1/apply-fix
Content-Type: application/json
```

### Autonomous Agent Cycle
```http
POST /api/v1/agent/run-cycle
```

Runs one full loop: **Diagnose → Prioritize → Generate Fix → Benchmark → Apply → Record**.

### Agent History
```http
GET /api/v1/agent/history
```

Returns all past fix attempts with outcomes.

---

## 🧠 How the Agent Reasons

### The Loop
1. **Scan Phase**: `ClusterScanner` calls `client.cat.indices()` and checks for "bad-" patterns
2. **Analyze Phase**: For each issue, metadata is extracted (field count, ILM settings, query patterns)
3. **Reason Phase**: Prompt sent to Elasticsearch Inference API:
   ```
   "You are an Elasticsearch Expert. Problem: {description}. 
    Generate ONLY valid JSON: { fixed_code: {...}, explanation: '...' }"
   ```
4. **Validate Phase**: `Validator` checks JSON syntax, performs dry-run on test indices
5. **Benchmark Phase**: Runs original query 5x, then fixed query 5x, compares latency
6. **Apply Phase**: Updates index settings/mappings, records decision to `.autofixer-history`
7. **Learn Phase**: Stores the fix pattern in `.autofixer-knowledge` index for future reference

### Fallback Logic
If the Inference API is unavailable, the agent uses **hardcoded expert rules**:
- **Mapping issues**: Increase `index.mapping.total_fields.limit`, remove unused fields
- **ILM issues**: Configure appropriate rollover intervals and retention policies
- **Query issues**: Suggest query rewrites to avoid wildcards and expensive aggregations

This ensures the demo **always works** even without an LLM.

---

## 📊 Example: Fixing a Mapping Explosion

**Before:**
```json
{
  "bad-mapping-logs": {
    "mappings": {
      "properties": {
        "field_0": { "type": "text" },
        "field_1": { "type": "text" },
        // ... 1498 more fields
        "field_1499": { "type": "text" }
      }
    }
  }
}
```

**Agent Decision:**
```
Issue Detected: bad-mapping-logs has 1500+ fields (limit is usually 1000)
  → Risk: Queries slow down exponentially
  → Cause: Unstructured logging without schema enforcement

AI Proposal:
  1. Increase index.mapping.total_fields.limit to 3000
  2. Add index.codec=best_compression
  3. Reduce index.refresh_interval to 30s (from 1s)
  4. Enable index.lifecycle.name=logs-default-ilm
```

**Benchmark Results:**
```
Query: range query on @timestamp (full scan of 1M docs)
Before:  2,400 ms (98% CPU)
After:      850 ms (45% CPU)
Improvement: 65% latency reduction ✅ SAFE
```

**Applied:**
```
Index settings updated
Backed up original state to .autofixer-history
Decision recorded with outcome
```

---

## 🔐 Security & Compliance

### API Key Management
The agent uses a dedicated, scoped API key with minimal privileges:
```json
{
  "cluster": ["monitor", "manage_ilm", "manage_pipeline"],
  "indices": [
    {
      "names": [".autofixer-*"],
      "privileges": ["all"]
    },
    {
      "names": ["*"],
      "privileges": ["monitor", "view_index_metadata", "manage"]
    }
  ]
}
```

Generate your own:
```bash
python scripts/generate_api_key.py
```

### Audit Trail
Every decision is logged:
- **Diagnostics**: What was detected
- **Proposals**: Why this fix was suggested
- **Benchmarks**: Performance before/after
- **Applications**: What was actually changed
- **Outcomes**: Success or rollback

Access via:
```bash
curl http://localhost:8000/api/v1/agent/history
```

---

## 🚦 Project Status

| Component | Status | Details |
|-----------|--------|---------|
| **Agent Core** | ✅ Stable | Diagnostic, fix generation, validation working |
| **Elasticsearch Integration** | ✅ Stable | Async client, Cloud Serverless tested |
| **Inference API** | ✅ Stable | GPT-4 integration + fallbacks |
| **Kibana Plugin** | ✅ Alpha | Basic UI, ready for Kibana 8.x |
| **Streamlit Demo** | ✅ Working | Perfect for quick testing |
| **Docker** | ✅ Ready | Single-command deployment |

---

## 📈 Roadmap

- [ ] **Multi-cluster orchestration** – Manage multiple Elasticsearch deployments
- [ ] **Advanced RAG** – Integrate ELSER for semantic search over knowledge base
- [ ] **Cost optimization** – Recommend reserved capacity and index downsizing
- [ ] **Alerting** – Slack/PagerDuty notifications when issues detected
- [ ] **Web UI** – Standalone Next.js dashboard (no Kibana dependency)
- [ ] **Machine Learning** – Train custom models on cluster patterns
- [ ] **Ansible/Terraform** – Infrastructure-as-code output options

---

## 🤝 Contributing

We welcome PRs! Areas to improve:
- More diagnostic rules (serverless autoscaling, vector search)
- Enhanced LLM prompts for better fix quality
- Performance optimizations for large clusters
- Additional benchmark metrics (memory, GC pauses)
- Multi-language support in fix explanations

Please open an issue first to discuss your idea.

---

## 📄 License

Licensed under the **MIT License**. See [LICENSE.txt](LICENSE.txt) for details.

---

## 👏 Credits

Built with ❤️ for the **ESAB Hackathon 2025**.

- **Problem**: Elasticsearch clusters degrade silently
- **Solution**: Autonomous AI-powered SRE agent
- **Stack**: FastAPI + Elasticsearch Inference API + Kibana

---

## 📞 Support & Feedback

- **Issues**: [GitHub Issues](https://github.com/yourusername/elastic-autofixer-agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/elastic-autofixer-agent/discussions)
- **Email**: your-email@example.com
- **Twitter**: [@your_handle](https://twitter.com/your_handle) | tag [@elastic_devs](https://twitter.com/elastic_devs)

---

## 🎥 Demo Video

**[Watch the 3-minute walkthrough](https://youtu.be/your-video-link)**

See the agent in action:
1. Scanning a broken cluster (mapping explosion, ILM failures)
2. Proposing AI-generated fixes
3. Benchmarking improvements
4. Applying changes safely
5. Verifying the cluster is now healthy

---

<div align="center">

### **Turn your Elasticsearch cluster into a self-healing system.**

**[⭐ Star us on GitHub](https://github.com/yourusername/elastic-autofixer-agent)** | **[🚀 Get Started](#-installation--setup)**

</div>
