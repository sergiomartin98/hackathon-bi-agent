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

    # 3. SKILL 1: Generar Frontend / Dashboard HTML
    print("\n" + "=" * 70)
    print("🎨 [SKILL 1] GENERANDO DASHBOARD INTERACTIVO (HTML)...")
    print("=" * 70)
    output_html = current_dir / "outputs" / "dashboard_clientes_vip.html"
    generate_html_dashboard(results, output_html)

    # 4. SKILL 2: Generar e Imprimir Documento PDF del Reporte
    print("\n" + "=" * 70)
    print("📄 [SKILL 2] GENERANDO DOCUMENTO PDF DEL REPORTE EJECUTIVO...")
    print("=" * 70)
    output_pdf = current_dir / "outputs" / "reporte_clientes_vip.pdf"
    pdf_res = agent.generate_pdf_report(output_html, output_pdf)

    print("\n" + "=" * 70)
    print("✅ CICLO DE HABILIDADES COMPLETADO EXITOSAMENTE")
    print("=" * 70)
    print(f"🌐 [Skill 1] Dashboard HTML:")
    print(f"   file:///{output_html.resolve()}")
    print(f"📑 [Skill 2] Documento PDF generado:")
    print(f"   file:///{output_pdf.resolve()} ({pdf_res['size_mb']} MB)")
    print("=" * 70)


if __name__ == "__main__":
    main()
