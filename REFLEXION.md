# Reflexión y Aprendizajes del Proyecto

## 1. Desafíos Técnicos Afrontados
1. **Volumen de Datos y Rendimiento**:
   - Trabajar con más de 400.000 registros en una base de datos remota en la nube requirió diseñar consultas analíticas eficientes en PostgreSQL con agregaciones en origen (`WITH customer_stats AS ...`), evitando traer datos masivos sin procesar a la memoria local.
2. **Definición de "Pérdida de Actividad" en Retail B2B**:
   - A diferencia de clientes finales (B2C) que compran semanalmente, los distribuidores mayoristas de Retail operan por ciclos de reaprovisionamiento. Establecer un umbral de inactividad de más de 60 días combinado con el análisis de caída de frecuencia permitió distinguir clientes con compras estacionales de aquellos en riesgo real de fuga.
3. **De la Analítica Descriptiva a la Prescriptiva**:
   - El mayor salto cualitativo de este agente es que no se limita a mostrar "cuánto se ha perdido", sino que investiga la cesta de compra particular de cada cliente y prescribe un plan táctico de 3 pasos listo para ser ejecutado por el equipo comercial.

## 2. Próximas Mejoras y Escalabilidad
- **Automatización de Disparadores (Triggers)**: Conectar el agente a un webhook o cron job para que, en cuanto un cliente supere su intervalo medio de compra en un factor de 1.5x, se envíe una alerta automática por Slack o Email al gestor de cuenta.
- **Integración con CRM**: Exportar las 3 acciones propuestas directamente como tareas asignadas en HubSpot o Salesforce.

