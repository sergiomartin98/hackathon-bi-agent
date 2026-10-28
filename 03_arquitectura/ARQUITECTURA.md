# 03. Arquitectura del Sistema Agéntico de BI

## 1. Diagrama de Arquitectura Multihabilidad

```mermaid
flowchart TD
    subgraph DataLayer["Capa de Datos"]
        DB[("PostgreSQL en Supabase\nTabla: fact_sales\n407,664 registros")]
    end

    subgraph ToolLayer["Capa de Herramientas (Tools)"]
        DBTool["db_tool.py\n- SQL Queries analíticas\n- Cálculo RFM\n- Filtro Churn (>60 días)\n- Historial y Top SKUs"]
        PDFTool["pdf_tool.py (Skill 2)\n- Chromium Headless Engine\n- Impresión PDF ejecutiva\n- Renderizado de gráficos Chart.js"]
    end

    subgraph AgentLayer["Capa de Inteligencia y Agente"]
        Agent["BIAgentCustomerRetention (agent.py)\n- Orquestador Multihabilidad\n- Detección de Top 5 VIPs en riesgo\n- Motor de diagnóstico comercial\n- Formulación de 3 acciones tácticas por cliente\n- Coordinación de exportaciones"]
    end

    subgraph PresentationLayer["Capa de Entregables (Outputs)"]
        GenDash["generator_dashboard.py\n- Renderizador HTML + CSS Tailwind\n- Inyección de Chart.js"]
        DashHTML[("dashboard_clientes_vip.html\nSkill 1: Dashboard HTML Interactivo")]
        ReportPDF[("reporte_clientes_vip.pdf\nSkill 2: Documento PDF Ejecutivo")]
    end

    DB -->|SQLAlchemy / psycopg2| DBTool
    DBTool --> Agent
    Agent -->|Skill 1| GenDash
    GenDash --> DashHTML
    DashHTML -->|Skill 2: Entrada HTML| PDFTool
    PDFTool --> ReportPDF
```

## 2. Componentes del Sistema

### 2.1 Base de Datos (Supabase PostgreSQL)
- **Tabla**: `fact_sales` (407.664 registros limpios del dataset Online Retail II).
- **Índices**: `idx_sales_date`, `idx_sales_customer`, `idx_sales_country`.

### 2.2 Herramienta de Acceso Analítico (`04_agente/tools/db_tool.py`)
- Implementa queries optimizadas para segmentar la base de clientes y calcular recencia (`days_inactive`), frecuencia (`order_count`) y valor monetario (`total_spent`).
- Extrae la cesta de productos más representativa de cada cliente VIP para personalizar las recomendaciones.

### 2.3 Agente de BI (`04_agente/agent.py`)
- Orquesta ambas habilidades (Skill 1 y Skill 2).
- Evalúa el perfil de compra (mayorista nacional vs internacional, frecuencia vs ticket medio).
- Genera un diagnóstico contextualizado del motivo de cese de compra.
- Formula **3 acciones accionables por cliente** categorizadas por canal, urgencia e impacto esperado.

### 2.4 Generador de Dashboard HTML (`04_agente/generator_dashboard.py`)
- Produce un archivo HTML autocontenido (`04_agente/outputs/dashboard_clientes_vip.html`) con diseño moderno (Tailwind CSS, Chart.js, tipografía profesional y responsive design).
- Incorpora directivas `@media print` y reglas CSS `break-inside: avoid;` para garantizar saltos de página limpios.

### 2.5 Motor de Exportación a PDF (`04_agente/tools/pdf_tool.py` - Skill 2)
- Utiliza Chromium Headless nativo (`msedge.exe` / `chrome.exe`) con flags optimizados para esperar la compilación de scripts JS antes de la captura.
- Produce el archivo PDF listo para su distribución ejecutiva o impresión formal: `04_agente/outputs/reporte_clientes_vip.pdf`.
