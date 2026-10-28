# 01. Investigación: Problema de Negocio y Mercado

## 1. Planteamiento del Problema
En el sector minorista y de distribución mayorista (*Retail / E-commerce*), la pérdida de clientes estratégicos (*Customer Attrition / Churn*) representa una de las mayores fugas de rentabilidad:
- **Efecto Pareto (80/20)**: Menos del 15% de la base de clientes suele representar más del 60% del volumen de facturación y margen neto.
- **Coste de Adquisición vs Retención**: Retener o reactivar a una cuenta VIP existente es entre **5 y 7 veces más económico** que adquirir un nuevo cliente con un volumen de compra equivalente.
- **Riesgo Silencioso**: A diferencia de los modelos de suscripción (donde el cliente cancela explícitamente), en retail la fuga ocurre de manera silenciosa: el cliente simplemente espacia o deja de emitir órdenes de compra.

## 2. Definición de Cliente Valioso
Para este sistema agéntico, se define como **Cliente Valioso** aquel que destaca en dos dimensiones analíticas clave:
1. **Valor Monetario Total (*Monetary Value*)**: Clientes en el percentil superior de facturación histórica acumulada.
2. **Volumen y Frecuencia de Compra (*Frequency / Order Volume*)**: Clientes con alta recurrencia de pedidos y volumen de unidades adquiridas.

## 3. Justificación de la Solución Agéntica
Los cuadros de mando tradicionales de BI suelen ser estáticos y meramente descriptivos. La incorporación de un **Agente de BI** aporta:
- **Detección Dinámica**: Identificación autónoma de umbrales anómalos de inactividad (recencia > 60 días) en cuentas de alto valor.
- **Prescripción Accionable**: En lugar de mostrar solo números, el agente formula **3 acciones comerciales específicas y tácticas** por cada cliente en riesgo, personalizadas en base a su cesta de compra y país.
- **Presentación Ejecutiva**: Entrega los resultados en un Dashboard interactivo (HTML) con foco en la toma inmediata de decisiones.

