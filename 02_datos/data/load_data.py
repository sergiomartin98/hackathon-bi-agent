import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL no encontrada en el archivo .env")

# 1. Cargar archivo local
# Si tu archivo se llama diferente o es .csv, ajusta la ruta aquí:
file_path = "02_datos/data/online_retail_II.xlsx" 
print(f"Leyendo dataset desde {file_path}...")

if file_path.endswith('.xlsx'):
    df = pd.read_excel(file_path)
else:
    df = pd.read_csv(file_path, encoding='unicode_escape')

# 2. Limpieza analítica de Retail
print("Normalizando columnas y limpiando registros...")
df.columns = [c.strip().replace(" ", "_").lower() for c in df.columns]

# Eliminar nulos en clientes y compras canceladas/errores
df = df.dropna(subset=['customer_id'])
df['customer_id'] = df['customer_id'].astype(int)
df = df[(df['quantity'] > 0) & (df['price'] > 0)]
df['invoicedate'] = pd.to_datetime(df['invoicedate'])
df['total_amount'] = (df['quantity'] * df['price']).round(2)

# 3. Guardar muestra ligera (2.000 filas) para la entrega de GitHub
sample_path = "02_datos/data/online_retail_sample.csv"
df.head(2000).to_csv(sample_path, index=False)
print(f"Muestra ligera creada en: {sample_path}")

# 4. Ingesta por bloques en Supabase
print("Conectando con Supabase e insertando datos...")
engine = create_engine(DATABASE_URL)

# Subimos a la tabla 'fact_sales' en lotes de 5.000 registros para estabilidad
df.to_sql('fact_sales', engine, if_exists='replace', index=False, chunksize=5000)

# 5. Crear índices para optimizar las consultas del agente
print("Optimizando índices SQL...")
with engine.connect() as conn:
    conn.execute(text("CREATE INDEX IF NOT EXISTS idx_sales_date ON fact_sales(invoicedate);"))
    conn.execute(text("CREATE INDEX IF NOT EXISTS idx_sales_customer ON fact_sales(customer_id);"))
    conn.execute(text("CREATE INDEX IF NOT EXISTS idx_sales_country ON fact_sales(country);"))
    conn.commit()

print("¡Proceso completado con éxito! Tabla 'fact_sales' lista en Supabase.")