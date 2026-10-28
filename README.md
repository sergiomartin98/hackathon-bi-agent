# hackathon-bi-agent
> **Sistema Agéntico de BI para Retail basado en LLM, PostgreSQL (Supabase) y Frontend Interactivo.**

Este proyecto implementa un **Agente de Inteligencia de Negocios (BI)** especializado en la **detección proactiva de pérdida de actividad (*Churn*) en clientes valiosos (VIPs)** y la **generación de planes de acción prescriptivos**.

---

## 🎯 Skill del Agente
1. **Análisis Integral**: Procesa las 407.664 transacciones de la tabla `fact_sales` (dataset *Online Retail II*) alojadas en PostgreSQL (Supabase).
2. **Detección de Pérdida de Actividad**: Identifica a los **5 clientes más valiosos** (por volumen de facturación y recurrencia de pedidos) que presentan una inactividad prolongada (> 60 días).
3. **Plan Prescriptivo de Ataque**: Formula **3 acciones tácticas concretas y personalizadas** por cada cliente (15 acciones en total), adaptadas a sus productos favoritos, ticket promedio y país.
4. **Frontend / Dashboard HTML**: Renderiza automáticamente un Dashboard ejecutivo e interactivo (`dashboard_clientes_vip.html`) con KPIs, gráficos con Chart.js y fichas individuales de cada cliente.

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
│   └── ARQUITECTURA.md             # Diagrama de flujo y componentes
├── 04_agente/                      # Implementación principal del agente
│   ├── tools/
│   │   └── db_tool.py              # Queries analíticas y agregaciones SQL
│   ├── agent.py                    # Lógica del agente y prescripción estratégica
│   ├── generator_dashboard.py      # Motor de renderizado del frontend HTML
│   ├── main.py                     # Script ejecutable principal
│   └── outputs/
│       └── dashboard_clientes_vip.html # Dashboard interactivo generado
├── 05_pruebas/
│   └── CASOS_DE_PRUEBA.md          # Pruebas y validación de resultados
├── .env                            # Credenciales de conexión a PostgreSQL
├── .gitignore
├── README.md
└── REFLEXION.md                    # Aprendizajes y roadmap futuro
```

---

## 🚀 Cómo Ejecutar el Agente

1. **Configurar el entorno**:
   Asegúrate de tener instaladas las dependencias:
   ```bash
   pip install psycopg2-binary sqlalchemy python-dotenv pandas
   ```

2. **Ejecutar el agente**:
   ```bash
   python 04_agente/main.py
   ```

3. **Visualizar el Frontend / Dashboard**:
   Abre directamente en tu navegador el archivo generado:
   `04_agente/outputs/dashboard_clientes_vip.html`
