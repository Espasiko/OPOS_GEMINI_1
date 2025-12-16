---
stepsCompleted: 
  - requirements-gathering
inputDocuments: 
  - USER_REQUEST_CHAT
  - PROJECT_STRUCTURE_ANALYSIS
---

# OpositaIA pnpm Migration - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for **migrating OpositaIA from npm to pnpm**. The migration will improve disk space efficiency, installation speed, and dependency management across the monorepo structure.

## Requirements Inventory

### Functional Requirements

FR1: Replace all `npm` commands with `pnpm` equivalents across the project.
FR2: Migrate `package-lock.json` files to `pnpm-lock.yaml`.
FR3: Update CI/CD pipelines to use `pnpm` instead of `npm`.
FR4: Update documentation (README files, setup guides) to reflect `pnpm` usage.
FR5: Ensure all existing scripts (`npm run ...`) work identically with `pnpm run ...`.

### NonFunctional Requirements

NFR1: **Zero Downtime**: Development workflow must not be interrupted during migration.
NFR2: **Backward Compatibility**: Existing Docker containers and deployment scripts must continue to work.
NFR3: **Performance**: Installation time should improve by at least 30%.
NFR4: **Disk Space**: `node_modules` size should reduce by at least 40% (via symlinks/hard links).

### Additional Requirements

- Preserve existing `.gitignore` rules for `node_modules` and lock files.
- Ensure `pnpm` workspace configuration is optimal for monorepo structure (frontend, backend, mcp-server).
- Update VSCode/IDE settings if needed for `pnpm` compatibility.

### FR Coverage Map

- Epic 1 covers FR1, FR2, FR5
- Epic 2 covers FR3, FR4

## Epic List

1. **Core pnpm Migration**
2. **CI/CD & Documentation Update**

---

## Epic 1: Core pnpm Migration

Migrate all JavaScript/TypeScript projects from npm to pnpm, ensuring functional equivalence.

### Story 1.1: Install pnpm Globally

As a **Developer**,
I want **pnpm installed globally on the development machine**,
So that **I can use `pnpm` commands across all projects.**

**Acceptance Criteria:**

**Given** a fresh development environment
**When** I run `pnpm --version`
**Then** it returns a version >= 8.0.0
**And** `pnpm` is available in the system PATH.

**Implementation:**
```bash
npm install -g pnpm@latest
```

---

### Story 1.2: Migrate Frontend (React + Vite)

As a **Frontend Developer**,
I want **the frontend project to use pnpm**,
So that **dependencies install faster and use less disk space.**

**Acceptance Criteria:**

**Given** the `frontend/` directory with `package.json` and `package-lock.json`
**When** I run `pnpm install` in `frontend/`
**Then** a `pnpm-lock.yaml` is created
**And** `node_modules` is populated correctly
**And** `pnpm run dev` starts the Vite dev server
**And** `pnpm run build` creates a production build
**And** `package-lock.json` is deleted.

**Implementation Steps:**
1. `cd frontend`
2. `rm -rf node_modules package-lock.json`
3. `pnpm install`
4. `pnpm run dev` (verify)
5. `pnpm run build` (verify)
6. `git add pnpm-lock.yaml`
7. `git rm package-lock.json`

---

### Story 1.3: Migrate Backend (FastAPI + Python)

As a **Backend Developer**,
I want **the backend Node.js scripts (if any) to use pnpm**,
So that **consistency is maintained across the project.**

**Acceptance Criteria:**

**Given** the `backend/` directory (primarily Python, but may have Node scripts)
**When** I check for `package.json` files
**Then** if found, migrate them to `pnpm`
**And** if not found, mark this story as N/A.

**Note:** Backend is primarily Python. This story is a safety check.

---

### Story 1.4: Migrate MCP Server (TypeScript)

As a **MCP Developer**,
I want **the mcp-server project to use pnpm**,
So that **it benefits from faster installs and shared dependencies.**

**Acceptance Criteria:**

**Given** the `mcp-server/` directory with `package.json` and `package-lock.json`
**When** I run `pnpm install` in `mcp-server/`
**Then** a `pnpm-lock.yaml` is created
**And** `pnpm run build` compiles TypeScript successfully
**And** `node dist/index.js` starts the MCP server
**And** `package-lock.json` is deleted.

**Implementation Steps:**
1. `cd mcp-server`
2. `rm -rf node_modules package-lock.json`
3. `pnpm install`
4. `pnpm run build` (verify)
5. `node dist/index.js` (verify)
6. `git add pnpm-lock.yaml`
7. `git rm package-lock.json`

---

### Story 1.5: Configure pnpm Workspace (Monorepo)

As a **DevOps Engineer**,
I want **a `pnpm-workspace.yaml` file at the project root**,
So that **pnpm can manage all sub-projects as a unified workspace.**

**Acceptance Criteria:**

**Given** the project root directory
**When** I create `pnpm-workspace.yaml` with:
```yaml
packages:
  - 'frontend'
  - 'mcp-server'
```
**Then** running `pnpm install` at the root installs all dependencies for all workspaces
**And** shared dependencies are deduplicated via symlinks.

**Implementation:**
1. Create `pnpm-workspace.yaml` at project root
2. Run `pnpm install` at root
3. Verify `node_modules/.pnpm` contains shared packages

---

## Epic 2: CI/CD & Documentation Update

Update all automation and documentation to reflect the pnpm migration.

### Story 2.1: Update GitHub Actions Workflows

As a **CI/CD Engineer**,
I want **GitHub Actions to use pnpm**,
So that **CI builds are faster and consistent with local development.**

**Acceptance Criteria:**

**Given** `.github/workflows/*.yml` files that use `npm`
**When** I replace `npm ci` with `pnpm install --frozen-lockfile`
**And** replace `npm run build` with `pnpm run build`
**Then** CI pipelines pass successfully
**And** build times improve by at least 20%.

**Implementation:**
1. Find all `.github/workflows/*.yml` files
2. Replace:
   - `npm ci` → `pnpm install --frozen-lockfile`
   - `npm install` → `pnpm install`
   - `npm run X` → `pnpm run X`
3. Add pnpm setup step:
   ```yaml
   - name: Setup pnpm
     uses: pnpm/action-setup@v2
     with:
       version: 8
   ```

---

### Story 2.2: Update Docker Files

As a **DevOps Engineer**,
I want **Dockerfiles to use pnpm**,
So that **container builds are optimized.**

**Acceptance Criteria:**

**Given** `Dockerfile` or `docker-compose.yml` files that use `npm`
**When** I update them to use `pnpm`
**Then** `docker build` succeeds
**And** container size is reduced by at least 30%.

**Implementation:**
1. Update `Dockerfile`:
   ```dockerfile
   RUN npm install -g pnpm
   RUN pnpm install --frozen-lockfile
   ```
2. Test with `docker build -t opositaia-test .`

---

### Story 2.3: Update README and Setup Guides

As a **Documentation Maintainer**,
I want **all README files to reference pnpm**,
So that **new developers use the correct package manager.**

**Acceptance Criteria:**

**Given** `README.md`, `SETUP.md`, or similar files
**When** I replace all `npm install` references with `pnpm install`
**Then** the documentation is accurate and up-to-date.

**Files to Update:**
- `/README.md`
- `/frontend/README.md`
- `/mcp-server/README.md`
- Any setup guides in `/docs/`

---

### Story 2.4: Update VSCode Settings (Optional)

As a **Developer**,
I want **VSCode to recognize pnpm**,
So that **IntelliSense and task runners work correctly.**

**Acceptance Criteria:**

**Given** `.vscode/settings.json`
**When** I add:
```json
{
  "npm.packageManager": "pnpm"
}
```
**Then** VSCode uses `pnpm` for script execution.

---

## Verification Plan

### Automated Tests
- Run all existing test suites with `pnpm test`
- Verify CI/CD pipelines pass
- Check Docker builds complete successfully

### Manual Verification
- Developer onboarding test: Fresh clone → `pnpm install` → `pnpm run dev`
- Disk space check: Compare `node_modules` size before/after
- Performance benchmark: Measure `pnpm install` vs `npm install` time

### Rollback Plan
If issues arise:
1. Restore `package-lock.json` files from Git history
2. Run `npm install`
3. Revert commits related to pnpm migration

---

## Success Metrics

- ✅ All projects install dependencies with `pnpm install`
- ✅ All scripts (`dev`, `build`, `test`) work with `pnpm run`
- ✅ CI/CD pipelines pass
- ✅ Disk space reduced by 40%+
- ✅ Install time reduced by 30%+
- ✅ Documentation updated
