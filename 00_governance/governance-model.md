# Governance Model

## Purpose

Define the standards, rules and governance process for all Engineering OS assets.

---

# Asset Lifecycle

Every asset must follow the lifecycle below:

Draft → Review → Active → Deprecated → Archived

---

# Asset Registration Rules

All assets must be registered in:

```text
00_governance/asset-register.md
```

before being considered active.

---

# Naming Standards

## Projects

```text
PRJ-XXXX
```

Example:

```text
PRJ-0001 Engineering OS
```

---

## Workflows

```text
WF-XXXX
```

Example:

```text
WF-0001 Alert Processing Workflow
```

---

## Agents

```text
AGENT-XXXX
```

Example:

```text
AGENT-0001 SOC Analyst Agent
```

---

## Components

```text
COMPONENT-XXXX
```

Example:

```text
COMPONENT-0001 Alert Enricher
```

---

## Knowledge Articles

```text
KB-XXXX
```

Example:

```text
KB-0001 Redis Troubleshooting
```

---

# Versioning

Format:

```text
Major.Minor
```

Examples:

```text
1.0
1.1
1.2
2.0
```

Rules:

* Major = significant changes
* Minor = incremental improvements

---

# Repository Structure

```text
00_governance
01_framework
02_catalogs
03_projects
04_knowledge
05_components
06_patterns
07_workflows
08_agents
09_prompts
10_metrics
11_database
12_n8n
13_api
14_dashboards
15_templates
99_archive
```

---

# Documentation Requirements

Every Project must have:

* Project Template

Every Workflow must have:

* Workflow Template

Every Agent must have:

* Agent Template

Every Component must have:

* Component Template

---

# Change Control

Every change must follow:

1. Update file
2. Save file
3. Git Add
4. Git Commit
5. Git Push
6. Validate using Git Status

---

# Ownership

Repository Owner:

Paula Sabino

---

# Review Cycle

Governance review frequency:

Quarterly

---

# Change History

| Date       | Author       | Description              |
| ---------- | ------------ | ------------------------ |
| 2026-06-10 | Paula Sabino | Initial Governance Model |
