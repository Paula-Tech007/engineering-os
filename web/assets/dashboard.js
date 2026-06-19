const baseline = {
  summary: {
    total_projects: 1,
    total_assets: 1,
    total_agents: 1,
    total_workflows: 1,
    total_components: 1,
    total_prompts: 1,
    total_metrics: 1,
    total_dashboards: 1,
    total_knowledge_articles: 1,
    total_relationships: 3,
  },
  kpis: {
    catalog: {
      total_catalog_items: 12,
    },
    status: {
      active_projects: 1,
    },
    risk_and_governance: {
      asset_project_coverage_percent: 100,
    },
  },
  inventory: {
    projects: [
      {
        id: "PRJ-0001",
        type: "Projeto",
        name: "Engineering OS",
        status: "ACTIVE",
        owner: "Paula Sabino",
      },
    ],
    assets: [
      {
        id: "ASSET-0001",
        type: "Ativo",
        name: "Engineering OS API",
        status: "ACTIVE",
        owner: "Paula Sabino",
      },
    ],
    workflows: [
      {
        id: "WF-0001",
        type: "Workflow",
        name: "Engineering OS Governance Workflow",
        status: "ACTIVE",
        owner: "Paula Sabino",
      },
    ],
    agents: [
      {
        id: "AGENT-0001",
        type: "Agente",
        name: "Engineering OS Assistant",
        status: "ACTIVE",
        owner: "Paula Sabino",
      },
    ],
    components: [
      {
        id: "COMPONENT-0001",
        type: "Componente",
        name: "Standard API Response Contract",
        status: "ACTIVE",
        owner: "Paula Sabino",
      },
    ],
    prompts: [
      {
        id: "PROMPT-0001",
        type: "Prompt",
        name: "Engineering OS Governance Prompt",
        status: "ACTIVE",
        owner: "Paula Sabino",
      },
    ],
    metrics: [
      {
        id: "METRIC-0001",
        type: "Metrica",
        name: "Catalog Coverage",
        status: "ACTIVE",
        owner: "Paula Sabino",
      },
    ],
    dashboards: [
      {
        id: "DASH-0001",
        type: "Dashboard",
        name: "Engineering OS Governance Dashboard",
        status: "ACTIVE",
        owner: "Paula Sabino",
      },
    ],
    knowledge_articles: [
      {
        id: "KB-0001",
        type: "Conhecimento",
        name: "Engineering OS MVP Operating Guide",
        status: "PUBLISHED",
        owner: "Paula Sabino",
      },
    ],
    relationships: [
      {
        source_asset_id: "ASSET-0001",
        source_asset_type: "ASSET",
        target_asset_id: "PRJ-0001",
        target_asset_type: "PROJECT",
        relationship_type: "RELATED_TO",
      },
      {
        source_asset_id: "AGENT-0001",
        source_asset_type: "AGENT",
        target_asset_id: "PROMPT-0001",
        target_asset_type: "PROMPT",
        relationship_type: "USES",
      },
      {
        source_asset_id: "DASH-0001",
        source_asset_type: "DASHBOARD",
        target_asset_id: "METRIC-0001",
        target_asset_type: "METRIC",
        relationship_type: "MONITORS",
      },
    ],
  },
};

let inventoryRows = [];
let relationships = [];
let usingBaseline = false;

const elements = {
  apiStatus: document.querySelector("#apiStatus"),
  dataStatus: document.querySelector("#dataStatus"),
  totalCatalogItems: document.querySelector("#totalCatalogItems"),
  totalProjects: document.querySelector("#totalProjects"),
  activeProjects: document.querySelector("#activeProjects"),
  totalAssets: document.querySelector("#totalAssets"),
  assetCoverage: document.querySelector("#assetCoverage"),
  totalRelationships: document.querySelector("#totalRelationships"),
  relationshipCount: document.querySelector("#relationshipCount"),
  coverageLabel: document.querySelector("#coverageLabel"),
  impactLabel: document.querySelector("#impactLabel"),
  inventoryRows: document.querySelector("#inventoryRows"),
  relationshipRail: document.querySelector("#relationshipRail"),
  searchForm: document.querySelector("#searchForm"),
  searchInput: document.querySelector("#searchInput"),
  searchResults: document.querySelector("#searchResults"),
  impactForm: document.querySelector("#impactForm"),
  impactInput: document.querySelector("#impactInput"),
  impactResults: document.querySelector("#impactResults"),
};

function setStatus(element, text, state = "ok") {
  element.textContent = text;
  element.classList.remove("muted", "warning", "danger");
  if (state !== "ok") {
    element.classList.add(state);
  }
}

async function fetchJson(path) {
  const response = await fetch(path, {
    headers: {
      Accept: "application/json",
    },
  });

  if (!response.ok) {
    throw new Error(`${path} returned ${response.status}`);
  }

  return response.json();
}

function formatNumber(value) {
  return new Intl.NumberFormat("pt-BR").format(Number(value || 0));
}

function normalizeInventory(data) {
  const sources = [
    ["projects", "Projeto", "project_id", "project_name"],
    ["assets", "Ativo", "asset_id", "asset_name"],
    ["agents", "Agente", "agent_id", "agent_name"],
    ["workflows", "Workflow", "workflow_id", "workflow_name"],
    ["components", "Componente", "component_id", "component_name"],
    ["prompts", "Prompt", "prompt_id", "prompt_name"],
    ["metrics", "Metrica", "metric_id", "metric_name"],
    ["dashboards", "Dashboard", "dashboard_id", "dashboard_name"],
    ["knowledge_articles", "Conhecimento", "article_id", "title"],
  ];

  return sources.flatMap(([key, type, idField, nameField]) => {
    const items = data[key] || [];
    return items.map((item) => ({
      id: item.id || item[idField] || "-",
      type,
      group: key,
      name: item.name || item[nameField] || "-",
      status: item.status || "-",
      owner: item.owner || item.author || "-",
    }));
  });
}

function renderSummary(summary, kpis) {
  const catalogTotal = kpis?.catalog?.total_catalog_items
    ?? Object.values(summary).reduce((total, value) => total + Number(value || 0), 0);
  const activeProjects = kpis?.status?.active_projects || 0;
  const coverage = kpis?.risk_and_governance?.asset_project_coverage_percent || 0;

  elements.totalCatalogItems.textContent = formatNumber(catalogTotal);
  elements.totalProjects.textContent = formatNumber(summary.total_projects);
  elements.totalAssets.textContent = formatNumber(summary.total_assets);
  elements.totalRelationships.textContent = formatNumber(summary.total_relationships);
  elements.activeProjects.textContent = `${formatNumber(activeProjects)} ativos`;
  elements.assetCoverage.textContent = `${formatNumber(coverage)}% vinculados`;
  elements.coverageLabel.textContent = usingBaseline ? "Baseline do seed inicial" : "Dados conectados ao banco";
  elements.impactLabel.textContent = "Grafo de dependencias";
}

function renderInventory(filter = "all") {
  const rows = filter === "all"
    ? inventoryRows
    : inventoryRows.filter((row) => row.group === filter);

  if (!rows.length) {
    elements.inventoryRows.innerHTML = '<tr><td colspan="5">Nenhum item encontrado.</td></tr>';
    return;
  }

  elements.inventoryRows.innerHTML = rows.map((row) => `
    <tr>
      <td><strong>${escapeHtml(row.id)}</strong></td>
      <td><span class="type-badge">${escapeHtml(row.type)}</span></td>
      <td>${escapeHtml(row.name)}</td>
      <td><span class="state-badge ${row.status === "PUBLISHED" ? "warning" : ""}">${escapeHtml(row.status)}</span></td>
      <td>${escapeHtml(row.owner)}</td>
    </tr>
  `).join("");
}

function renderRelationships(items) {
  relationships = items || [];
  elements.relationshipCount.textContent = `${formatNumber(relationships.length)} relacoes`;

  if (!relationships.length) {
    elements.relationshipRail.innerHTML = '<p class="empty-state">Nenhum relacionamento registrado.</p>';
    return;
  }

  elements.relationshipRail.innerHTML = relationships.slice(0, 6).map((item) => `
    <article class="relationship-item">
      <strong>${escapeHtml(item.source_asset_id || "-")} -> ${escapeHtml(item.target_asset_id || "-")}</strong>
      <span>${escapeHtml(item.source_asset_type || "-")} / ${escapeHtml(item.target_asset_type || "-")}</span>
      <span>${escapeHtml(item.relationship_type || "-")}</span>
    </article>
  `).join("");
}

function flattenSearchResults(payload) {
  const data = payload?.data || {};
  const keys = [
    ["projects", "Projeto", "project_id", "project_name"],
    ["assets", "Ativo", "asset_id", "asset_name"],
    ["agents", "Agente", "agent_id", "agent_name"],
    ["workflows", "Workflow", "workflow_id", "workflow_name"],
    ["components", "Componente", "component_id", "component_name"],
    ["prompts", "Prompt", "prompt_id", "prompt_name"],
    ["metrics", "Metrica", "metric_id", "metric_name"],
    ["dashboards", "Dashboard", "dashboard_id", "dashboard_name"],
    ["knowledge_articles", "Conhecimento", "article_id", "title"],
  ];

  return keys.flatMap(([key, type, idField, nameField]) => (data[key] || []).map((item) => ({
    id: item[idField],
    type,
    name: item[nameField],
    status: item.status,
  })));
}

async function handleSearch(event) {
  event.preventDefault();
  const query = elements.searchInput.value.trim();

  if (!query) {
    elements.searchResults.innerHTML = '<p class="empty-state">Digite um termo para consultar o catalogo.</p>';
    return;
  }

  try {
    const payload = await fetchJson(`/search?q=${encodeURIComponent(query)}`);
    const results = flattenSearchResults(payload);
    renderSearchResults(results);
  } catch (error) {
    const localResults = inventoryRows.filter((row) => {
      const text = `${row.id} ${row.type} ${row.name} ${row.status} ${row.owner}`.toLowerCase();
      return text.includes(query.toLowerCase());
    });
    renderSearchResults(localResults, true);
  }
}

function renderSearchResults(results, local = false) {
  if (!results.length) {
    elements.searchResults.innerHTML = '<p class="empty-state">Nenhum resultado encontrado.</p>';
    return;
  }

  const suffix = local ? "Resultado local" : "Resultado da API";
  elements.searchResults.innerHTML = results.slice(0, 6).map((item) => `
    <article class="result-item">
      <strong>${escapeHtml(item.id || "-")} - ${escapeHtml(item.name || "-")}</strong>
      <span>${escapeHtml(item.type || "-")} - ${escapeHtml(item.status || "-")} - ${suffix}</span>
    </article>
  `).join("");
}

async function handleImpact(event) {
  event.preventDefault();
  const assetId = elements.impactInput.value.trim();

  if (!assetId) {
    elements.impactResults.innerHTML = '<p class="empty-state">Informe um ativo para ver dependencias e dependentes.</p>';
    return;
  }

  try {
    const payload = await fetchJson(`/assets/${encodeURIComponent(assetId)}/impact`);
    const data = payload.data || {};
    renderImpact(
      data.summary?.direct_dependencies || 0,
      data.summary?.direct_dependents || 0,
      data.summary?.total_direct_relationships || 0,
      false,
    );
  } catch (error) {
    const dependencies = relationships.filter((item) => item.source_asset_id === assetId).length;
    const dependents = relationships.filter((item) => item.target_asset_id === assetId).length;
    renderImpact(dependencies, dependents, dependencies + dependents, true);
  }
}

function renderImpact(dependencies, dependents, total, local = false) {
  elements.impactResults.innerHTML = `
    <div class="impact-row">
      <strong>${formatNumber(dependencies)} dependencias</strong>
      <span>Saidas diretas do ativo consultado</span>
    </div>
    <div class="impact-row">
      <strong>${formatNumber(dependents)} dependentes</strong>
      <span>Entradas diretas para o ativo consultado</span>
    </div>
    <div class="impact-row">
      <strong>${formatNumber(total)} relacoes diretas</strong>
      <span>${local ? "Calculado no baseline local" : "Calculado pela API"}</span>
    </div>
  `;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

async function bootstrap() {
  try {
    await fetchJson("/");
    setStatus(elements.apiStatus, "API online");
  } catch (error) {
    setStatus(elements.apiStatus, "API indisponivel", "danger");
  }

  try {
    const [summaryPayload, kpiPayload, inventoryPayload] = await Promise.all([
      fetchJson("/dashboard/summary"),
      fetchJson("/governance/kpis"),
      fetchJson("/inventory"),
    ]);

    const summary = summaryPayload.data || {};
    const kpis = kpiPayload.data || {};
    const inventory = inventoryPayload.data || {};

    usingBaseline = false;
    inventoryRows = normalizeInventory(inventory);
    renderSummary(summary, kpis);
    renderInventory();
    renderRelationships(inventory.relationships || []);
    setStatus(elements.dataStatus, "Banco conectado");
  } catch (error) {
    usingBaseline = true;
    inventoryRows = normalizeInventory(baseline.inventory);
    renderSummary(baseline.summary, baseline.kpis);
    renderInventory();
    renderRelationships(baseline.inventory.relationships);
    setStatus(elements.dataStatus, "Preview sem banco", "warning");
  }
}

document.querySelectorAll(".segment").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".segment").forEach((segment) => segment.classList.remove("active"));
    button.classList.add("active");
    renderInventory(button.dataset.filter);
  });
});

elements.searchForm.addEventListener("submit", handleSearch);
elements.impactForm.addEventListener("submit", handleImpact);

bootstrap();
