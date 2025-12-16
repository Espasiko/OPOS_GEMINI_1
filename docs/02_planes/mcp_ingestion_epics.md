---
stepsCompleted: 
  - step-01-validate-prerequisites
inputDocuments: 
  - USER_PROMPT_CHAT
---

# OpositaIA MCP - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for the **OpositaIA MCP Ingestion Feature**. It ensures that external agents (like the OpositaIA App agents) can autonomously ingest and verify new laws into the RAG knowledge base.

## Requirements Inventory

### Functional Requirements

FR1: The MCP server must expose a tool `ingest_new_law` that accepts a `boe_id`.
FR2: The tool must trigger the universal Python scraping and ingestion scripts for the given BOE ID.
FR3: The ingestion process must execute a verification step immediately after to confirm data integrity in both PostgreSQL and Qdrant.
FR4: The system must return a success/failure confirmation to the calling agent.

### NonFunctional Requirements

NFR1: **Environment Security**: Database credentials (Postgres Host, Qdrant URL/Key) must be loaded from `.env` or `.env.backend` files, NEVER hardcoded.
NFR2: **Platform Agnostic**: Must work for both Local (Docker) and Cloud (Qdrant Cloud/RDS) environments purely by changing environment variables.
NFR3: **Agent Autonomy**: The tool must handle the end-to-end process (Scrape -> Processing -> DB -> Verification) so the calling agent doesn't need to manage sub-steps.

### Additional Requirements

- Leverage existing Python scripts (`scrape_boe_universal.py`, `ingest_scraped_universal.py`, `verify_ingestion_universal.py`) via `child_process`.
- Ensure output logs are captured and returned (or summarized) in the MCP tool response to help the agent verify success.

### FR Coverage Map

- Epic 1 covers FR1, FR2, FR3, FR4

## Epic List

1. **Automated Law Ingestion via MCP**

---

## Epic 1: Automated Law Ingestion via MCP

Enable AI Agents to autonomously ingest new laws into the knowledge base by simply providing a valid BOE identifier.

### Story 1.1: Implement `ingest_new_law` MCP Tool

As a **Knowledge Base Manager Agent**,
I want **call a single function `ingest_new_law` with a BOE ID**,
So that **I can populate the RAG database with new legal content without needing manual developer intervention.**

**Acceptance Criteria:**

**Given** the MCP server is running and configured with valid `.env` credentials
**When** an agent calls `ingest_new_law(boe_id='BOE-A-2024-1234')`
**Then** the server executes `scrape_boe_universal.py` for that ID
**And** upon success, it executes `ingest_scraped_universal.py`
**And** upon success, it executes `verify_ingestion_universal.py`
**And** returns a JSON response indicating `status: "success"`, summary of chunks/vectors verified, and any relevant logs.
**And** if any step fails, it returns `status: "error"` with the specific log output.

---

### Story 1.2: Environment Variable & Verification Wiring

As a **System Administrator**,
I want **the MCP tool to rely strictly on environment variables (`.env`, `.env.backend`)**,
So that **I can switch between Local and Cloud infrastructure (e.g., Qdrant Cloud) without changing the MCP code.**

**Acceptance Criteria:**

**Given** a `.env` file containing `QDRANT_URL=https://cloud...` and `QDRANT_API_KEY=xyz`
**When** the `ingest_new_law` tool executes the Python scripts
**Then** the Python scripts receive these environment variables correctly (injected into the child process)
**And** the scripts successfully verify against the Cloud instance instead of localhost
**And** no API keys or hostnames are present in the TypeScript source code.
