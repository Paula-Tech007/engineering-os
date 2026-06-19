from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text, or_
from sqlalchemy.orm import Session

if __package__:
    from .database import SessionLocal
    from .response_utils import success_response, list_response
    from .models import (
        Asset,
        Project,
        Agent,
        Workflow,
        Component,
        Prompt,
        Metric,
        Dashboard,
        KnowledgeArticle,
        AssetRelationship,
    )
    from .schemas import (
        ProjectCreate,
        ProjectUpdate,
        AssetCreate,
        AssetUpdate,
        AgentCreate,
        AgentUpdate,
        WorkflowCreate,
        WorkflowUpdate,
        ComponentCreate,
        ComponentUpdate,
        PromptCreate,
        PromptUpdate,
        MetricCreate,
        MetricUpdate,
        DashboardCreate,
        DashboardUpdate,
        KnowledgeArticleCreate,
        KnowledgeArticleUpdate,
        AssetRelationshipCreate,
        AssetRelationshipUpdate,
    )
else:
    from database import SessionLocal
    from response_utils import success_response, list_response
    from models import (
        Asset,
        Project,
        Agent,
        Workflow,
        Component,
        Prompt,
        Metric,
        Dashboard,
        KnowledgeArticle,
        AssetRelationship,
    )
    from schemas import (
        ProjectCreate,
        ProjectUpdate,
        AssetCreate,
        AssetUpdate,
        AgentCreate,
        AgentUpdate,
        WorkflowCreate,
        WorkflowUpdate,
        ComponentCreate,
        ComponentUpdate,
        PromptCreate,
        PromptUpdate,
        MetricCreate,
        MetricUpdate,
        DashboardCreate,
        DashboardUpdate,
        KnowledgeArticleCreate,
        KnowledgeArticleUpdate,
        AssetRelationshipCreate,
        AssetRelationshipUpdate,
    )


app = FastAPI(
    title="Engineering OS API",
    version="1.0.0"
)

BASE_DIR = Path(__file__).resolve().parent.parent
WEB_DIR = BASE_DIR / "web"
DASHBOARD_FILE = WEB_DIR / "dashboard.html"
DASHBOARD_ASSETS_DIR = WEB_DIR / "assets"

app.mount(
    "/dashboard-assets",
    StaticFiles(directory=DASHBOARD_ASSETS_DIR),
    name="dashboard-assets"
)


# ==========================================================
# DATABASE SESSION
# ==========================================================

def get_db():
    db: Session = SessionLocal()
    return db


# ==========================================================
# HELPERS
# ==========================================================

def now():
    return datetime.now()


def schema_to_dict(schema, exclude_unset: bool = False):
    if hasattr(schema, "model_dump"):
        return schema.model_dump(exclude_unset=exclude_unset)

    return schema.dict(exclude_unset=exclude_unset)


def get_record_or_404(db, model, id_field, id_value, not_found_message):
    record = db.query(model).filter(
        getattr(model, id_field) == id_value
    ).first()

    if record is None:
        raise HTTPException(
            status_code=404,
            detail=not_found_message
        )

    return record


def commit_or_rollback(db):
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise


def create_record(db, model, id_field, schema_data, already_exists_message, success_message, response_key):
    data = schema_to_dict(schema_data)

    existing_record = db.query(model).filter(
        getattr(model, id_field) == data[id_field]
    ).first()

    if existing_record is not None:
        raise HTTPException(
            status_code=400,
            detail=already_exists_message
        )

    new_record = model(
        **data,
        created_date=now(),
        last_updated=now()
    )

    db.add(new_record)
    commit_or_rollback(db)
    db.refresh(new_record)

    return success_response(
        message=success_message,
        data={
            response_key: new_record
        }
    )


def update_record(db, model, id_field, id_value, schema_data, not_found_message, success_message, response_key):
    record = get_record_or_404(
        db=db,
        model=model,
        id_field=id_field,
        id_value=id_value,
        not_found_message=not_found_message
    )

    update_data = schema_to_dict(
        schema_data,
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(record, field, value)

    record.last_updated = now()

    commit_or_rollback(db)
    db.refresh(record)

    return success_response(
        message=success_message,
        data={
            response_key: record
        }
    )


def delete_record(db, model, id_field, id_value, not_found_message, success_message):
    record = get_record_or_404(
        db=db,
        model=model,
        id_field=id_field,
        id_value=id_value,
        not_found_message=not_found_message
    )

    db.delete(record)
    commit_or_rollback(db)

    return success_response(
        message=success_message,
        data={
            id_field: id_value
        }
    )


def query_relationships_for_asset(db, asset_id: str, direction: str):
    if direction == "outgoing":
        return db.query(AssetRelationship).filter(
            AssetRelationship.source_asset_id == asset_id
        ).all()

    if direction == "incoming":
        return db.query(AssetRelationship).filter(
            AssetRelationship.target_asset_id == asset_id
        ).all()

    return db.query(AssetRelationship).filter(
        or_(
            AssetRelationship.source_asset_id == asset_id,
            AssetRelationship.target_asset_id == asset_id
        )
    ).all()


def validate_relationship_direction(direction: str):
    if direction not in {"all", "incoming", "outgoing"}:
        raise HTTPException(
            status_code=400,
            detail="direction must be one of: all, incoming, outgoing"
        )


# ==========================================================
# SYSTEM
# ==========================================================

@app.get("/", tags=["System"])
def home():
    return success_response(
        message="Engineering OS API is running",
        data={
            "platform": "Engineering OS",
            "status": "running",
            "version": "1.0.0"
        }
    )


@app.get("/health", tags=["System"])
def health_check():
    db = get_db()

    try:
        db.execute(text("SELECT 1"))

        return success_response(
            message="Health check completed successfully",
            data={
                "status": "healthy",
                "database": "connected"
            }
        )

    finally:
        db.close()


# ==========================================================
# DASHBOARD SUMMARY
# ==========================================================

@app.get("/dashboard", tags=["Dashboards"], response_class=HTMLResponse)
def dashboard_ui():
    return DASHBOARD_FILE.read_text(encoding="utf-8")


@app.get("/dashboard/summary", tags=["Dashboards"])
def dashboard_summary():
    db = get_db()

    try:
        summary = {
            "total_projects": db.query(Project).count(),
            "total_assets": db.query(Asset).count(),
            "total_agents": db.query(Agent).count(),
            "total_workflows": db.query(Workflow).count(),
            "total_components": db.query(Component).count(),
            "total_prompts": db.query(Prompt).count(),
            "total_metrics": db.query(Metric).count(),
            "total_dashboards": db.query(Dashboard).count(),
            "total_knowledge_articles": db.query(KnowledgeArticle).count(),
            "total_relationships": db.query(AssetRelationship).count()
        }

        return success_response(
            message="Dashboard summary retrieved successfully",
            data=summary
        )

    finally:
        db.close()


# ==========================================================
# ASSETS
# ==========================================================

@app.get("/assets", tags=["Assets"])
def get_assets():
    db = get_db()

    try:
        assets = db.query(Asset).all()
        return list_response(
            message="Assets retrieved successfully",
            items=assets
        )

    finally:
        db.close()


@app.get("/assets/{asset_id}", tags=["Assets"])
def get_asset_by_id(asset_id: str):
    db = get_db()

    try:
        asset = get_record_or_404(
            db=db,
            model=Asset,
            id_field="asset_id",
            id_value=asset_id,
            not_found_message="Asset not found"
        )

        return success_response(
            message="Asset retrieved successfully",
            data={"asset": asset}
        )

    finally:
        db.close()


@app.post("/assets", tags=["Assets"])
def create_asset(asset_data: AssetCreate):
    db = get_db()

    try:
        return create_record(
            db=db,
            model=Asset,
            id_field="asset_id",
            schema_data=asset_data,
            already_exists_message="Asset already exists",
            success_message="Asset created successfully",
            response_key="asset"
        )

    finally:
        db.close()


@app.put("/assets/{asset_id}", tags=["Assets"])
def update_asset(asset_id: str, asset_data: AssetUpdate):
    db = get_db()

    try:
        return update_record(
            db=db,
            model=Asset,
            id_field="asset_id",
            id_value=asset_id,
            schema_data=asset_data,
            not_found_message="Asset not found",
            success_message="Asset updated successfully",
            response_key="asset"
        )

    finally:
        db.close()


@app.delete("/assets/{asset_id}", tags=["Assets"])
def delete_asset(asset_id: str):
    db = get_db()

    try:
        return delete_record(
            db=db,
            model=Asset,
            id_field="asset_id",
            id_value=asset_id,
            not_found_message="Asset not found",
            success_message="Asset deleted successfully"
        )

    finally:
        db.close()


# ==========================================================
# ASSET RELATIONSHIPS
# ==========================================================

@app.get("/relationships", tags=["Relationships"])
def get_relationships():
    db = get_db()

    try:
        relationships = db.query(AssetRelationship).all()
        return list_response(
            message="Asset relationships retrieved successfully",
            items=relationships
        )

    finally:
        db.close()


@app.get("/relationships/{relationship_id}", tags=["Relationships"])
def get_relationship_by_id(relationship_id: int):
    db = get_db()

    try:
        relationship = get_record_or_404(
            db=db,
            model=AssetRelationship,
            id_field="relationship_id",
            id_value=relationship_id,
            not_found_message="Asset relationship not found"
        )

        return success_response(
            message="Asset relationship retrieved successfully",
            data={"relationship": relationship}
        )

    finally:
        db.close()


@app.post("/relationships", tags=["Relationships"])
def create_relationship(relationship_data: AssetRelationshipCreate):
    db = get_db()

    try:
        data = schema_to_dict(relationship_data)
        relationship = AssetRelationship(
            **data,
            created_date=now(),
            last_updated=now()
        )

        db.add(relationship)
        commit_or_rollback(db)
        db.refresh(relationship)

        return success_response(
            message="Asset relationship created successfully",
            data={"relationship": relationship}
        )

    finally:
        db.close()


@app.put("/relationships/{relationship_id}", tags=["Relationships"])
def update_relationship(relationship_id: int, relationship_data: AssetRelationshipUpdate):
    db = get_db()

    try:
        return update_record(
            db=db,
            model=AssetRelationship,
            id_field="relationship_id",
            id_value=relationship_id,
            schema_data=relationship_data,
            not_found_message="Asset relationship not found",
            success_message="Asset relationship updated successfully",
            response_key="relationship"
        )

    finally:
        db.close()


@app.delete("/relationships/{relationship_id}", tags=["Relationships"])
def delete_relationship(relationship_id: int):
    db = get_db()

    try:
        return delete_record(
            db=db,
            model=AssetRelationship,
            id_field="relationship_id",
            id_value=relationship_id,
            not_found_message="Asset relationship not found",
            success_message="Asset relationship deleted successfully"
        )

    finally:
        db.close()


@app.get("/assets/{asset_id}/relationships", tags=["Relationships"])
def get_asset_relationships(asset_id: str, direction: str = "all"):
    validate_relationship_direction(direction)
    db = get_db()

    try:
        get_record_or_404(
            db=db,
            model=Asset,
            id_field="asset_id",
            id_value=asset_id,
            not_found_message="Asset not found"
        )

        relationships = query_relationships_for_asset(
            db=db,
            asset_id=asset_id,
            direction=direction
        )

        return list_response(
            message="Asset relationships retrieved successfully",
            items=relationships
        )

    finally:
        db.close()


@app.get("/assets/{asset_id}/impact", tags=["Relationships"])
def get_asset_impact(asset_id: str):
    db = get_db()

    try:
        asset = get_record_or_404(
            db=db,
            model=Asset,
            id_field="asset_id",
            id_value=asset_id,
            not_found_message="Asset not found"
        )

        outgoing_relationships = query_relationships_for_asset(
            db=db,
            asset_id=asset_id,
            direction="outgoing"
        )
        incoming_relationships = query_relationships_for_asset(
            db=db,
            asset_id=asset_id,
            direction="incoming"
        )

        impact = {
            "asset": asset,
            "direct_dependencies": outgoing_relationships,
            "direct_dependents": incoming_relationships,
            "summary": {
                "direct_dependencies": len(outgoing_relationships),
                "direct_dependents": len(incoming_relationships),
                "total_direct_relationships": (
                    len(outgoing_relationships) + len(incoming_relationships)
                )
            }
        }

        return success_response(
            message="Asset impact analysis retrieved successfully",
            data=impact
        )

    finally:
        db.close()


# ==========================================================
# PROJECTS
# ==========================================================

@app.get("/projects", tags=["Projects"])
def get_projects():
    db = get_db()

    try:
        projects = db.query(Project).all()
        return list_response(
            message="Projects retrieved successfully",
            items=projects
        )

    finally:
        db.close()


@app.get("/projects/{project_id}", tags=["Projects"])
def get_project_by_id(project_id: str):
    db = get_db()

    try:
        project = get_record_or_404(
            db=db,
            model=Project,
            id_field="project_id",
            id_value=project_id,
            not_found_message="Project not found"
        )

        return success_response(
            message="Project retrieved successfully",
            data={"project": project}
        )

    finally:
        db.close()


@app.post("/projects", tags=["Projects"])
def create_project(project_data: ProjectCreate):
    db = get_db()

    try:
        return create_record(
            db=db,
            model=Project,
            id_field="project_id",
            schema_data=project_data,
            already_exists_message="Project already exists",
            success_message="Project created successfully",
            response_key="project"
        )

    finally:
        db.close()


@app.put("/projects/{project_id}", tags=["Projects"])
def update_project(project_id: str, project_data: ProjectUpdate):
    db = get_db()

    try:
        return update_record(
            db=db,
            model=Project,
            id_field="project_id",
            id_value=project_id,
            schema_data=project_data,
            not_found_message="Project not found",
            success_message="Project updated successfully",
            response_key="project"
        )

    finally:
        db.close()


@app.delete("/projects/{project_id}", tags=["Projects"])
def delete_project(project_id: str):
    db = get_db()

    try:
        return delete_record(
            db=db,
            model=Project,
            id_field="project_id",
            id_value=project_id,
            not_found_message="Project not found",
            success_message="Project deleted successfully"
        )

    finally:
        db.close()


@app.get("/projects/{project_id}/inventory", tags=["Projects"])
def get_project_inventory(project_id: str):
    db = get_db()

    try:
        project = get_record_or_404(
            db=db,
            model=Project,
            id_field="project_id",
            id_value=project_id,
            not_found_message="Project not found"
        )

        project_asset_ids = [
            asset.asset_id
            for asset in db.query(Asset).filter(Asset.project_id == project_id).all()
        ]
        project_entity_ids = [project_id] + project_asset_ids

        inventory = {
            "project": {
                "project_id": project.project_id,
                "project_name": project.project_name,
                "description": project.description,
                "owner": project.owner,
                "status": project.status,
                "priority": project.priority,
                "repository_url": project.repository_url,
                "created_date": project.created_date,
                "last_updated": project.last_updated
            },
            "assets": db.query(Asset).filter(Asset.project_id == project_id).all(),
            "agents": db.query(Agent).filter(Agent.project_id == project_id).all(),
            "workflows": db.query(Workflow).filter(Workflow.project_id == project_id).all(),
            "components": db.query(Component).filter(Component.project_id == project_id).all(),
            "prompts": db.query(Prompt).filter(Prompt.project_id == project_id).all(),
            "metrics": db.query(Metric).filter(Metric.project_id == project_id).all(),
            "dashboards": db.query(Dashboard).filter(Dashboard.project_id == project_id).all(),
            "knowledge_articles": db.query(KnowledgeArticle).filter(
                KnowledgeArticle.project_id == project_id
            ).all(),
            "relationships": db.query(AssetRelationship).filter(
                or_(
                    AssetRelationship.source_asset_id.in_(project_entity_ids),
                    AssetRelationship.target_asset_id.in_(project_entity_ids)
                )
            ).all()
        }

        return success_response(
            message="Project inventory retrieved successfully",
            data=inventory
        )

    finally:
        db.close()


# ==========================================================
# AGENTS
# ==========================================================

@app.get("/agents", tags=["Agents"])
def get_agents():
    db = get_db()

    try:
        agents = db.query(Agent).all()
        return list_response(
            message="Agents retrieved successfully",
            items=agents
        )

    finally:
        db.close()


@app.get("/agents/{agent_id}", tags=["Agents"])
def get_agent_by_id(agent_id: str):
    db = get_db()

    try:
        agent = get_record_or_404(
            db=db,
            model=Agent,
            id_field="agent_id",
            id_value=agent_id,
            not_found_message="Agent not found"
        )

        return success_response(
            message="Agent retrieved successfully",
            data={"agent": agent}
        )

    finally:
        db.close()


@app.post("/agents", tags=["Agents"])
def create_agent(agent_data: AgentCreate):
    db = get_db()

    try:
        return create_record(
            db=db,
            model=Agent,
            id_field="agent_id",
            schema_data=agent_data,
            already_exists_message="Agent already exists",
            success_message="Agent created successfully",
            response_key="agent"
        )

    finally:
        db.close()


@app.put("/agents/{agent_id}", tags=["Agents"])
def update_agent(agent_id: str, agent_data: AgentUpdate):
    db = get_db()

    try:
        return update_record(
            db=db,
            model=Agent,
            id_field="agent_id",
            id_value=agent_id,
            schema_data=agent_data,
            not_found_message="Agent not found",
            success_message="Agent updated successfully",
            response_key="agent"
        )

    finally:
        db.close()


@app.delete("/agents/{agent_id}", tags=["Agents"])
def delete_agent(agent_id: str):
    db = get_db()

    try:
        return delete_record(
            db=db,
            model=Agent,
            id_field="agent_id",
            id_value=agent_id,
            not_found_message="Agent not found",
            success_message="Agent deleted successfully"
        )

    finally:
        db.close()


# ==========================================================
# WORKFLOWS
# ==========================================================

@app.get("/workflows", tags=["Workflows"])
def get_workflows():
    db = get_db()

    try:
        workflows = db.query(Workflow).all()
        return list_response(
            message="Workflows retrieved successfully",
            items=workflows
        )

    finally:
        db.close()


@app.get("/workflows/{workflow_id}", tags=["Workflows"])
def get_workflow_by_id(workflow_id: str):
    db = get_db()

    try:
        workflow = get_record_or_404(
            db=db,
            model=Workflow,
            id_field="workflow_id",
            id_value=workflow_id,
            not_found_message="Workflow not found"
        )

        return success_response(
            message="Workflow retrieved successfully",
            data={"workflow": workflow}
        )

    finally:
        db.close()


@app.post("/workflows", tags=["Workflows"])
def create_workflow(workflow_data: WorkflowCreate):
    db = get_db()

    try:
        return create_record(
            db=db,
            model=Workflow,
            id_field="workflow_id",
            schema_data=workflow_data,
            already_exists_message="Workflow already exists",
            success_message="Workflow created successfully",
            response_key="workflow"
        )

    finally:
        db.close()


@app.put("/workflows/{workflow_id}", tags=["Workflows"])
def update_workflow(workflow_id: str, workflow_data: WorkflowUpdate):
    db = get_db()

    try:
        return update_record(
            db=db,
            model=Workflow,
            id_field="workflow_id",
            id_value=workflow_id,
            schema_data=workflow_data,
            not_found_message="Workflow not found",
            success_message="Workflow updated successfully",
            response_key="workflow"
        )

    finally:
        db.close()


@app.delete("/workflows/{workflow_id}", tags=["Workflows"])
def delete_workflow(workflow_id: str):
    db = get_db()

    try:
        return delete_record(
            db=db,
            model=Workflow,
            id_field="workflow_id",
            id_value=workflow_id,
            not_found_message="Workflow not found",
            success_message="Workflow deleted successfully"
        )

    finally:
        db.close()


# ==========================================================
# COMPONENTS
# ==========================================================

@app.get("/components", tags=["Components"])
def get_components():
    db = get_db()

    try:
        components = db.query(Component).all()
        return list_response(
            message="Components retrieved successfully",
            items=components
        )

    finally:
        db.close()


@app.get("/components/{component_id}", tags=["Components"])
def get_component_by_id(component_id: str):
    db = get_db()

    try:
        component = get_record_or_404(
            db=db,
            model=Component,
            id_field="component_id",
            id_value=component_id,
            not_found_message="Component not found"
        )

        return success_response(
            message="Component retrieved successfully",
            data={"component": component}
        )

    finally:
        db.close()


@app.post("/components", tags=["Components"])
def create_component(component_data: ComponentCreate):
    db = get_db()

    try:
        return create_record(
            db=db,
            model=Component,
            id_field="component_id",
            schema_data=component_data,
            already_exists_message="Component already exists",
            success_message="Component created successfully",
            response_key="component"
        )

    finally:
        db.close()


@app.put("/components/{component_id}", tags=["Components"])
def update_component(component_id: str, component_data: ComponentUpdate):
    db = get_db()

    try:
        return update_record(
            db=db,
            model=Component,
            id_field="component_id",
            id_value=component_id,
            schema_data=component_data,
            not_found_message="Component not found",
            success_message="Component updated successfully",
            response_key="component"
        )

    finally:
        db.close()


@app.delete("/components/{component_id}", tags=["Components"])
def delete_component(component_id: str):
    db = get_db()

    try:
        return delete_record(
            db=db,
            model=Component,
            id_field="component_id",
            id_value=component_id,
            not_found_message="Component not found",
            success_message="Component deleted successfully"
        )

    finally:
        db.close()


# ==========================================================
# PROMPTS
# ==========================================================

@app.get("/prompts", tags=["Prompts"])
def get_prompts():
    db = get_db()

    try:
        prompts = db.query(Prompt).all()
        return list_response(
            message="Prompts retrieved successfully",
            items=prompts
        )

    finally:
        db.close()


@app.get("/prompts/{prompt_id}", tags=["Prompts"])
def get_prompt_by_id(prompt_id: str):
    db = get_db()

    try:
        prompt = get_record_or_404(
            db=db,
            model=Prompt,
            id_field="prompt_id",
            id_value=prompt_id,
            not_found_message="Prompt not found"
        )

        return success_response(
            message="Prompt retrieved successfully",
            data={"prompt": prompt}
        )

    finally:
        db.close()


@app.post("/prompts", tags=["Prompts"])
def create_prompt(prompt_data: PromptCreate):
    db = get_db()

    try:
        return create_record(
            db=db,
            model=Prompt,
            id_field="prompt_id",
            schema_data=prompt_data,
            already_exists_message="Prompt already exists",
            success_message="Prompt created successfully",
            response_key="prompt"
        )

    finally:
        db.close()


@app.put("/prompts/{prompt_id}", tags=["Prompts"])
def update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    db = get_db()

    try:
        return update_record(
            db=db,
            model=Prompt,
            id_field="prompt_id",
            id_value=prompt_id,
            schema_data=prompt_data,
            not_found_message="Prompt not found",
            success_message="Prompt updated successfully",
            response_key="prompt"
        )

    finally:
        db.close()


@app.delete("/prompts/{prompt_id}", tags=["Prompts"])
def delete_prompt(prompt_id: str):
    db = get_db()

    try:
        return delete_record(
            db=db,
            model=Prompt,
            id_field="prompt_id",
            id_value=prompt_id,
            not_found_message="Prompt not found",
            success_message="Prompt deleted successfully"
        )

    finally:
        db.close()


# ==========================================================
# METRICS
# ==========================================================

@app.get("/metrics", tags=["Metrics"])
def get_metrics():
    db = get_db()

    try:
        metrics = db.query(Metric).all()
        return list_response(
            message="Metrics retrieved successfully",
            items=metrics
        )

    finally:
        db.close()


@app.get("/metrics/{metric_id}", tags=["Metrics"])
def get_metric_by_id(metric_id: str):
    db = get_db()

    try:
        metric = get_record_or_404(
            db=db,
            model=Metric,
            id_field="metric_id",
            id_value=metric_id,
            not_found_message="Metric not found"
        )

        return success_response(
            message="Metric retrieved successfully",
            data={"metric": metric}
        )

    finally:
        db.close()


@app.post("/metrics", tags=["Metrics"])
def create_metric(metric_data: MetricCreate):
    db = get_db()

    try:
        return create_record(
            db=db,
            model=Metric,
            id_field="metric_id",
            schema_data=metric_data,
            already_exists_message="Metric already exists",
            success_message="Metric created successfully",
            response_key="metric"
        )

    finally:
        db.close()


@app.put("/metrics/{metric_id}", tags=["Metrics"])
def update_metric(metric_id: str, metric_data: MetricUpdate):
    db = get_db()

    try:
        return update_record(
            db=db,
            model=Metric,
            id_field="metric_id",
            id_value=metric_id,
            schema_data=metric_data,
            not_found_message="Metric not found",
            success_message="Metric updated successfully",
            response_key="metric"
        )

    finally:
        db.close()


@app.delete("/metrics/{metric_id}", tags=["Metrics"])
def delete_metric(metric_id: str):
    db = get_db()

    try:
        return delete_record(
            db=db,
            model=Metric,
            id_field="metric_id",
            id_value=metric_id,
            not_found_message="Metric not found",
            success_message="Metric deleted successfully"
        )

    finally:
        db.close()


# ==========================================================
# DASHBOARDS
# ==========================================================

@app.get("/dashboards", tags=["Dashboards"])
def get_dashboards():
    db = get_db()

    try:
        dashboards = db.query(Dashboard).all()
        return list_response(
            message="Dashboards retrieved successfully",
            items=dashboards
        )

    finally:
        db.close()


@app.get("/dashboards/{dashboard_id}", tags=["Dashboards"])
def get_dashboard_by_id(dashboard_id: str):
    db = get_db()

    try:
        dashboard = get_record_or_404(
            db=db,
            model=Dashboard,
            id_field="dashboard_id",
            id_value=dashboard_id,
            not_found_message="Dashboard not found"
        )

        return success_response(
            message="Dashboard retrieved successfully",
            data={"dashboard": dashboard}
        )

    finally:
        db.close()


@app.post("/dashboards", tags=["Dashboards"])
def create_dashboard(dashboard_data: DashboardCreate):
    db = get_db()

    try:
        return create_record(
            db=db,
            model=Dashboard,
            id_field="dashboard_id",
            schema_data=dashboard_data,
            already_exists_message="Dashboard already exists",
            success_message="Dashboard created successfully",
            response_key="dashboard"
        )

    finally:
        db.close()


@app.put("/dashboards/{dashboard_id}", tags=["Dashboards"])
def update_dashboard(dashboard_id: str, dashboard_data: DashboardUpdate):
    db = get_db()

    try:
        return update_record(
            db=db,
            model=Dashboard,
            id_field="dashboard_id",
            id_value=dashboard_id,
            schema_data=dashboard_data,
            not_found_message="Dashboard not found",
            success_message="Dashboard updated successfully",
            response_key="dashboard"
        )

    finally:
        db.close()


@app.delete("/dashboards/{dashboard_id}", tags=["Dashboards"])
def delete_dashboard(dashboard_id: str):
    db = get_db()

    try:
        return delete_record(
            db=db,
            model=Dashboard,
            id_field="dashboard_id",
            id_value=dashboard_id,
            not_found_message="Dashboard not found",
            success_message="Dashboard deleted successfully"
        )

    finally:
        db.close()


# ==========================================================
# KNOWLEDGE
# ==========================================================

@app.get("/knowledge", tags=["Knowledge"])
def get_knowledge_articles():
    db = get_db()

    try:
        knowledge_articles = db.query(KnowledgeArticle).all()
        return list_response(
            message="Knowledge articles retrieved successfully",
            items=knowledge_articles
        )

    finally:
        db.close()


@app.get("/knowledge/{article_id}", tags=["Knowledge"])
def get_knowledge_article_by_id(article_id: str):
    db = get_db()

    try:
        article = get_record_or_404(
            db=db,
            model=KnowledgeArticle,
            id_field="article_id",
            id_value=article_id,
            not_found_message="Knowledge article not found"
        )

        return success_response(
            message="Knowledge article retrieved successfully",
            data={"article": article}
        )

    finally:
        db.close()


@app.post("/knowledge", tags=["Knowledge"])
def create_knowledge_article(article_data: KnowledgeArticleCreate):
    db = get_db()

    try:
        return create_record(
            db=db,
            model=KnowledgeArticle,
            id_field="article_id",
            schema_data=article_data,
            already_exists_message="Knowledge article already exists",
            success_message="Knowledge article created successfully",
            response_key="article"
        )

    finally:
        db.close()


@app.put("/knowledge/{article_id}", tags=["Knowledge"])
def update_knowledge_article(article_id: str, article_data: KnowledgeArticleUpdate):
    db = get_db()

    try:
        return update_record(
            db=db,
            model=KnowledgeArticle,
            id_field="article_id",
            id_value=article_id,
            schema_data=article_data,
            not_found_message="Knowledge article not found",
            success_message="Knowledge article updated successfully",
            response_key="article"
        )

    finally:
        db.close()


@app.delete("/knowledge/{article_id}", tags=["Knowledge"])
def delete_knowledge_article(article_id: str):
    db = get_db()

    try:
        return delete_record(
            db=db,
            model=KnowledgeArticle,
            id_field="article_id",
            id_value=article_id,
            not_found_message="Knowledge article not found",
            success_message="Knowledge article deleted successfully"
        )

    finally:
        db.close()



# ==========================================================
# GOVERNANCE KPIS
# ==========================================================

@app.get("/governance/kpis", tags=["Governance"])
def get_governance_kpis():
    db = get_db()

    try:
        total_projects = db.query(Project).count()
        total_assets = db.query(Asset).count()
        total_agents = db.query(Agent).count()
        total_workflows = db.query(Workflow).count()
        total_components = db.query(Component).count()
        total_prompts = db.query(Prompt).count()
        total_metrics = db.query(Metric).count()
        total_dashboards = db.query(Dashboard).count()
        total_knowledge_articles = db.query(KnowledgeArticle).count()
        total_relationships = db.query(AssetRelationship).count()

        active_projects = db.query(Project).filter(
            Project.status.in_(["Active", "ACTIVE"])
        ).count()

        active_assets = db.query(Asset).filter(
            Asset.status.in_(["Active", "ACTIVE"])
        ).count()

        active_agents = db.query(Agent).filter(
            Agent.status.in_(["Active", "ACTIVE"])
        ).count()

        active_workflows = db.query(Workflow).filter(
            Workflow.status.in_(["Active", "ACTIVE"])
        ).count()

        active_components = db.query(Component).filter(
            Component.status.in_(["Active", "ACTIVE"])
        ).count()

        active_dashboards = db.query(Dashboard).filter(
            Dashboard.status.in_(["Active", "ACTIVE"])
        ).count()

        published_knowledge_articles = db.query(KnowledgeArticle).filter(
            KnowledgeArticle.status.in_(["Published", "PUBLISHED"])
        ).count()

        high_criticality_assets = db.query(Asset).filter(
            Asset.criticality.in_(["High", "HIGH", "Critical", "CRITICAL"])
        ).count()

        assets_linked_to_project = db.query(Asset).filter(
            Asset.project_id.isnot(None)
        ).count()

        assets_without_project = total_assets - assets_linked_to_project

        if total_assets > 0:
            asset_project_coverage_percent = round(
                (assets_linked_to_project / total_assets) * 100,
                2
            )
        else:
            asset_project_coverage_percent = 0

        total_catalog_items = (
            total_projects
            + total_assets
            + total_agents
            + total_workflows
            + total_components
            + total_prompts
            + total_metrics
            + total_dashboards
            + total_knowledge_articles
            + total_relationships
        )

        governance_kpis = {
            "catalog": {
                "total_catalog_items": total_catalog_items,
                "total_projects": total_projects,
                "total_assets": total_assets,
                "total_agents": total_agents,
                "total_workflows": total_workflows,
                "total_components": total_components,
                "total_prompts": total_prompts,
                "total_metrics": total_metrics,
                "total_dashboards": total_dashboards,
                "total_knowledge_articles": total_knowledge_articles,
                "total_relationships": total_relationships
            },
            "status": {
                "active_projects": active_projects,
                "active_assets": active_assets,
                "active_agents": active_agents,
                "active_workflows": active_workflows,
                "active_components": active_components,
                "active_dashboards": active_dashboards,
                "published_knowledge_articles": published_knowledge_articles
            },
            "risk_and_governance": {
                "high_criticality_assets": high_criticality_assets,
                "assets_linked_to_project": assets_linked_to_project,
                "assets_without_project": assets_without_project,
                "asset_project_coverage_percent": asset_project_coverage_percent
            }
        }

        return success_response(
            message="Governance KPIs retrieved successfully",
            data=governance_kpis
        )

    finally:
        db.close()

# ==========================================================
# INVENTORY
# ==========================================================

@app.get("/inventory", tags=["Inventory"])
def get_inventory():
    db = get_db()

    try:
        inventory = {
            "projects": db.query(Project).all(),
            "assets": db.query(Asset).all(),
            "components": db.query(Component).all(),
            "workflows": db.query(Workflow).all(),
            "agents": db.query(Agent).all(),
            "prompts": db.query(Prompt).all(),
            "metrics": db.query(Metric).all(),
            "dashboards": db.query(Dashboard).all(),
            "knowledge_articles": db.query(KnowledgeArticle).all(),
            "relationships": db.query(AssetRelationship).all()
        }

        return success_response(
            message="Inventory retrieved successfully",
            data=inventory
        )

    finally:
        db.close()

        
# ==========================================================
# GLOBAL SEARCH
# ==========================================================

@app.get("/search", tags=["Search"])
def global_search(q: str = Query(..., min_length=1)):
    db = get_db()

    try:
        search_term = f"%{q}%"

        projects = db.query(Project).filter(
            or_(
                Project.project_id.ilike(search_term),
                Project.project_name.ilike(search_term),
                Project.description.ilike(search_term),
                Project.owner.ilike(search_term),
                Project.status.ilike(search_term),
                Project.priority.ilike(search_term),
                Project.repository_url.ilike(search_term),
            )
        ).all()

        assets = db.query(Asset).filter(
            or_(
                Asset.asset_id.ilike(search_term),
                Asset.project_id.ilike(search_term),
                Asset.asset_name.ilike(search_term),
                Asset.asset_type.ilike(search_term),
                Asset.owner.ilike(search_term),
                Asset.status.ilike(search_term),
                Asset.criticality.ilike(search_term),
                Asset.technology.ilike(search_term),
                Asset.environment.ilike(search_term),
            )
        ).all()

        agents = db.query(Agent).filter(
            or_(
                Agent.agent_id.ilike(search_term),
                Agent.project_id.ilike(search_term),
                Agent.agent_name.ilike(search_term),
                Agent.version.ilike(search_term),
                Agent.owner.ilike(search_term),
                Agent.status.ilike(search_term),
                Agent.model_provider.ilike(search_term),
                Agent.model_name.ilike(search_term),
                Agent.purpose.ilike(search_term),
            )
        ).all()

        workflows = db.query(Workflow).filter(
            or_(
                Workflow.workflow_id.ilike(search_term),
                Workflow.project_id.ilike(search_term),
                Workflow.workflow_name.ilike(search_term),
                Workflow.workflow_type.ilike(search_term),
                Workflow.owner.ilike(search_term),
                Workflow.status.ilike(search_term),
                Workflow.trigger_type.ilike(search_term),
                Workflow.technology.ilike(search_term),
            )
        ).all()

        components = db.query(Component).filter(
            or_(
                Component.component_id.ilike(search_term),
                Component.project_id.ilike(search_term),
                Component.component_name.ilike(search_term),
                Component.component_type.ilike(search_term),
                Component.owner.ilike(search_term),
                Component.status.ilike(search_term),
                Component.technology.ilike(search_term),
                Component.repository_url.ilike(search_term),
            )
        ).all()

        prompts = db.query(Prompt).filter(
            or_(
                Prompt.prompt_id.ilike(search_term),
                Prompt.project_id.ilike(search_term),
                Prompt.prompt_name.ilike(search_term),
                Prompt.prompt_type.ilike(search_term),
                Prompt.owner.ilike(search_term),
                Prompt.status.ilike(search_term),
                Prompt.version.ilike(search_term),
                Prompt.model_provider.ilike(search_term),
                Prompt.prompt_content.ilike(search_term),
            )
        ).all()

        metrics = db.query(Metric).filter(
            or_(
                Metric.metric_id.ilike(search_term),
                Metric.project_id.ilike(search_term),
                Metric.metric_name.ilike(search_term),
                Metric.metric_category.ilike(search_term),
                Metric.metric_type.ilike(search_term),
                Metric.owner.ilike(search_term),
                Metric.status.ilike(search_term),
            )
        ).all()

        dashboards = db.query(Dashboard).filter(
            or_(
                Dashboard.dashboard_id.ilike(search_term),
                Dashboard.project_id.ilike(search_term),
                Dashboard.dashboard_name.ilike(search_term),
                Dashboard.dashboard_type.ilike(search_term),
                Dashboard.owner.ilike(search_term),
                Dashboard.status.ilike(search_term),
                Dashboard.technology.ilike(search_term),
                Dashboard.dashboard_url.ilike(search_term),
            )
        ).all()

        knowledge_articles = db.query(KnowledgeArticle).filter(
            or_(
                KnowledgeArticle.article_id.ilike(search_term),
                KnowledgeArticle.project_id.ilike(search_term),
                KnowledgeArticle.title.ilike(search_term),
                KnowledgeArticle.category.ilike(search_term),
                KnowledgeArticle.author.ilike(search_term),
                KnowledgeArticle.status.ilike(search_term),
                KnowledgeArticle.tags.ilike(search_term),
                KnowledgeArticle.article_content.ilike(search_term),
            )
        ).all()

        relationships = db.query(AssetRelationship).filter(
            or_(
                AssetRelationship.source_asset_id.ilike(search_term),
                AssetRelationship.source_asset_type.ilike(search_term),
                AssetRelationship.target_asset_id.ilike(search_term),
                AssetRelationship.target_asset_type.ilike(search_term),
                AssetRelationship.relationship_type.ilike(search_term),
                AssetRelationship.description.ilike(search_term),
            )
        ).all()

        search_results = {
            "query": q,
            "totals": {
                "projects": len(projects),
                "assets": len(assets),
                "agents": len(agents),
                "workflows": len(workflows),
                "components": len(components),
                "prompts": len(prompts),
                "metrics": len(metrics),
                "dashboards": len(dashboards),
                "knowledge_articles": len(knowledge_articles),
                "relationships": len(relationships),
            },
            "projects": projects,
            "assets": assets,
            "agents": agents,
            "workflows": workflows,
            "components": components,
            "prompts": prompts,
            "metrics": metrics,
            "dashboards": dashboards,
            "knowledge_articles": knowledge_articles,
            "relationships": relationships,
        }

        return success_response(
            message="Search completed successfully",
            data=search_results
        )

    finally:
        db.close()
