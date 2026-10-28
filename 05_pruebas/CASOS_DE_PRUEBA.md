# 05. Casos de Prueba y Validación

## 1. Matriz de Casos de Prueba

| ID | Componente / Caso | Objetivo de la Prueba | Resultado Esperado | Estado |
|---|---|---|---|---|
| **CP-01** | Conectividad a Supabase | Validar cadena de conexión `DATABASE_URL` y acceso a PostgreSQL | Conexión establecida con éxito en pooler 5432 | **APROBADO** |
| **CP-02** | Integridad de `fact_sales` | Comprobar volumen total y no nulidad de clientes | 407.664 registros válidos entre 2009 y 2010 | **APROBADO** |
| **CP-03** | Cálculo de Recencia e Inactividad | Determinar días transcurridos desde la última compra de cada cliente respecto al corte del dataset | Días calculados con precisión numérica | **APROBADO** |
| **CP-04** | Detección de Top 5 VIPs con Churn | Identificar las 5 cuentas de mayor valor con inactividad > 60 días | Identificados clientes 13902, 17940, 12482, 14063, 18251 (£128,747.75 en riesgo) | **APROBADO** |
| **CP-05** | Prescripción de Acciones Tácticas | Verificar que el agente genera exactamente 3 acciones personalizadas por cliente | 15 acciones generadas con canal, urgencia e impacto | **APROBADO** |
| **CP-06** | Generación del Frontend HTML | Renderizar el archivo HTML con Tailwind CSS y Chart.js | Archivo `dashboard_clientes_vip.html` de ~78 KB funcional y navegable | **APROBADO** |

## 2. Comprobación de Resultados Clave
- **Cliente #13902 (Dinamarca)**: Gasto £34,095.26 | 267 días inactivo | Acciones: Auditoría logística nórdica, rappel B2B y catálogo físico.
- **Cliente #17940 (UK)**: Gasto £26,286.75 | 80 días inactivo | Acciones: Oferta reposición estacional, pre-venta exclusiva y flexibilidad financiera.
- **Cliente #12482 (Suecia)**: Gasto £23,691.40 | 211 días inactivo | Acciones: Concierge post-venta, resolución de incidencias y tarifa plana de envío.
- **Cliente #14063 (UK)**: Gasto £22,710.20 | 73 días inactivo | Acciones: Paquete VIP de reposición con descuento por volumen.
- **Cliente #18251 (UK)**: Gasto £21,964.14 | 80 días inactivo | Acciones: Campaña de fidelización y crédito directo.

