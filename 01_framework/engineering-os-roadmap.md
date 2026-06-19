# Engineering OS Roadmap

## Purpose

Define the implementation roadmap for Engineering OS.

This roadmap organizes the project into clear phases, from foundation to automation, dashboards and AI-powered search.

---

# Current Status

## Completed

- Repository structure
- GitHub integration
- Governance model
- Asset register
- ID standards
- Technology catalog
- Workflow catalog
- Component catalog
- Agent catalog
- Project catalog
- Prompt catalog
- First project registration
- First workflow registration
- First agent registration
- Logical database model
- Physical database model
- Initial seed data
- API layer for core catalog entities
- Global search endpoint
- Consolidated inventory endpoint
- Governance KPI endpoint
- Standard API response contract
- Automated API contract tests
- Asset relationship API
- Direct impact analysis endpoint
- SQL physical model aligned with API models

---

# MVP Scope

The MVP must focus on making Engineering OS usable with the smallest possible implementation.

## MVP Goals

- Store assets in MariaDB
- Register projects
- Register workflows
- Register agents
- Register components
- Search assets by ID
- Search assets by name
- Search assets by type
- Show asset relationships

---

# Phase 1 - Foundation

Status:
Completed

Deliverables:

- Repository
- Governance
- Catalogs
- Templates
- Initial assets

---

# Phase 2 - Database

Status:
Completed

Deliverables:

- Logical model
- Physical model
- Seed data

---

# Phase 3 - Local Database Execution

Status:
Completed

Deliverables:

- Create MariaDB database
- Execute physical model SQL
- Execute seed data SQL
- Validate tables
- Validate initial records
- External database URL configuration

---

# Phase 4 - Search Engine MVP

Status:
Completed

Deliverables:

- Asset search by ID
- Asset search by name
- Asset search by type
- Relationship lookup
- Impact analysis query
- Global text search across projects, assets, agents, workflows, components, prompts, metrics, dashboards and knowledge articles

---

# Phase 5 - n8n Integration

Status:
Future

Deliverables:

- n8n workflow for asset search
- n8n workflow for impact analysis
- n8n workflow for asset registration
- n8n workflow for governance review

---

# Phase 6 - API Layer

Status:
Completed

Deliverables:

- Asset API
- Project API
- Workflow API
- Agent API
- Relationship API
- Component API
- Prompt API
- Metric API
- Dashboard API
- Knowledge article API
- Standard success and list responses
- Pydantic schema validation

---

# Phase 7 - Dashboard

Status:
Completed

Deliverables:

- Executive dashboard
- Governance dashboard
- Asset coverage dashboard
- Reuse dashboard
- Dashboard summary API
- Governance KPI API

---

# Phase 8 - AI Search

Status:
Future

Deliverables:

- Embeddings
- Semantic search
- AI assistant
- Reuse recommendations
- Impact analysis assistant

---

# Implementation Order

1. Local MariaDB execution - Completed
2. SQL validation - Completed
3. Search queries - Completed
4. API - Completed
5. Dashboard and governance summary APIs - Completed
6. n8n workflows - Future
7. AI semantic search - Future

---

# Success Criteria

Engineering OS MVP is successful when:

- Database is created successfully
- Initial records are inserted
- Assets can be searched
- Relationships can be queried
- API can retrieve catalog and inventory information
- Governance KPIs can be retrieved
- API contract tests pass locally
- Governance assets are versioned in GitHub

---

# Risks

| Risk | Mitigation |
|------|------------|
| Documentation not matching database | Keep SQL and Markdown synchronized |
| Catalogs becoming outdated | Governance review cycle |
| n8n workflows depending on incomplete data | Validate seed data first |
| Scope expansion | Respect MVP boundaries |

---

# Change History

| Date | Author | Change |
|------|--------|--------|
| 2026-06-10 | Paula Sabino | Initial roadmap |
| 2026-06-19 | Paula Sabino | MVP API, search, inventory and governance KPIs completed |
