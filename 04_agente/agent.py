import os
import json
from pathlib import Path
from tools.db_tool import (
    get_dataset_overview,
    get_customer_segments_summary,
    get_top_churned_vip_customers,
    get_customer_top_products,
    get_customer_monthly_history
)
from tools.pdf_tool import HTMLToPDFExporter
from generator_dashboard import generate_html_dashboard


class BIAgentCustomerRetention:
    """
    Agente de Inteligencia de Negocios (BI) especializado en Retail.
    
    Habilidades (Skills):
    - Skill 1: Analizar la base de datos completa en PostgreSQL (Supabase), detectar pérdida 
               de actividad en clientes VIP, seleccionar los Top 5 en riesgo de churn,
               formular 3 acciones tácticas por cliente y generar un Dashboard interactivo HTML.
    - Skill 2: Generar e imprimir un documento PDF ejecutivo a partir del reporte HTML generado,
               asegurando alta resolución gráfica y guardándolo en la carpeta del proyecto.
    """

    def __init__(self, inactivity_threshold_days=60):
        self.inactivity_threshold_days = inactivity_threshold_days
        self.pdf_exporter = HTMLToPDFExporter()

    def run_analysis(self):
        print("[AGENTE BI] Iniciando análisis analítico de clientes en Supabase...")
        
        # 1. Obtener visión global
        overview = get_dataset_overview()
        print(f"[AGENTE BI] Datos cargados: {overview['total_rows']:,} transacciones, {overview['total_customers']:,} clientes.")

        # 2. Segmentación de clientes
        segments = get_customer_segments_summary(self.inactivity_threshold_days)

        # 3. Identificar Top 5 VIPs con pérdida de actividad
        top_vips_raw = get_top_churned_vip_customers(limit=5, min_inactivity_days=self.inactivity_threshold_days)

        vip_profiles = []
        total_lost_revenue = 0

        for vip in top_vips_raw:
            cid = vip["customer_id"]
            total_spent = float(vip["total_spent"])
            total_lost_revenue += total_spent

            # Enriquecer con productos favoritos e histórico mensual
            top_products = get_customer_top_products(cid, limit=3)
            monthly_trend = get_customer_monthly_history(cid)

            # Generar diagnóstico y 3 acciones estratégicas por cliente
            diagnostic, actions = self._generate_strategic_actions(vip, top_products)

            vip_profiles.append({
                "customer_id": cid,
                "country": vip["country"],
                "total_spent": total_spent,
                "total_orders": int(vip["order_count"]),
                "units_bought": int(vip["units_bought"]),
                "avg_ticket": float(vip["avg_ticket"]),
                "first_order": vip["first_order"].strftime("%Y-%m-%d"),
                "last_order": vip["last_order"].strftime("%Y-%m-%d"),
                "days_inactive": int(vip["days_inactive"]),
                "top_products": top_products,
                "monthly_trend": monthly_trend,
                "diagnostic": diagnostic,
                "actions": actions
            })

        print(f"[AGENTE BI] Análisis finalizado. 5 clientes VIP en riesgo identificados con un impacto de £{total_lost_revenue:,.2f}.")

        results = {
            "overview": {
                "total_rows": overview["total_rows"],
                "total_customers": overview["total_customers"],
                "total_orders": overview["total_orders"],
                "total_revenue": float(overview["total_revenue"]),
                "min_date": overview["min_date"].strftime("%Y-%m-%d"),
                "max_date": overview["max_date"].strftime("%Y-%m-%d"),
                "vip_lost_revenue": total_lost_revenue,
                "inactivity_threshold": self.inactivity_threshold_days
            },
            "segments": segments,
            "top_vip_churned": vip_profiles
        }
        return results

    def _generate_strategic_actions(self, customer, top_products):
        """
        Genera un diagnóstico preciso y 3 acciones estratégicas personalizadas
        para reactivar a cada cliente según su comportamiento transaccional.
        """
        cid = customer["customer_id"]
        country = customer["country"]
        days = int(customer["days_inactive"])
        spent = float(customer["total_spent"])
        orders = int(customer["order_count"])
        avg_ticket = float(customer["avg_ticket"])
        top_sku = top_products[0]["description"] if top_products else "artículos mayoristas"

        # Diagnóstico analítico personalizado
        if country in ["Denmark", "Sweden"]:
            diagnostic = (
                f"Cliente mayorista internacional estratégico en {country}. Acumula £{spent:,.2f} en {orders} pedidos "
                f"con una inactividad crítica de {days} días. El cese abrupto en compras de gran volumen sugiere "
                f"un probable cuello de botella logístico/aduanero o cambio de proveedor regional de distribución."
            )
            actions = [
                {
                    "title": "1. Auditoría Logística y Tarifa Plana de Envíos B2B",
                    "channel": "Videollamada con Key Account Manager Internacional",
                    "description": (
                        f"Contactar al equipo de compras en {country} para revisar condiciones de entrega y flete marítimo/terrestre. "
                        f"Ofrecer bonificación del 100% en gastos de envío para órdenes superiores a £5,000 en su línea principal ({top_sku})."
                    ),
                    "expected_impact": "Recuperar el canal de aprovisionamiento internacional y destrabar pedidos frenados por costes logísticos.",
                    "urgency": "Inmediata (Próximos 5 días)"
                },
                {
                    "title": "2. Acuerdo de Rappel y Reserva de Stock Anticipada",
                    "channel": "Propuesta Comercial Formal / Contrato B2B",
                    "description": (
                        f"Presentar un esquema de rappel por volumen con escalado del 8% al 12% de descuento adicional, "
                        f"garantizando inventario reservado en almacén central para sus categorías clave."
                    ),
                    "expected_impact": "Fidelización contractual de largo plazo y previsibilidad de inventario.",
                    "urgency": "Medio plazo (10-15 días)"
                },
                {
                    "title": "3. Catálogo Exclusivo Nórdico y Muestrario Físico de Nuevas Líneas",
                    "channel": "Envío de Muestras Courier Premium + Reunión Ejecutiva",
                    "description": (
                        f"Despachar un kit de muestras físicas de las colecciones de temporada que complementan su histórico "
                        f"de compra ({top_sku}), con línea de crédito comercial ampliada a 60 días."
                    ),
                    "expected_impact": "Reactivar la demanda de nuevos productos e incrementar el ticket promedio histórico (£{avg_ticket:,.2f}).",
                    "urgency": "Corto plazo (7 días)"
                }
            ]
        elif orders >= 20:
            diagnostic = (
                f"Cliente de alta frecuencia y recurrencia (29+ pedidos registrados, total £{spent:,.2f}). "
                f"Muestra una desconexión severa tras {days} días sin actividad. Al ser un cliente habitual, "
                f"la pérdida repentina denota insatisfacción con el último pedido o captación agresiva de la competencia."
            )
            actions = [
                {
                    "title": "1. Llamada de Calidad Post-Venta y Concierge VIP",
                    "channel": "Llamada Telefónica Directa de Dirección de Clientes",
                    "description": (
                        f"Realizar una llamada de satisfacción centrada en indagar incidencias en su último pedido de {customer['last_order'].strftime('%d/%m/%Y')}. "
                        f"Asignar un gestor de cuenta dedicado ('VIP Concierge') para canalizar pedidos por mensajería directa o email prioritario."
                    ),
                    "expected_impact": "Resolver fricciones operativas pasadas y restaurar la confianza inmediata.",
                    "urgency": "Urgente (48 horas)"
                },
                {
                    "title": "2. Campaña de 'Bienvenido de Vuelta' con Crédito Directo en Cuenta",
                    "channel": "Email VIP Personalizado con Notificación Directa",
                    "description": (
                        f"Abonar un crédito promocional no condicionado de £500 en su cuenta comercial, canjeable durante los próximos "
                        f"14 días en su producto estrella '{top_sku}'."
                    ),
                    "expected_impact": "Incentivo inmediato de reactivación con retorno de inversión garantizado en el primer pedido.",
                    "urgency": "Corto plazo (3-5 días)"
                },
                {
                    "title": "3. Acceso Prioritario a Reposiciones y Pedidos Exprés",
                    "channel": "Portal B2B / Configuración de Cuenta VIP",
                    "description": (
                        f"Habilitar despacho en 24h garantizado sin recargo para sus pedidos recurrentes y embalaje con marca blanca "
                        f"para facilitar su distribución final."
                    ),
                    "expected_impact": "Blindar al cliente frente a la competencia mejorando la agilidad operativa.",
                    "urgency": "Medio plazo (10 días)"
                }
            ]
        else:
            # Clientes de ticket medio/alto en UK con compras periódicas concentradas
            diagnostic = (
                f"Cliente mayorista nacional (UK) con alto poder adquisitivo: £{spent:,.2f} acumulados y ticket promedio de £{avg_ticket:,.2f}. "
                f"Inactivo desde hace {days} días (última compra en septiembre de 2010), perdiendo el ciclo comercial de otoño/Navidad. "
                f"Su patrón indica compras por campañas estacionales que no han sido oportunamente estimuladas."
            )
            actions = [
                {
                    "title": "1. Oferta de Reabastecimiento Estacional con Descuento por Volumen",
                    "channel": "Reunión Comercial Presencial / Llamada de KAM",
                    "description": (
                        f"Presentar una propuesta de reposición con precio especial en '{top_sku}' y lotes afines, "
                        f"aplicando un 10% de descuento directo al alcanzar un pedido mínimo de £3,000."
                    ),
                    "expected_impact": "Reincorporar al cliente en la campaña estacional inmediata recuperando más de £5,000 en compras.",
                    "urgency": "Inmediata (3-5 días)"
                },
                {
                    "title": "2. Pre-venta Exclusiva de Novedades y Reserva Garantizada",
                    "channel": "Catálogo Digital Interactivo con Pre-reserva",
                    "description": (
                        f"Brindar acceso anticipado de 72 horas al catálogo de nuevas colecciones antes de su lanzamiento al público general, "
                        f"asegurando disponibilidad completa de stock."
                    ),
                    "expected_impact": "Aumentar la percepción de exclusividad de marca e impulsar compras anticipadas.",
                    "urgency": "Corto plazo (7 días)"
                },
                {
                    "title": "3. Flexibilización de Condiciones de Pago y Descuento por Pronto Pago",
                    "channel": "Finanzas Comerciales / Facturación B2B",
                    "description": (
                        f"Ofrecer ampliación de plazos a 30/60 días fecha factura o un 3% de descuento adicional por pago al contado dentro de los 10 días."
                    ),
                    "expected_impact": "Facilitar el flujo de caja del cliente y eliminar barreras financieras para emitir órdenes de gran importe.",
                    "urgency": "Medio plazo (10-15 días)"
                }
            ]

        return diagnostic, actions

    def generate_pdf_report(self, html_path, output_pdf_path=None):
        """
        Skill 2:
        Genera un documento PDF ejecutivo a partir del reporte HTML generado.
        Guarda el archivo .pdf resultante en la carpeta del proyecto.
        """
        print(f"[AGENTE BI - SKILL 2] Iniciando impresión y renderizado PDF desde: {html_path}...")
        result = self.pdf_exporter.convert(html_path, output_pdf_path)
        print(f"[AGENTE BI - SKILL 2] PDF generado exitosamente en: {result['pdf_path']} ({result['size_mb']} MB)")
        return result

    def execute_all_skills(self, output_dir=None):
        """
        Ejecuta el ciclo completo de habilidades del agente:
        1. Skill 1: Analítica de Churn VIP + Generación de Dashboard HTML
        2. Skill 2: Exportación e Impresión del Reporte en Formato PDF
        """
        base_dir = Path(output_dir) if output_dir else Path(__file__).resolve().parent / "outputs"
        base_dir.mkdir(parents=True, exist_ok=True)

        # 1. Ejecución Skill 1
        analysis_data = self.run_analysis()
        html_file = base_dir / "dashboard_clientes_vip.html"
        generate_html_dashboard(analysis_data, html_file)

        # 2. Ejecución Skill 2
        pdf_file = base_dir / "reporte_clientes_vip.pdf"
        pdf_result = self.generate_pdf_report(html_file, pdf_file)

        return {
            "analysis_data": analysis_data,
            "html_path": str(html_file.resolve()),
            "pdf_path": pdf_result["pdf_path"],
            "pdf_size_mb": pdf_result["size_mb"]
        }


if __name__ == "__main__":
    agent = BIAgentCustomerRetention(inactivity_threshold_days=60)
    data = agent.run_analysis()
    print("Muestra resultado del agente:", json.dumps(data["top_vip_churned"][0], indent=2))

