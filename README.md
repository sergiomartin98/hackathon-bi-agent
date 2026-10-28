# hackathon-bi-agent
> **Sistema Agéntico de BI para Retail basado en LLM, PostgreSQL (Supabase) y Generación Multi-formato (HTML y PDF).**

Este proyecto implementa un **Agente de Inteligencia de Negocios (BI)** especializado en la **detección proactiva de pérdida de actividad (*Churn*) en clientes valiosos (VIPs)** y la **generación de planes de acción prescriptivos**.

---

## 🎯 Habilidades (Skills) del Agente

### 🔹 Skill 1: Análisis Analítico de Attrition y Dashboard Interactivo (HTML)
1. **Análisis Integral**: Procesa las 407.664 transacciones de la tabla `fact_sales` (dataset *Online Retail II*) alojadas en PostgreSQL (Supabase).
2. **Detección de Pérdida de Actividad**: Identifica a los **5 clientes más valiosos** (por volumen de facturación y recurrencia de pedidos) que presentan una inactividad prolongada (> 60 días).
3. **Plan Prescriptivo de Ataque**: Formula **3 acciones tácticas concretas y personalizadas** por cada cliente (15 acciones en total), adaptadas a sus productos favoritos, ticket promedio y país.
4. **Dashboard Interactivo (HTML)**: Renderiza automáticamente un Dashboard ejecutivo (`04_agente/outputs/dashboard_clientes_vip.html`) con KPIs, gráficos interactivos con Chart.js y fichas de cliente.

### 🔹 Skill 2: Impresión y Exportación Ejecutiva en Documento PDF
1. **Motor de Renderizado Headless**: Integra `HTMLToPDFExporter` (`04_agente/tools/pdf_tool.py`), el cual utiliza el motor Chromium headless del sistema (Microsoft Edge / Google Chrome).
2. **Fidelidad Gráfica Completa**: Renderiza todos los scripts dinámicos (gráficos vectoriales de Chart.js, paletas de Tailwind CSS, tipografía ejecutiva e iconos).
3. **Paginación Inteligente**: Aplica directivas `@media print` y reglas CSS (`break-inside: avoid;`) para asegurar que las tarjetas de clientes y gráficos no se corten entre páginas.
4. **Salida Persistida**: Genera y guarda automáticamente el documento PDF en:
   `04_agente/outputs/reporte_clientes_vip.pdf`.

---

## 📂 Estructura del Repositorio

```text
hackathon-bi-agent/
│
├── 01_investigacion/
│   └── PROBLEMA_Y_MERCADO.md       # Justificación del negocio y modelo RFM
├── 02_datos/
│   ├── DICCIONARIO_DATOS.md        # Esquema de la tabla fact_sales
│   └── load_data.py                # Script ETL de carga a Supabase
├── 03_arquitectura/
│   └── ARQUITECTURA.md             # Diagrama de flujo y componentes (Skills 1 y 2)
├── 04_agente/                      # Implementación principal del agente
│   ├── tools/
│   │   ├── db_tool.py              # Queries analíticas y agregaciones SQL
│   │   └── pdf_tool.py             # Herramienta de conversión HTML a PDF (Skill 2)
│   ├── agent.py                    # Orquestador del agente con Skills 1 y 2
│   ├── generator_dashboard.py      # Motor de renderizado del frontend HTML
│   ├── main.py                     # Script ejecutable principal
│   └── outputs/
│       ├── dashboard_clientes_vip.html # Dashboard interactivo (Skill 1)
│       └── reporte_clientes_vip.pdf    # Reporte impreso en PDF (Skill 2)
├── 05_pruebas/
│   └── CASOS_DE_PRUEBA.md          # Pruebas y validación de ambas habilidades
├── .env.example                    # Plantilla de configuración de credenciales
├── .gitignore                      # Excluye .env y datos locales confidenciales
├── ejecutar_agente.bat             # ⚡ Lanzador ejecutable autónomo (Doble clic)
├── requirements.txt                # Dependencias del proyecto
├── README.md
└── REFLEXION.md                    # Aprendizajes y roadmap futuro
```

---

## 🚀 Cómo Ejecutar el Agente

### Paso Previo: Configurar Credenciales
1. Copia el archivo `.env.example` y renómbralo como `.env`.
2. Introduce tu contraseña de la base de datos Supabase en `DATABASE_URL`.

### Opción A: Modo Rápido (1 solo clic - Sin abrir VS Code) ⚡
1. Abre la carpeta del proyecto en el Explorador de Archivos de Windows.
2. Haz **doble clic en el archivo [`ejecutar_agente.bat`](file:///C:/Users/fjlimam/Downloads/Proy%20agente%20no2/hackathon-bi-agent/ejecutar_agente.bat)**.
3. El script automáticamente:
   * Verifica la instalación de Python.
   * Valida e instala dependencias faltantes desde `requirements.txt`.
   * Ejecuta el agente analítico (Skill 1 y Skill 2).
   * Pregunta si deseas abrir directamente el Dashboard HTML interactivo y el PDF en tu navegador.

### Opción B: Desde la Terminal
```bash
# Instalar dependencias (solo primera vez)
pip install -r requirements.txt

# Ejecutar el agente
python 04_agente/main.py
```
