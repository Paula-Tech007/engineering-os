# Engineering OS - Logical Data Model

## Purpose

Logical data model for Engineering OS.

This model defines the core entities used to manage governance, cataloging, inventory, discovery and reuse of engineering assets.

---

# Core Entities

## Projects

Table:
projects

Primary Key:
project_id

Purpose:
Central project registry.

Key fields:
project_name, description, owner, status, priority, repository_url

---

## Assets

Table:
assets

Primary Key:
asset_id

Relationship:
Many Assets to One Project

Key fields:
asset_name, asset_type, owner, status, criticality, technology, environment

---

## Workflows

Table:
workflows

Primary Key:
workflow_id

Relationship:
Many Workflows to One Project

Key fields:
workflow_name, workflow_type, owner, status, trigger_type, technology

---

## Agents

Table:
agents

Primary Key:
agent_id

Relationship:
Many Agents to One Project

Key fields:
agent_name, version, owner, status, model_provider, model_name, purpose

---

## Components

Table:
components

Primary Key:
component_id

Relationship:
Many Components to One Project

Key fields:
component_name, component_type, owner, status, technology, repository_url

---

## Prompts

Table:
prompts

Primary Key:
prompt_id

Relationship:
Many Prompts to One Project

Key fields:
prompt_name, prompt_type, owner, status, version, model_provider, prompt_content

---

## Metrics

Table:
metrics

Primary Key:
metric_id

Relationship:
Many Metrics to One Project

Key fields:
metric_name, metric_category, metric_type, owner, target_value, current_value, status

---

## Dashboards

Table:
dashboards

Primary Key:
dashboard_id

Relationship:
Many Dashboards to One Project

Key fields:
dashboard_name, dashboard_type, owner, status, technology, dashboard_url

---

## Knowledge Articles

Table:
knowledge_articles

Primary Key:
article_id

Relationship:
Many Knowledge Articles to One Project

Key fields:
title, category, author, status, tags, article_content

---

## Asset Relationships

Table:
asset_relationships

Primary Key:
relationship_id

Purpose:
Generic directed relationship graph across Engineering OS entities.

Key fields:
source_asset_id, source_asset_type, target_asset_id, target_asset_type, relationship_type, description

---

# Relationship Overview

projects
    |-- assets
    |-- workflows
    |-- agents
    |-- components
    |-- prompts
    |-- metrics
    |-- dashboards
    |-- knowledge_articles

asset_relationships connects any source entity to any target entity using a directed relationship type.

---

# Database Engine

MariaDB

---

# Version

1.0.0

---

# Change History

| Date | Author | Change |
|------|--------|--------|
| 2026-06-10 | Paula Sabino | Initial logical model |
| 2026-06-19 | Paula Sabino | Aligned model with MVP API entities and relationship graph |
