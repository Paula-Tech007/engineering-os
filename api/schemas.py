from pydantic import BaseModel, field_validator
from typing import Optional
from decimal import Decimal


# ==========================================================
# VALIDATION HELPERS
# ==========================================================

def normalize_upper(value: Optional[str]) -> Optional[str]:
    if value is None:
        return value
    return value.strip().upper()


def validate_allowed(value: Optional[str], allowed_values: list[str], field_name: str) -> Optional[str]:
    if value is None:
        return value

    normalized_value = normalize_upper(value)

    if normalized_value not in allowed_values:
        allowed_text = ", ".join(allowed_values)
        raise ValueError(f"{field_name} must be one of: {allowed_text}")

    return normalized_value


# ==========================================================
# PROJECTS
# ==========================================================

class ProjectCreate(BaseModel):
    project_id: str
    project_name: str
    description: Optional[str] = None
    owner: Optional[str] = None
    status: str
    priority: Optional[str] = None
    repository_url: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        return validate_allowed(
            value,
            ["PLANNED", "ACTIVE", "ON_HOLD", "COMPLETED", "CANCELLED"],
            "Project status"
        )

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, value):
        return validate_allowed(
            value,
            ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
            "Project priority"
        )


class ProjectUpdate(BaseModel):
    project_name: Optional[str] = None
    description: Optional[str] = None
    owner: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    repository_url: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        return validate_allowed(
            value,
            ["PLANNED", "ACTIVE", "ON_HOLD", "COMPLETED", "CANCELLED"],
            "Project status"
        )

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, value):
        return validate_allowed(
            value,
            ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
            "Project priority"
        )


# ==========================================================
# ASSETS
# ==========================================================

class AssetCreate(BaseModel):
    asset_id: str
    project_id: Optional[str] = None
    asset_name: str
    asset_type: str
    owner: Optional[str] = None
    status: str
    criticality: Optional[str] = None
    technology: Optional[str] = None
    environment: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        return validate_allowed(
            value,
            ["ACTIVE", "INACTIVE", "DEPRECATED", "PLANNED"],
            "Asset status"
        )

    @field_validator("criticality")
    @classmethod
    def validate_criticality(cls, value):
        return validate_allowed(
            value,
            ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
            "Asset criticality"
        )

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, value):
        return validate_allowed(
            value,
            ["DEV", "TEST", "HML", "QA", "PROD", "LOCAL", "CLOUD"],
            "Asset environment"
        )


class AssetUpdate(BaseModel):
    project_id: Optional[str] = None
    asset_name: Optional[str] = None
    asset_type: Optional[str] = None
    owner: Optional[str] = None
    status: Optional[str] = None
    criticality: Optional[str] = None
    technology: Optional[str] = None
    environment: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        return validate_allowed(
            value,
            ["ACTIVE", "INACTIVE", "DEPRECATED", "PLANNED"],
            "Asset status"
        )

    @field_validator("criticality")
    @classmethod
    def validate_criticality(cls, value):
        return validate_allowed(
            value,
            ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
            "Asset criticality"
        )

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, value):
        return validate_allowed(
            value,
            ["DEV", "TEST", "HML", "QA", "PROD", "LOCAL", "CLOUD"],
            "Asset environment"
        )


# ==========================================================
# AGENTS
# ==========================================================

class AgentCreate(BaseModel):
    agent_id: str
    agent_name: str
    version: Optional[str] = None
    owner: Optional[str] = None
    project_id: Optional[str] = None
    status: str
    model_provider: Optional[str] = None
    model_name: Optional[str] = None
    purpose: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        return validate_allowed(
            value,
            ["ACTIVE", "INACTIVE", "DEPRECATED"],
            "Agent status"
        )


class AgentUpdate(BaseModel):
    agent_name: Optional[str] = None
    version: Optional[str] = None
    owner: Optional[str] = None
    project_id: Optional[str] = None
    status: Optional[str] = None
    model_provider: Optional[str] = None
    model_name: Optional[str] = None
    purpose: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        return validate_allowed(
            value,
            ["ACTIVE", "INACTIVE", "DEPRECATED"],
            "Agent status"
        )


# ==========================================================
# WORKFLOWS
# ==========================================================

class WorkflowCreate(BaseModel):
    workflow_id: str
    workflow_name: str
    workflow_type: Optional[str] = None
    project_id: Optional[str] = None
    owner: Optional[str] = None
    status: str
    trigger_type: Optional[str] = None
    technology: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        return validate_allowed(
            value,
            ["ACTIVE", "DISABLED", "TESTING", "PLANNED"],
            "Workflow status"
        )


class WorkflowUpdate(BaseModel):
    workflow_name: Optional[str] = None
    workflow_type: Optional[str] = None
    project_id: Optional[str] = None
    owner: Optional[str] = None
    status: Optional[str] = None
    trigger_type: Optional[str] = None
    technology: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        return validate_allowed(
            value,
            ["ACTIVE", "DISABLED", "TESTING", "PLANNED"],
            "Workflow status"
        )


# ==========================================================
# COMPONENTS
# ==========================================================

class ComponentCreate(BaseModel):
    component_id: str
    component_name: str
    component_type: Optional[str] = None
    project_id: Optional[str] = None
    owner: Optional[str] = None
    status: str
    technology: Optional[str] = None
    repository_url: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        return validate_allowed(
            value,
            ["ACTIVE", "INACTIVE", "DEPRECATED", "PLANNED"],
            "Component status"
        )


class ComponentUpdate(BaseModel):
    component_name: Optional[str] = None
    component_type: Optional[str] = None
    project_id: Optional[str] = None
    owner: Optional[str] = None
    status: Optional[str] = None
    technology: Optional[str] = None
    repository_url: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        return validate_allowed(
            value,
            ["ACTIVE", "INACTIVE", "DEPRECATED", "PLANNED"],
            "Component status"
        )


# ==========================================================
# PROMPTS
# ==========================================================

class PromptCreate(BaseModel):
    prompt_id: str
    project_id: Optional[str] = None
    prompt_name: str
    prompt_type: Optional[str] = None
    owner: Optional[str] = None
    status: str
    version: Optional[str] = None
    model_provider: Optional[str] = None
    prompt_content: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        return validate_allowed(
            value,
            ["ACTIVE", "INACTIVE", "DEPRECATED", "DRAFT"],
            "Prompt status"
        )


class PromptUpdate(BaseModel):
    project_id: Optional[str] = None
    prompt_name: Optional[str] = None
    prompt_type: Optional[str] = None
    owner: Optional[str] = None
    status: Optional[str] = None
    version: Optional[str] = None
    model_provider: Optional[str] = None
    prompt_content: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        return validate_allowed(
            value,
            ["ACTIVE", "INACTIVE", "DEPRECATED", "DRAFT"],
            "Prompt status"
        )


# ==========================================================
# METRICS
# ==========================================================

class MetricCreate(BaseModel):
    metric_id: str
    project_id: Optional[str] = None
    metric_name: str
    metric_category: Optional[str] = None
    metric_type: Optional[str] = None
    owner: Optional[str] = None
    target_value: Optional[Decimal] = None
    current_value: Optional[Decimal] = None
    status: str

    @field_validator("target_value", "current_value")
    @classmethod
    def validate_metric_value(cls, value):
        if value is not None and value < 0:
            raise ValueError("Metric values must be greater than or equal to zero")
        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        return validate_allowed(
            value,
            ["ACTIVE", "INACTIVE", "TRACKING", "ARCHIVED"],
            "Metric status"
        )


class MetricUpdate(BaseModel):
    project_id: Optional[str] = None
    metric_name: Optional[str] = None
    metric_category: Optional[str] = None
    metric_type: Optional[str] = None
    owner: Optional[str] = None
    target_value: Optional[Decimal] = None
    current_value: Optional[Decimal] = None
    status: Optional[str] = None

    @field_validator("target_value", "current_value")
    @classmethod
    def validate_metric_value(cls, value):
        if value is not None and value < 0:
            raise ValueError("Metric values must be greater than or equal to zero")
        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        return validate_allowed(
            value,
            ["ACTIVE", "INACTIVE", "TRACKING", "ARCHIVED"],
            "Metric status"
        )


# ==========================================================
# DASHBOARDS
# ==========================================================

class DashboardCreate(BaseModel):
    dashboard_id: str
    project_id: Optional[str] = None
    dashboard_name: str
    dashboard_type: Optional[str] = None
    owner: Optional[str] = None
    status: str
    technology: Optional[str] = None
    dashboard_url: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        return validate_allowed(
            value,
            ["ACTIVE", "INACTIVE", "PLANNED", "DEPRECATED"],
            "Dashboard status"
        )


class DashboardUpdate(BaseModel):
    project_id: Optional[str] = None
    dashboard_name: Optional[str] = None
    dashboard_type: Optional[str] = None
    owner: Optional[str] = None
    status: Optional[str] = None
    technology: Optional[str] = None
    dashboard_url: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        return validate_allowed(
            value,
            ["ACTIVE", "INACTIVE", "PLANNED", "DEPRECATED"],
            "Dashboard status"
        )


# ==========================================================
# KNOWLEDGE ARTICLES
# ==========================================================

class KnowledgeArticleCreate(BaseModel):
    article_id: str
    project_id: Optional[str] = None
    title: str
    category: Optional[str] = None
    author: Optional[str] = None
    status: str
    tags: Optional[str] = None
    article_content: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        return validate_allowed(
            value,
            ["DRAFT", "PUBLISHED", "ARCHIVED", "REVIEW"],
            "Knowledge article status"
        )


class KnowledgeArticleUpdate(BaseModel):
    project_id: Optional[str] = None
    title: Optional[str] = None
    category: Optional[str] = None
    author: Optional[str] = None
    status: Optional[str] = None
    tags: Optional[str] = None
    article_content: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        return validate_allowed(
            value,
            ["DRAFT", "PUBLISHED", "ARCHIVED", "REVIEW"],
            "Knowledge article status"
        )


# ==========================================================
# ASSET RELATIONSHIPS
# ==========================================================

class AssetRelationshipCreate(BaseModel):
    source_asset_id: str
    source_asset_type: str
    target_asset_id: str
    target_asset_type: str
    relationship_type: str
    description: Optional[str] = None

    @field_validator("source_asset_type", "target_asset_type")
    @classmethod
    def validate_asset_type(cls, value):
        return validate_allowed(
            value,
            [
                "PROJECT",
                "ASSET",
                "AGENT",
                "WORKFLOW",
                "COMPONENT",
                "PROMPT",
                "METRIC",
                "DASHBOARD",
                "KNOWLEDGE_ARTICLE",
            ],
            "Asset type"
        )

    @field_validator("relationship_type")
    @classmethod
    def validate_relationship_type(cls, value):
        return validate_allowed(
            value,
            [
                "DEPENDS_ON",
                "USES",
                "OWNS",
                "TRIGGERS",
                "PRODUCES",
                "MONITORS",
                "DOCUMENTS",
                "RELATED_TO",
            ],
            "Relationship type"
        )


class AssetRelationshipUpdate(BaseModel):
    source_asset_id: Optional[str] = None
    source_asset_type: Optional[str] = None
    target_asset_id: Optional[str] = None
    target_asset_type: Optional[str] = None
    relationship_type: Optional[str] = None
    description: Optional[str] = None

    @field_validator("source_asset_type", "target_asset_type")
    @classmethod
    def validate_asset_type(cls, value):
        return validate_allowed(
            value,
            [
                "PROJECT",
                "ASSET",
                "AGENT",
                "WORKFLOW",
                "COMPONENT",
                "PROMPT",
                "METRIC",
                "DASHBOARD",
                "KNOWLEDGE_ARTICLE",
            ],
            "Asset type"
        )

    @field_validator("relationship_type")
    @classmethod
    def validate_relationship_type(cls, value):
        return validate_allowed(
            value,
            [
                "DEPENDS_ON",
                "USES",
                "OWNS",
                "TRIGGERS",
                "PRODUCES",
                "MONITORS",
                "DOCUMENTS",
                "RELATED_TO",
            ],
            "Relationship type"
        )
