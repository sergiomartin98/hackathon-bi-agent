import os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Cargar variables de entorno
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError(f"DATABASE_URL no encontrada en {env_path}")

engine = create_engine(DATABASE_URL)


def get_dataset_overview():
    """Obtiene métricas globales del dataset fact_sales."""
    query = text("""
        SELECT 
            COUNT(*) AS total_rows,
            COUNT(DISTINCT customer_id) AS total_customers,
            COUNT(DISTINCT invoice) AS total_orders,
            ROUND(SUM(total_amount)::numeric, 2) AS total_revenue,
            MIN(invoicedate) AS min_date,
            MAX(invoicedate) AS max_date
        FROM fact_sales
        WHERE customer_id IS NOT NULL;
    """)
    with engine.connect() as conn:
        res = conn.execute(query).fetchone()
        return dict(res._mapping)


def get_customer_segments_summary(inactivity_threshold_days=60):
    """Segmenta a los clientes según su actividad y valor."""
    query = text(f"""
        WITH customer_stats AS (
            SELECT 
                customer_id,
                country,
                COUNT(DISTINCT invoice) AS order_count,
                SUM(quantity) AS units_bought,
                ROUND(SUM(total_amount)::numeric, 2) AS total_spent,
                MIN(invoicedate) AS first_order,
                MAX(invoicedate) AS last_order,
                ROUND(EXTRACT(EPOCH FROM ((SELECT MAX(invoicedate) FROM fact_sales) - MAX(invoicedate))) / 86400) AS days_inactive
            FROM fact_sales
            WHERE customer_id IS NOT NULL
            GROUP BY customer_id, country
        )
        SELECT 
            CASE 
                WHEN days_inactive <= 30 THEN 'Activo (0-30 d)'
                WHEN days_inactive <= {inactivity_threshold_days} THEN 'En Riesgo (31-60 d)'
                ELSE 'Inactivo / Churn (>60 d)'
            END AS activity_status,
            COUNT(*) AS customer_count,
            ROUND(SUM(total_spent)::numeric, 2) AS revenue_segment,
            ROUND(AVG(total_spent)::numeric, 2) AS avg_spent_per_customer
        FROM customer_stats
        GROUP BY 1
        ORDER BY customer_count DESC;
    """)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
        return df.to_dict(orient="records")


def get_top_churned_vip_customers(limit=5, min_inactivity_days=60):
    """
    Identifica a los N clientes más valiosos (por volumen de gasto o frecuencia de compras)
    que han cesado su actividad de compra por encima del umbral de días.
    """
    query = text(f"""
        WITH customer_stats AS (
            SELECT 
                customer_id,
                country,
                COUNT(DISTINCT invoice) AS order_count,
                SUM(quantity) AS units_bought,
                ROUND(SUM(total_amount)::numeric, 2) AS total_spent,
                ROUND((SUM(total_amount) / NULLIF(COUNT(DISTINCT invoice), 0))::numeric, 2) AS avg_ticket,
                MIN(invoicedate) AS first_order,
                MAX(invoicedate) AS last_order,
                ROUND(EXTRACT(EPOCH FROM ((SELECT MAX(invoicedate) FROM fact_sales) - MAX(invoicedate))) / 86400) AS days_inactive
            FROM fact_sales
            WHERE customer_id IS NOT NULL
            GROUP BY customer_id, country
        )
        SELECT *
        FROM customer_stats
        WHERE days_inactive >= {min_inactivity_days}
        ORDER BY total_spent DESC
        LIMIT {limit};
    """)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
        return df.to_dict(orient="records")


def get_customer_top_products(customer_id, limit=4):
    """Obtiene los productos favoritos más adquiridos por un cliente."""
    query = text(f"""
        SELECT 
            description,
            SUM(quantity) AS total_units,
            ROUND(SUM(total_amount)::numeric, 2) AS total_spent
        FROM fact_sales
        WHERE customer_id = :cid
        GROUP BY description
        ORDER BY total_spent DESC
        LIMIT {limit};
    """)
    with engine.connect() as conn:
        res = conn.execute(query, {"cid": customer_id}).fetchall()
        return [dict(r._mapping) for r in res]


def get_customer_monthly_history(customer_id):
    """Obtiene la serie temporal mensual de compras para graficar la pérdida de actividad."""
    query = text(f"""
        SELECT 
            TO_CHAR(invoicedate, 'YYYY-MM') AS month,
            COUNT(DISTINCT invoice) AS orders,
            ROUND(SUM(total_amount)::numeric, 2) AS spend
        FROM fact_sales
        WHERE customer_id = :cid
        GROUP BY 1
        ORDER BY 1;
    """)
    with engine.connect() as conn:
        res = conn.execute(query, {"cid": customer_id}).fetchall()
        return [dict(r._mapping) for r in res]


if __name__ == "__main__":
    overview = get_dataset_overview()
    print("Dataset Overview:", overview)
    vips = get_top_churned_vip_customers(5)
    print(f"Top {len(vips)} VIPs en riesgo:")
    for v in vips:
        print(v["customer_id"], v["country"], v["total_spent"], v["days_inactive"])

