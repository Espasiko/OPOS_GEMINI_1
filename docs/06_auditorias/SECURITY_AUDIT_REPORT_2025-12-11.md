# Security Audit Report - OpositaIA Backend
**Date:** December 11, 2025
**Auditor:** GitHub Copilot (BMad Master Mode)
**Methodology:** Security Audit Personas (Hacker, Defender, Auditor)

## 1. Executive Summary
This report details the findings of a security audit performed on the `backend` directory. The audit focused on credential management, network configuration, and code practices. While recent fixes have improved the security posture of ingestion scripts, significant risks remain in legacy scripts and configuration management.

## 2. Findings

### 2.1. Hardcoded Credentials (CRITICAL)
**Status:** ⚠️ Partially Mitigated / Risk Remains
**Description:** Several files still contain hardcoded secrets or default passwords acting as fallbacks.
**Evidence:**
- `backend/agents/ingest_missing_laws.py`: Contains fallback `DB_PASSWORD = "postgres"` (Mitigated with warning, but still present).
- `backend/migrate_qdrant_simple.py`: **CRITICAL**. Contains a full JWT token hardcoded: `API_KEY = "eyJhbGci..."`.
- `backend/scripts/check_qdrant_status.py`: Hardcoded `key="layer"`.
- `backend/agents/rag_agent.py`: Hardcoded `key="tema_id"`.

**Recommendation:**
- **Immediate:** Rotate the JWT token found in `migrate_qdrant_simple.py`.
- **Action:** Remove all default password fallbacks. The application must fail to start if secrets are missing (Fail Secure).

### 2.2. Network Exposure & Hardcoded URLs (HIGH)
**Status:** ⚠️ High Risk
**Description:** Multiple scripts hardcode `localhost` or `0.0.0.0`, which breaks container isolation and creates ambiguity between dev/prod environments.
**Evidence:**
- 20+ occurrences of `http://localhost:6333` (Qdrant) and `http://localhost:11434` (Ollama) hardcoded in scripts like `main.py`, `rag_agent_v2.py`, `check_qdrant_status.py`.
- `backend/main.py` defaults to `0.0.0.0`, exposing the API to all interfaces.

**Recommendation:**
- Centralize configuration in a `config.py` file that reads from environment variables.
- Replace all `localhost` references with `os.getenv("SERVICE_HOST", "localhost")` to support Docker networking (`opositaia-qdrant`, `opositaia-postgres`).

### 2.3. Logging Practices (MEDIUM)
**Status:** ⚠️ Needs Improvement
**Description:** Extensive use of `print()` statements instead of structured logging. This makes monitoring difficult and risks leaking sensitive data to stdout.
**Evidence:**
- `backend/agents/ingest_boe_4layers_extended.py`: Uses `print("DEBUG: ...")`.
- `backend/test_all_providers.py`: Uses `print()` for test outputs.

**Recommendation:**
- Replace `print()` with Python's `logging` module.
- Ensure log levels (INFO, DEBUG, ERROR) are configurable via env vars.

### 2.4. Qdrant Security (HIGH)
**Status:** ❌ Unsecured
**Description:** Qdrant is accessed without authentication in most scripts.
**Evidence:**
- `QdrantClient(host="localhost", port=6333)` is the standard pattern found.
- No `api_key` parameter is passed in most instantiations.

**Recommendation:**
- Enforce `QDRANT_API_KEY` usage in all Qdrant clients.
- Configure Qdrant container to require authentication in production.

## 3. Action Plan (Backlog)

| ID | Priority | Task | Owner |
| :--- | :--- | :--- | :--- |
| SEC-001 | **Critical** | Rotate exposed JWT in `migrate_qdrant_simple.py` and remove file from history if needed. | DevOps |
| SEC-002 | **High** | Refactor `backend/main.py` and agents to use a central `config.py` for URLs and Ports. | Backend Dev |
| SEC-003 | **High** | Implement `QDRANT_API_KEY` support across all RAG agents. | Backend Dev |
| SEC-004 | **Medium** | Replace `print()` with `logging` in all backend scripts. | Backend Dev |
| SEC-005 | **Medium** | Remove default "postgres" password fallbacks; enforce env var presence. | Backend Dev |

---
*End of Report*
