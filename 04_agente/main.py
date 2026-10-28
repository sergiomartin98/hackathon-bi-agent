import sys
from pathlib import Path

# Configurar encoding seguro para consola de Windows
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Agregar directorio actual al sys.path para importaciones relativas
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from agent import BIAgentCustomerRetention
from generator_dashboard import generate_html_dashboard


def main():
    print("=" * 70)
    print("🚀 EJECUTANDO AGENTE DE INTELIGENCIA DE NEGOCIOS (BI RETAIL)")
    print("=" * 70)

    # 1. Instanciar y ejecutar el agente analítico
    # Usamos un umbral de 60 días para detectar cese significativo de actividad
    agent = BIAgentCustomerRetention(inactivity_threshold_days=60)
    results = agent.run_analysis()

    # 2. Resumen ejecutivo en consola
    overview = results["overview"]
    vips = results["top_vip_churned"]

    print("\n" + "-" * 70)
    print("📊 RESULTADOS DEL ANÁLISIS")
    print("-" * 70)
    print(f"Total registros analizados: {overview['total_rows']:,}")
    print(f"Total clientes analizados:  {overview['total_customers']:,}")
    print(f"Facturación global:         £{overview['total_revenue']:,.2f}")
    print(f"Facturación VIP en riesgo:  £{overview['vip_lost_revenue']:,.2f}")
    print("-" * 70)

    print("\n🚨 TOP 5 CLIENTES VALIOSOS CON PÉRDIDA DE ACTIVIDAD:")
    for idx, vip in enumerate(vips, 1):
        print(f"\n{idx}. Cliente #{vip['customer_id']} ({vip['country']})")
        print(f"   - Gasto Total:       £{vip['total_spent']:,.2f}")
        print(f"   - Pedidos:           {vip['total_orders']} (Ticket prom: £{vip['avg_ticket']:,.2f})")
        print(f"   - Días Inactivo:     {vip['days_inactive']} días (Última compra: {vip['last_order']})")
        print("   - 3 Acciones propuestas:")
        for a_idx, act in enumerate(vip["actions"], 1):
            print(f"      {a_idx}) {act['title']} [{act['urgency']}]")

    # 3. Generar Frontend / Dashboard HTML
    output_html = current_dir / "outputs" / "dashboard_clientes_vip.html"
    generate_html_dashboard(results, output_html)

    print("\n" + "=" * 70)
    print(f"✅ PROCESO COMPLETADO EXITOSAMENTE")
    print(f"🌐 Abre el Dashboard HTML en tu navegador:")
    print(f"   file:///{output_html.resolve()}")
    print("=" * 70)


if __name__ == "__main__":
    main()
