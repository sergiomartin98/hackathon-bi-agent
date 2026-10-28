# Diccionario de Datos: fact_sales (Online Retail II)

| Columna | Tipo | Descripción |
|---|---|---|
| `invoice` | TEXT | Código identificador de la transacción |
| `stockcode` | TEXT | Código identificador del producto |
| `description` | TEXT | Nombre o descripción del producto |
| `quantity` | INTEGER | Unidades vendidas |
| `invoicedate` | TIMESTAMP | Fecha y hora de compra |
| `price` | NUMERIC | Precio unitario del artículo |
| `customer_id` | INTEGER | Identificador único del cliente |
| `country` | TEXT | País del cliente |
| `total_amount` | NUMERIC | Importe total calculado (quantity * price) |