# 03. Arquitectura del Sistema Agéntico de BI

## 1. Diagrama de Arquitectura

```mermaid
flowchart TD
    subgraph DataLayer["Capa de Datos"]
        DB[("PostgreSQL en Supabase\nTabla: fact_sales\n407,664 registros")]
    end

    subgraph ToolLayer["Capa de Herramientas (Tools)"]
        DBTool["db_tool.py\n- SQL Queries analíticas\n- Cálculo RFM\n- Filtro Churn (>60 días)\n- Historial y Top SKUs"]
    end

    subgraph AgentLayer["Capa de Inteligencia y Agente"]
        Agent["BIAgentCustomerRetention (agent.py)\n- Orquestación analítica\n- Detección de Top 5 VIPs en riesgo\n- Motor de diagnóstico comercial\n- Formulación de 3 acciones tácticas por cliente"]
    end

    subgraph PresentationLayer["Capa de Presentación (Frontend)"]
        GenDash["generator_dashboard.py\n- Motor de renderizado HTML\n- Tailwind CSS + Chart.js\n- Componentes interactivos"]
        DashHTML[("dashboard_clientes_vip.html\nDashboard Ejecutivo Autónomo")]
    end

    DB -->|SQLAlchemy / psycopg2| DBTool
    DBTool --> Agent
    Agent --> GenDash
    GenDash --> DashHTML
```

## 2. Componentes del Sistema

### 2.1 Base de Datos (Supabase PostgreSQL)
- **Tabla**: `fact_sales` (407.664 registros limpios del dataset Online Retail II).
- **Índices**: `idx_sales_date`, `idx_sales_customer`, `idx_sales_country`.

### 2.2 Herramienta de Acceso Analítico (`04_agente/tools/db_tool.py`)
- Implementa queries optimizadas para segmentar la base de clientes y calcular recencia (`days_inactive`), frecuencia (`order_count`) y valor monetario (`total_spent`).
- Extrae la cesta de productos más representativa de cada cliente VIP para personalizar las recomendaciones.

### 2.3 Agente de BI (`04_agente/agent.py`)
- Orquesta el pipeline analítico.
- Evalúa el perfil de compra (mayorista nacional vs internacional, frecuencia vs ticket medio).
- Genera un diagnóstico contextualizado del motivo de cese de compra.
- Formula **3 acciones accionables por cliente** categorizadas por canal, urgencia e impacto esperado.

### 2.4 Generador de Dashboard (`04_agente/generator_dashboard.py`)
- Produce un archivo HTML autocontenido (`04_agente/outputs/dashboard_clientes_vip.html`) con diseño moderno (Tailwind CSS, Chart.js, tipografía profesional y responsive design).

