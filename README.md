# Engineering OS

![Status](https://img.shields.io/badge/status-MVP%20concluido-2ea44f)
![API](https://img.shields.io/badge/API-FastAPI-009688)
![Database](https://img.shields.io/badge/database-MariaDB-003545)
![Tests](https://img.shields.io/badge/tests-unittest-blue)

Plataforma corporativa para governanca, reutilizacao, catalogacao e descoberta de ativos de engenharia, automacao, seguranca e inteligencia artificial.

O Engineering OS organiza projetos, APIs, agentes, workflows, componentes, prompts, metricas, dashboards, conhecimento e relacionamentos em um modelo unico de governanca e rastreabilidade.

---

## Visao Geral

| Item | Detalhe |
|------|---------|
| Versao | 1.0.0 |
| Status | MVP concluido |
| Responsavel | Paula Sabino |
| Stack principal | FastAPI, SQLAlchemy, Pydantic, MariaDB |
| Repositorio | `github.com/Paula-Tech007/engineering-os` |

## Preview do Dashboard

![Engineering OS Dashboard Cyberpunk](docs/assets/dashboard-cyberpunk.png)

## O Que o MVP Entrega

- API FastAPI para governanca, catalogo, inventario e descoberta de ativos.
- CRUD de projetos, ativos, agentes, workflows, componentes, prompts, metricas, dashboards e artigos de conhecimento.
- CRUD de relacionamentos entre ativos e entidades do catalogo.
- Dashboard web servido pela propria API.
- Inventario consolidado e inventario por projeto.
- Busca global por texto.
- Consulta de relacionamentos por ativo.
- Analise de impacto direto por ativo.
- KPIs de governanca.
- Contrato de resposta padronizado.
- Validacao de schemas com Pydantic.
- Scripts SQL para criar e popular a base MariaDB.
- Testes automatizados leves sem dependencia de banco ativo.

## Arquitetura

```mermaid
graph LR
    A[Catalogos e Governanca] --> B[FastAPI]
    C[MariaDB] --> B
    B --> D[Inventario]
    B --> E[Busca Global]
    B --> F[Relacionamentos]
    B --> G[KPIs]
    F --> H[Analise de Impacto]
```

## Estrutura do Repositorio

| Caminho | Finalidade |
|---------|------------|
| `00_governance/` | Modelo de governanca e registro de ativos |
| `01_framework/` | Roadmap e diretrizes do Engineering OS |
| `02_catalogs/` | Catalogos oficiais e padroes de identificacao |
| `03_projects/` | Registro dos projetos governados |
| `04_knowledge/` | Base e templates de conhecimento |
| `07_workflows/` | Workflows documentados |
| `08_agents/` | Agentes documentados |
| `11_database/` | Modelo fisico, modelo logico e seed SQL |
| `15_templates/` | Templates reutilizaveis |
| `api/` | API FastAPI, models, schemas e testes |

## API

A API fica em `api/` e expoe o contrato principal do MVP.

| Recurso | Endpoint |
|---------|----------|
| Status da API | `GET /` |
| Health check | `GET /health` |
| Projetos | `/projects` |
| Ativos | `/assets` |
| Agentes | `/agents` |
| Workflows | `/workflows` |
| Componentes | `/components` |
| Prompts | `/prompts` |
| Metricas | `/metrics` |
| Dashboards | `/dashboards` |
| Conhecimento | `/knowledge` |
| Relacionamentos | `/relationships` |
| Dashboard web | `GET /dashboard` |
| Inventario consolidado | `GET /inventory` |
| Inventario por projeto | `GET /projects/{project_id}/inventory` |
| Relacionamentos por ativo | `GET /assets/{asset_id}/relationships` |
| Impacto direto por ativo | `GET /assets/{asset_id}/impact` |
| Busca global | `GET /search?q=termo` |
| KPIs de governanca | `GET /governance/kpis` |
| Dashboard summary | `GET /dashboard/summary` |

## Execucao Local

Crie o ambiente virtual e instale as dependencias:

```powershell
python -m venv api\venv
api\venv\Scripts\python.exe -m pip install -r api\requirements.txt
```

Configure a conexao com o banco, quando necessario:

```powershell
$env:ENGINEERING_OS_DATABASE_URL="mysql+pymysql://usuario:senha@localhost:3306/engineering_os"
```

Crie a base MariaDB e carregue os dados iniciais:

```powershell
mysql -u usuario -p < 11_database\engineering-os-physical-model.sql
mysql -u usuario -p < 11_database\seed-data.sql
```

Inicie a API:

```powershell
api\venv\Scripts\python.exe -m uvicorn api.main:app --reload
```

Depois acesse:

- API: `http://127.0.0.1:8000`
- Dashboard web: `http://127.0.0.1:8000/dashboard`
- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

## Testes

Execute os testes de contrato sem depender de banco ativo:

```powershell
api\venv\Scripts\python.exe -m unittest discover -s api/tests
```

## Roadmap

| Fase | Status |
|------|--------|
| Foundation setup | Concluido |
| Catalogos reais | Concluido |
| Asset registry e busca | Concluido |
| Search engine MVP | Concluido |
| Dashboards e KPIs | Concluido |
| Relacionamentos e impacto | Concluido |
| Reuse engine automation | Futuro |
| Portal Engineering OS | Futuro |
| Busca semantica com IA | Futuro |

## Governanca

O Engineering OS segue um modelo de governanca baseado em:

- padroes de IDs;
- registro central de ativos;
- catalogos versionados;
- templates reutilizaveis;
- rastreabilidade entre entidades;
- revisao periodica dos ativos governados.

## Status Atual

O MVP esta concluido e versionado no GitHub. A base atual entrega API, banco, seed inicial, contratos de resposta, testes, inventario, busca global, relacionamentos, analise de impacto e KPIs de governanca.
