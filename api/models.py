from sqlalchemy import Column, String, DateTime, Text, DECIMAL, ForeignKey, Integer
from sqlalchemy.orm import relationship

if __package__:
    from .database import Base
else:
    from database import Base


class Project(Base):
    __tablename__ = "projects"

    project_id = Column(String(50), primary_key=True)
    project_name = Column(String(255))
    description = Column(Text)
    owner = Column(String(255))
    status = Column(String(50))
    priority = Column(String(50))
    repository_url = Column(String(500))
    created_date = Column(DateTime)
    last_updated = Column(DateTime)

    assets = relationship("Asset", back_populates="project")
    agents = relationship("Agent", back_populates="project")
    workflows = relationship("Workflow", back_populates="project")
    components = relationship("Component", back_populates="project")
    prompts = relationship("Prompt", back_populates="project")
    metrics = relationship("Metric", back_populates="project")
    dashboards = relationship("Dashboard", back_populates="project")
    knowledge_articles = relationship("KnowledgeArticle", back_populates="project")


class Asset(Base):
    __tablename__ = "assets"

    asset_id = Column(String(50), primary_key=True)
    project_id = Column(String(50), ForeignKey("projects.project_id"))
    asset_name = Column(String(255))
    asset_type = Column(String(100))
    owner = Column(String(255))
    status = Column(String(50))
    criticality = Column(String(50))
    technology = Column(String(100))
    environment = Column(String(50))
    created_date = Column(DateTime)
    last_updated = Column(DateTime)

    project = relationship("Project", back_populates="assets")


class Agent(Base):
    __tablename__ = "agents"

    agent_id = Column(String(50), primary_key=True)
    agent_name = Column(String(255))
    version = Column(String(50))
    owner = Column(String(255))
    project_id = Column(String(50), ForeignKey("projects.project_id"))
    status = Column(String(50))
    model_provider = Column(String(100))
    model_name = Column(String(100))
    purpose = Column(Text)
    created_date = Column(DateTime)
    last_updated = Column(DateTime)

    project = relationship("Project", back_populates="agents")


class Workflow(Base):
    __tablename__ = "workflows"

    workflow_id = Column(String(50), primary_key=True)
    workflow_name = Column(String(255))
    workflow_type = Column(String(100))
    project_id = Column(String(50), ForeignKey("projects.project_id"))
    owner = Column(String(255))
    status = Column(String(50))
    trigger_type = Column(String(100))
    technology = Column(String(100))
    created_date = Column(DateTime)
    last_updated = Column(DateTime)

    project = relationship("Project", back_populates="workflows")


class Component(Base):
    __tablename__ = "components"

    component_id = Column(String(50), primary_key=True)
    component_name = Column(String(255))
    component_type = Column(String(100))
    project_id = Column(String(50), ForeignKey("projects.project_id"))
    owner = Column(String(255))
    status = Column(String(50))
    technology = Column(String(100))
    repository_url = Column(String(500))
    created_date = Column(DateTime)
    last_updated = Column(DateTime)

    project = relationship("Project", back_populates="components")


class Prompt(Base):
    __tablename__ = "prompts"

    prompt_id = Column(String(50), primary_key=True)
    project_id = Column(String(50), ForeignKey("projects.project_id"))
    prompt_name = Column(String(255))
    prompt_type = Column(String(100))
    owner = Column(String(255))
    status = Column(String(50))
    version = Column(String(50))
    model_provider = Column(String(100))
    prompt_content = Column(Text)
    created_date = Column(DateTime)
    last_updated = Column(DateTime)

    project = relationship("Project", back_populates="prompts")


class Metric(Base):
    __tablename__ = "metrics"

    metric_id = Column(String(50), primary_key=True)
    project_id = Column(String(50), ForeignKey("projects.project_id"))
    metric_name = Column(String(255))
    metric_category = Column(String(100))
    metric_type = Column(String(100))
    owner = Column(String(255))
    target_value = Column(DECIMAL(18, 2))
    current_value = Column(DECIMAL(18, 2))
    status = Column(String(50))
    created_date = Column(DateTime)
    last_updated = Column(DateTime)

    project = relationship("Project", back_populates="metrics")


class Dashboard(Base):
    __tablename__ = "dashboards"

    dashboard_id = Column(String(50), primary_key=True)
    project_id = Column(String(50), ForeignKey("projects.project_id"))
    dashboard_name = Column(String(255))
    dashboard_type = Column(String(100))
    owner = Column(String(255))
    status = Column(String(50))
    technology = Column(String(100))
    dashboard_url = Column(String(500))
    created_date = Column(DateTime)
    last_updated = Column(DateTime)

    project = relationship("Project", back_populates="dashboards")


class KnowledgeArticle(Base):
    __tablename__ = "knowledge_articles"

    article_id = Column(String(50), primary_key=True)
    project_id = Column(String(50), ForeignKey("projects.project_id"))
    title = Column(String(255))
    category = Column(String(100))
    author = Column(String(255))
    status = Column(String(50))
    tags = Column(String(500))
    article_content = Column(Text)
    created_date = Column(DateTime)
    last_updated = Column(DateTime)

    project = relationship("Project", back_populates="knowledge_articles")


class AssetRelationship(Base):
    __tablename__ = "asset_relationships"

    relationship_id = Column(Integer, primary_key=True, autoincrement=True)
    source_asset_id = Column(String(50))
    source_asset_type = Column(String(100))
    target_asset_id = Column(String(50))
    target_asset_type = Column(String(100))
    relationship_type = Column(String(100))
    description = Column(Text)
    created_date = Column(DateTime)
    last_updated = Column(DateTime)
