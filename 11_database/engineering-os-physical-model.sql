-- Engineering OS - Physical Database Model
-- Database Engine: MariaDB/MySQL
-- Version: 1.0.0
-- Author: Paula Sabino

CREATE DATABASE IF NOT EXISTS engineering_os
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE engineering_os;

CREATE TABLE IF NOT EXISTS projects (
    project_id VARCHAR(50) PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    description TEXT,
    owner VARCHAR(255),
    status VARCHAR(50) NOT NULL,
    priority VARCHAR(50),
    repository_url VARCHAR(500),
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS assets (
    asset_id VARCHAR(50) PRIMARY KEY,
    project_id VARCHAR(50),
    asset_name VARCHAR(255) NOT NULL,
    asset_type VARCHAR(100) NOT NULL,
    owner VARCHAR(255),
    status VARCHAR(50) NOT NULL,
    criticality VARCHAR(50),
    technology VARCHAR(100),
    environment VARCHAR(50),
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_assets_project
        FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS agents (
    agent_id VARCHAR(50) PRIMARY KEY,
    agent_name VARCHAR(255) NOT NULL,
    version VARCHAR(50),
    owner VARCHAR(255),
    project_id VARCHAR(50),
    status VARCHAR(50) NOT NULL,
    model_provider VARCHAR(100),
    model_name VARCHAR(100),
    purpose TEXT,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_agents_project
        FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS workflows (
    workflow_id VARCHAR(50) PRIMARY KEY,
    workflow_name VARCHAR(255) NOT NULL,
    workflow_type VARCHAR(100),
    project_id VARCHAR(50),
    owner VARCHAR(255),
    status VARCHAR(50) NOT NULL,
    trigger_type VARCHAR(100),
    technology VARCHAR(100),
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_workflows_project
        FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS components (
    component_id VARCHAR(50) PRIMARY KEY,
    component_name VARCHAR(255) NOT NULL,
    component_type VARCHAR(100),
    project_id VARCHAR(50),
    owner VARCHAR(255),
    status VARCHAR(50) NOT NULL,
    technology VARCHAR(100),
    repository_url VARCHAR(500),
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_components_project
        FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS prompts (
    prompt_id VARCHAR(50) PRIMARY KEY,
    project_id VARCHAR(50),
    prompt_name VARCHAR(255) NOT NULL,
    prompt_type VARCHAR(100),
    owner VARCHAR(255),
    status VARCHAR(50) NOT NULL,
    version VARCHAR(50),
    model_provider VARCHAR(100),
    prompt_content TEXT,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_prompts_project
        FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS metrics (
    metric_id VARCHAR(50) PRIMARY KEY,
    project_id VARCHAR(50),
    metric_name VARCHAR(255) NOT NULL,
    metric_category VARCHAR(100),
    metric_type VARCHAR(100),
    owner VARCHAR(255),
    target_value DECIMAL(18, 2),
    current_value DECIMAL(18, 2),
    status VARCHAR(50) NOT NULL,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_metrics_project
        FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS dashboards (
    dashboard_id VARCHAR(50) PRIMARY KEY,
    project_id VARCHAR(50),
    dashboard_name VARCHAR(255) NOT NULL,
    dashboard_type VARCHAR(100),
    owner VARCHAR(255),
    status VARCHAR(50) NOT NULL,
    technology VARCHAR(100),
    dashboard_url VARCHAR(500),
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_dashboards_project
        FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS knowledge_articles (
    article_id VARCHAR(50) PRIMARY KEY,
    project_id VARCHAR(50),
    title VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    author VARCHAR(255),
    status VARCHAR(50) NOT NULL,
    tags VARCHAR(500),
    article_content TEXT,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_knowledge_articles_project
        FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS asset_relationships (
    relationship_id INT AUTO_INCREMENT PRIMARY KEY,
    source_asset_id VARCHAR(50) NOT NULL,
    source_asset_type VARCHAR(100) NOT NULL,
    target_asset_id VARCHAR(50) NOT NULL,
    target_asset_type VARCHAR(100) NOT NULL,
    relationship_type VARCHAR(100) NOT NULL,
    description TEXT,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_asset_relationships_source (source_asset_id),
    INDEX idx_asset_relationships_target (target_asset_id),
    INDEX idx_asset_relationships_type (relationship_type)
);
