# MCP Ingestion Tool - Test Plan

## Implementation Summary

✅ **Completed:** The `ingest_new_law` MCP tool has been successfully implemented in `mcp-server/src/index.ts`.

### Changes Made:

1. **Tool Definition** (Line ~145): Added to TOOLS array
2. **Case Handler** (Line ~190): Added to switch statement
3. **Implementation Function** (Line ~370): `handleIngestNewLaw()` with full logic

### Key Features:

- ✅ Executes Python scripts via `child_process`
- ✅ Loads credentials from `.env` and `.env.backend`
- ✅ Supports both local (Docker) and cloud (Qdrant Cloud/RDS) environments
- ✅ Automatic verification after ingestion
- ✅ Returns detailed success/error JSON responses

---

## Test Plan

### Test 1: Local Environment Test

**Objective:** Verify the tool works with local Docker instances of Qdrant and Postgres.

**Prerequisites:**
- Qdrant running on `localhost:6333`
- Postgres running on `localhost:5432`
- `.venv` activated with all dependencies

**Test Command:**
```bash
cd /home/spas/OPOS_GEMINI_1/mcp-server
node dist/index.js
```

**Expected MCP Tool Call (from client):**
```json
{
  "name": "ingest_new_law",
  "arguments": {
    "boe_id": "BOE-A-2023-12345"
  }
}
```

**Expected Response:**
```json
{
  "status": "success",
  "boe_id": "BOE-A-2023-12345",
  "scrape_summary": "📊 Total chunks/paragraphs extracted: 150",
  "ingest_summary": "✅ Ingestion COMPLETE for BOE-A-2023-12345",
  "verification": "✅ [Postgres] Total Text Chunks found: 150\n✅ [Qdrant] Total Vectors found: 150",
  "message": "Ley BOE-A-2023-12345 ingestada y verificada exitosamente"
}
```

---

### Test 2: Cloud Environment Test

**Objective:** Verify the tool works with Qdrant Cloud and local Postgres.

**Prerequisites:**
- Update `.env` with:
  ```
  QDRANT_URL=https://xyz.cloud.qdrant.io
  QDRANT_API_KEY=your_api_key_here
  ```

**Test Command:** Same as Test 1

**Expected Behavior:**
- Scraper runs locally
- Ingester connects to Qdrant Cloud (using API key)
- Verification confirms vectors in cloud instance

---

### Test 3: Error Handling Test

**Objective:** Verify proper error responses for invalid BOE IDs.

**Test Input:**
```json
{
  "name": "ingest_new_law",
  "arguments": {
    "boe_id": "INVALID-ID-9999"
  }
}
```

**Expected Response:**
```json
{
  "status": "error",
  "boe_id": "INVALID-ID-9999",
  "error_message": "Command failed: ...",
  "stderr": "Error: Could not fetch BOE page...",
  "stdout": ""
}
```

---

## Manual Testing Steps

### Step 1: Start MCP Server
```bash
cd /home/spas/OPOS_GEMINI_1/mcp-server
npm run build
node dist/index.js
```

### Step 2: Test with MCP Inspector (if available)
Or use the `test-server.js` script if it exists.

### Step 3: Verify Database
After successful ingestion, manually verify:
```bash
# Postgres
psql -h localhost -U postgres -d opositaia -c "SELECT COUNT(*) FROM laws WHERE law_id = 'BOE-A-2023-12345';"

# Qdrant
curl http://localhost:6333/collections/opositaia_knowledge/points/scroll \
  -H "Content-Type: application/json" \
  -d '{"filter": {"must": [{"key": "boe_id", "match": {"value": "BOE-A-2023-12345"}}]}, "limit": 1}'
```

---

## Next Steps

1. **Integration Testing:** Test the tool from the OpositaIA app agents
2. **Performance Testing:** Measure ingestion time for large laws (>1000 articles)
3. **Security Audit:** Verify no credentials are logged or exposed
4. **Documentation:** Update MCP README with usage examples

---

## Rollback Plan

If issues are found, restore the backup:
```bash
cp /home/spas/OPOS_GEMINI_1/mcp-server/src/index.ts.backup \
   /home/spas/OPOS_GEMINI_1/mcp-server/src/index.ts
cd /home/spas/OPOS_GEMINI_1/mcp-server && npm run build
```
