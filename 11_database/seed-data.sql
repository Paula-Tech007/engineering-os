-- Engineering OS - Initial Seed Data
-- Database Engine: MariaDB/MySQL

USE engineering_os;

INSERT INTO projects (
    project_id,
    project_name,
    description,
    owner,
    status,
    priority,
    repository_url
) VALUES (
    'PRJ-0001',
    'Engineering OS',
    'Centralized engineering operating system for governance, reuse, cataloging and discovery of engineering assets.',
    'Paula Sabino',
    'ACTIVE',
    'HIGH',
    'https://github.com/Paula-Tech007/engineering-os'
);

INSERT INTO assets (
    asset_id,
    project_id,
    asset_name,
    asset_type,
    owner,
    status,
    criticality,
    technology,
    environment
) VALUES (
    'ASSET-0001',
    'PRJ-0001',
    'Engineering OS API',
    'API',
    'Paula Sabino',
    'ACTIVE',
    'HIGH',
    'FastAPI',
    'LOCAL'
);

INSERT INTO workflows (
    workflow_id,
    project_id,
    workflow_name,
    workflow_type,
    owner,
    status,
    trigger_type,
    technology
) VALUES (
    'WF-0001',
    'PRJ-0001',
    'Engineering OS Governance Workflow',
    'Governance',
    'Paula Sabino',
    'ACTIVE',
    'Manual',
    'Markdown'
);

INSERT INTO agents (
    agent_id,
    agent_name,
    version,
    owner,
    project_id,
    status,
    model_provider,
    model_name,
    purpose
) VALUES (
    'AGENT-0001',
    'Engineering OS Assistant',
    '1.0.0',
    'Paula Sabino',
    'PRJ-0001',
    'ACTIVE',
    'OpenAI',
    'GPT',
    'Provide governance guidance, asset discovery, catalog consultation and engineering standards support.'
);

INSERT INTO components (
    component_id,
    component_name,
    component_type,
    project_id,
    owner,
    status,
    technology,
    repository_url
) VALUES (
    'COMPONENT-0001',
    'Standard API Response Contract',
    'Backend Utility',
    'PRJ-0001',
    'Paula Sabino',
    'ACTIVE',
    'Python',
    'https://github.com/Paula-Tech007/engineering-os'
);

INSERT INTO prompts (
    prompt_id,
    project_id,
    prompt_name,
    prompt_type,
    owner,
    status,
    version,
    model_provider,
    prompt_content
) VALUES (
    'PROMPT-0001',
    'PRJ-0001',
    'Engineering OS Governance Prompt',
    'System',
    'Paula Sabino',
    'ACTIVE',
    '1.0.0',
    'OpenAI',
    'Use Engineering OS governance standards to answer catalog, reuse and lifecycle questions.'
);

INSERT INTO metrics (
    metric_id,
    project_id,
    metric_name,
    metric_category,
    metric_type,
    owner,
    target_value,
    current_value,
    status
) VALUES (
    'METRIC-0001',
    'PRJ-0001',
    'Catalog Coverage',
    'Governance',
    'Percentage',
    'Paula Sabino',
    100.00,
    100.00,
    'ACTIVE'
);

INSERT INTO dashboards (
    dashboard_id,
    project_id,
    dashboard_name,
    dashboard_type,
    owner,
    status,
    technology,
    dashboard_url
) VALUES (
    'DASH-0001',
    'PRJ-0001',
    'Engineering OS Governance Dashboard',
    'Governance',
    'Paula Sabino',
    'ACTIVE',
    'FastAPI',
    '/dashboard/summary'
);

INSERT INTO knowledge_articles (
    article_id,
    project_id,
    title,
    category,
    author,
    status,
    tags,
    article_content
) VALUES (
    'KB-0001',
    'PRJ-0001',
    'Engineering OS MVP Operating Guide',
    'Governance',
    'Paula Sabino',
    'PUBLISHED',
    'engineering-os,mvp,governance',
    'Use the API, catalogs and SQL assets as the authoritative MVP baseline for Engineering OS.'
);

INSERT INTO asset_relationships (
    source_asset_id,
    source_asset_type,
    target_asset_id,
    target_asset_type,
    relationship_type,
    description
) VALUES
(
    'ASSET-0001',
    'ASSET',
    'PRJ-0001',
    'PROJECT',
    'RELATED_TO',
    'Engineering OS API belongs to the Engineering OS project.'
),
(
    'AGENT-0001',
    'AGENT',
    'PROMPT-0001',
    'PROMPT',
    'USES',
    'Engineering OS Assistant uses the governance prompt.'
),
(
    'DASH-0001',
    'DASHBOARD',
    'METRIC-0001',
    'METRIC',
    'MONITORS',
    'Governance dashboard monitors catalog coverage.'
);
