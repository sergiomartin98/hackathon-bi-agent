import json
from pathlib import Path


def generate_html_dashboard(data, output_path):
    """
    Genera un Dashboard ejecutivo e interactivo en formato HTML
    con Tailwind CSS, Chart.js y componentes visuales para presentar
    los insights del agente de BI.
    """
    overview = data["overview"]
    segments = data["segments"]
    vips = data["top_vip_churned"]

    # Preparar datos para Chart.js
    segment_labels = [s["activity_status"] for s in segments]
    segment_counts = [s["customer_count"] for s in segments]
    segment_revenues = [float(s["revenue_segment"]) for s in segments]

    vip_labels = [f"ID {v['customer_id']} ({v['country']})" for v in vips]
    vip_spends = [v["total_spent"] for v in vips]
    vip_inactivity = [v["days_inactive"] for v in vips]

    # Renderizar tarjetas de los Top 5 Clientes
    vip_cards_html = ""
    for idx, vip in enumerate(vips, 1):
        # Productos favoritos
        products_html = ""
        for p in vip["top_products"]:
            products_html += f"""
            <div class="flex items-center justify-between text-sm py-1.5 border-b border-slate-100 last:border-0">
                <span class="text-slate-700 font-medium truncate max-w-xs" title="{p['description']}">
                    📦 {p['description']}
                </span>
                <span class="text-slate-500 font-semibold whitespace-nowrap">
                    {p['total_units']:,} unids &bull; £{float(p['total_spent']):,.2f}
                </span>
            </div>
            """

        # 3 Acciones estratégicas
        actions_html = ""
        for a_idx, act in enumerate(vip["actions"], 1):
            badge_color = "bg-amber-100 text-amber-800 border-amber-200" if "Urgente" in act["urgency"] or "Inmediata" in act["urgency"] else "bg-blue-100 text-blue-800 border-blue-200"
            actions_html += f"""
            <div class="bg-slate-50 rounded-xl p-4 border border-slate-200 hover:border-indigo-400 transition-all shadow-sm">
                <div class="flex flex-wrap items-center justify-between gap-2 mb-2">
                    <h5 class="font-bold text-slate-800 text-sm flex items-center gap-1.5">
                        <span class="w-6 h-6 rounded-full bg-indigo-600 text-white flex items-center justify-center text-xs font-bold">{a_idx}</span>
                        {act['title']}
                    </h5>
                    <span class="text-xs px-2.5 py-0.5 rounded-full font-semibold border {badge_color}">
                        ⏱ {act['urgency']}
                    </span>
                </div>
                <p class="text-xs text-indigo-700 font-semibold mb-2">
                    🎯 Canal sugerido: <span class="text-slate-700 font-normal">{act['channel']}</span>
                </p>
                <p class="text-xs text-slate-600 leading-relaxed mb-3">
                    {act['description']}
                </p>
                <div class="bg-white rounded-lg p-2.5 border border-slate-200 text-xs text-emerald-800 flex items-start gap-1.5">
                    <span class="font-bold text-emerald-600">📈 Impacto:</span>
                    <span>{act['expected_impact']}</span>
                </div>
            </div>
            """

        vip_cards_html += f"""
        <div class="bg-white rounded-2xl shadow-md border border-slate-200 p-6 mb-8 hover:shadow-lg transition-shadow">
            <div class="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-slate-200 mb-5">
                <div class="flex items-center gap-3">
                    <div class="w-12 h-12 rounded-2xl bg-gradient-to-tr from-indigo-600 to-violet-500 text-white flex items-center justify-center font-bold text-lg shadow-sm">
                        #{idx}
                    </div>
                    <div>
                        <div class="flex items-center gap-2">
                            <h3 class="text-xl font-bold text-slate-900">Cliente VIP #{vip['customer_id']}</h3>
                            <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-slate-100 text-slate-700 border border-slate-200">
                                🌍 {vip['country']}
                            </span>
                        </div>
                        <p class="text-xs text-slate-500 mt-0.5">
                            Cliente desde {vip['first_order']} &bull; Última compra: <strong class="text-rose-600">{vip['last_order']}</strong>
                        </p>
                    </div>
                </div>
                <div class="flex flex-wrap items-center gap-3">
                    <div class="bg-rose-50 border border-rose-200 rounded-xl px-4 py-2 text-right">
                        <span class="text-xs text-rose-600 uppercase font-bold tracking-wider block">Inactividad</span>
                        <span class="text-lg font-black text-rose-700">{vip['days_inactive']} días</span>
                    </div>
                    <div class="bg-indigo-50 border border-indigo-200 rounded-xl px-4 py-2 text-right">
                        <span class="text-xs text-indigo-600 uppercase font-bold tracking-wider block">Gasto Total</span>
                        <span class="text-lg font-black text-indigo-900">£{vip['total_spent']:,.2f}</span>
                    </div>
                </div>
            </div>

            <!-- Métricas rápidas del cliente -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-5 text-center">
                <div class="bg-slate-50 p-2.5 rounded-xl border border-slate-200">
                    <span class="text-xs text-slate-500 block">Total Pedidos</span>
                    <span class="text-base font-bold text-slate-800">{vip['total_orders']}</span>
                </div>
                <div class="bg-slate-50 p-2.5 rounded-xl border border-slate-200">
                    <span class="text-xs text-slate-500 block">Unidades Compradas</span>
                    <span class="text-base font-bold text-slate-800">{vip['units_bought']:,}</span>
                </div>
                <div class="bg-slate-50 p-2.5 rounded-xl border border-slate-200">
                    <span class="text-xs text-slate-500 block">Ticket Promedio</span>
                    <span class="text-base font-bold text-slate-800">£{vip['avg_ticket']:,.2f}</span>
                </div>
                <div class="bg-slate-50 p-2.5 rounded-xl border border-slate-200">
                    <span class="text-xs text-slate-500 block">Estado del Cliente</span>
                    <span class="text-xs font-bold text-rose-700 bg-rose-100 px-2 py-0.5 rounded-full inline-block mt-0.5">Riesgo Alto Churn</span>
                </div>
            </div>

            <!-- Diagnóstico de pérdida de actividad -->
            <div class="bg-amber-50 border-l-4 border-amber-500 p-3.5 rounded-r-xl mb-5">
                <div class="flex items-start gap-2">
                    <span class="text-amber-600 font-bold text-base">⚠️</span>
                    <div>
                        <h4 class="text-xs font-bold text-amber-900 uppercase tracking-wider">Diagnóstico de Pérdida de Actividad</h4>
                        <p class="text-xs text-amber-800 mt-0.5 leading-relaxed">{vip['diagnostic']}</p>
                    </div>
                </div>
            </div>

            <!-- Productos preferidos -->
            <div class="mb-5 bg-slate-50/60 p-4 rounded-xl border border-slate-200">
                <h4 class="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                    <span>⭐</span> Artículos Clave con Mayor Aporte de Facturación
                </h4>
                <div class="space-y-1">
                    {products_html}
                </div>
            </div>

            <!-- 3 Acciones Tácticas -->
            <div>
                <h4 class="text-sm font-bold text-slate-800 uppercase tracking-wider mb-3 flex items-center gap-2">
                    <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block"></span>
                    Plan Estratégico Prescriptivo (3 Acciones de Ataque y Reactivación)
                </h4>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                    {actions_html}
                </div>
            </div>
        </div>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BI Retail Agent - Retención de Clientes VIP</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}
    </style>
</head>
<body class="bg-slate-100 text-slate-900 min-h-screen">

    <!-- Top Navigation Bar -->
    <header class="bg-slate-900 text-white border-b border-slate-800 sticky top-0 z-50 shadow-md">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex flex-wrap items-center justify-between gap-4">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-500 to-purple-500 flex items-center justify-center font-black text-xl shadow-inner">
                    🤖
                </div>
                <div>
                    <h1 class="text-lg font-bold tracking-tight">BI Retail Intelligence Agent</h1>
                    <p class="text-xs text-slate-400">Sistema de Detección de Fuga y Plan de Reactivación VIP</p>
                </div>
            </div>
            <div class="flex items-center gap-3 text-xs">
                <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-semibold">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    PostgreSQL Supabase Conectado
                </span>
                <span class="text-slate-400 hidden sm:inline">&bull;</span>
                <span class="text-slate-300 font-medium">Dataset: <strong>Online Retail II</strong></span>
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

        <!-- Header Hero & Context -->
        <div class="bg-white rounded-3xl p-6 md:p-8 shadow-sm border border-slate-200 mb-8">
            <div class="max-w-3xl">
                <span class="text-xs uppercase font-extrabold tracking-wider text-indigo-600 bg-indigo-50 px-3 py-1 rounded-full border border-indigo-100">
                    Skill Ejecutada: Análisis de Attrition y Reactivación Prescriptiva
                </span>
                <h2 class="text-2xl md:text-3xl font-extrabold text-slate-900 mt-3 leading-tight">
                    Detección de Pérdida de Actividad en los 5 Clientes Más Valiosos
                </h2>
                <p class="text-slate-600 text-sm md:text-base mt-2 leading-relaxed">
                    El agente analizó la totalidad de los <strong>{overview['total_rows']:,} registros</strong> en Supabase, calculó métricas de Recencia, Frecuencia y Valor Monetario (RFM) e identificó a los clientes líderes en facturación y pedidos que presentan una cesación prolongada de compras.
                </p>
            </div>

            <!-- KPIs Principales -->
            <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mt-8 pt-6 border-t border-slate-200">
                <div class="bg-gradient-to-br from-rose-50 to-rose-100/50 p-4 rounded-2xl border border-rose-200">
                    <span class="text-xs font-bold text-rose-600 uppercase tracking-wider block">Facturación VIP en Riesgo</span>
                    <span class="text-2xl lg:text-3xl font-black text-rose-700 mt-1 block">£{overview['vip_lost_revenue']:,.2f}</span>
                    <span class="text-xs text-rose-600/80 mt-1 block font-medium">Suma de los 5 VIPs inactivos</span>
                </div>
                <div class="bg-slate-50 p-4 rounded-2xl border border-slate-200">
                    <span class="text-xs font-bold text-slate-500 uppercase tracking-wider block">Clientes Totales Evaluados</span>
                    <span class="text-2xl lg:text-3xl font-black text-slate-800 mt-1 block">{overview['total_customers']:,}</span>
                    <span class="text-xs text-slate-500 mt-1 block font-medium">{overview['total_orders']:,} órdenes globales</span>
                </div>
                <div class="bg-slate-50 p-4 rounded-2xl border border-slate-200">
                    <span class="text-xs font-bold text-slate-500 uppercase tracking-wider block">Facturación Global</span>
                    <span class="text-2xl lg:text-3xl font-black text-slate-800 mt-1 block">£{overview['total_revenue']:,.2f}</span>
                    <span class="text-xs text-slate-500 mt-1 block font-medium">{overview['min_date']} a {overview['max_date']}</span>
                </div>
                <div class="bg-indigo-50 p-4 rounded-2xl border border-indigo-200">
                    <span class="text-xs font-bold text-indigo-600 uppercase tracking-wider block">Acciones Tácticas Generadas</span>
                    <span class="text-2xl lg:text-3xl font-black text-indigo-700 mt-1 block">15</span>
                    <span class="text-xs text-indigo-600/80 mt-1 block font-medium">3 por cada cliente VIP</span>
                </div>
            </div>
        </div>

        <!-- Charts Section -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <!-- Gráfico 1: Segmentación de Clientes -->
            <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                <div class="flex items-center justify-between mb-4">
                    <div>
                        <h3 class="text-base font-bold text-slate-800">Distribución de la Base de Clientes</h3>
                        <p class="text-xs text-slate-500">Segmentación por días de inactividad respecto al último corte</p>
                    </div>
                </div>
                <div class="relative h-64">
                    <canvas id="segmentChart"></canvas>
                </div>
            </div>

            <!-- Gráfico 2: Top 5 VIPs en Riesgo -->
            <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                <div class="flex items-center justify-between mb-4">
                    <div>
                        <h3 class="text-base font-bold text-slate-800">Top 5 VIPs: Gasto Acumulado vs Días Inactivos</h3>
                        <p class="text-xs text-slate-500">Magnitud del impacto financiero y tiempo transcurrido sin compras</p>
                    </div>
                </div>
                <div class="relative h-64">
                    <canvas id="vipChart"></canvas>
                </div>
            </div>
        </div>

        <!-- Deep Dive: Top 5 Clientes y sus 3 Acciones -->
        <div class="mb-8">
            <div class="flex items-center justify-between mb-5">
                <div>
                    <h3 class="text-xl font-black text-slate-900">Detalle de los 5 Clientes Más Valiosos con Pérdida de Actividad</h3>
                    <p class="text-xs text-slate-500 mt-0.5">Diagnóstico analítico particular y plan de acción de 3 pasos por cliente</p>
                </div>
                <span class="text-xs font-bold text-indigo-700 bg-indigo-50 border border-indigo-200 px-3 py-1.5 rounded-xl">
                    Umbral de Inactividad: &gt; {overview['inactivity_threshold']} días
                </span>
            </div>

            {vip_cards_html}
        </div>

        <!-- Tabla Resumen Comparativa -->
        <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
            <div class="flex flex-wrap items-center justify-between gap-4 mb-4">
                <div>
                    <h3 class="text-base font-bold text-slate-800">Matriz Ejecutiva de Priorización de Contacto</h3>
                    <p class="text-xs text-slate-500">Resumen ordenado por aportación financiera en riesgo</p>
                </div>
                <button onclick="window.print()" class="px-4 py-2 bg-slate-900 text-white text-xs font-bold rounded-xl hover:bg-slate-800 transition-colors flex items-center gap-2">
                    🖨️ Exportar / Imprimir Reporte
                </button>
            </div>
            <div class="overflow-x-auto">
                <table class="w-full text-left text-xs text-slate-700">
                    <thead class="bg-slate-50 text-slate-600 font-bold uppercase tracking-wider border-b border-slate-200">
                        <tr>
                            <th class="py-3 px-4">Prioridad</th>
                            <th class="py-3 px-4">ID Cliente</th>
                            <th class="py-3 px-4">País</th>
                            <th class="py-3 px-4 text-right">Gasto Total (£)</th>
                            <th class="py-3 px-4 text-center">Pedidos</th>
                            <th class="py-3 px-4 text-right">Ticket Promedio (£)</th>
                            <th class="py-3 px-4 text-center">Días Inactivo</th>
                            <th class="py-3 px-4">Acción Inmediata Clave</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100">
                        {"".join([f'''
                        <tr class="hover:bg-slate-50/80 transition-colors">
                            <td class="py-3.5 px-4 font-bold text-indigo-600">#{i}</td>
                            <td class="py-3.5 px-4 font-bold text-slate-900">Cliente {v["customer_id"]}</td>
                            <td class="py-3.5 px-4">{v["country"]}</td>
                            <td class="py-3.5 px-4 text-right font-black text-slate-900">£{v["total_spent"]:,.2f}</td>
                            <td class="py-3.5 px-4 text-center">{v["total_orders"]}</td>
                            <td class="py-3.5 px-4 text-right font-semibold">£{v["avg_ticket"]:,.2f}</td>
                            <td class="py-3.5 px-4 text-center">
                                <span class="px-2.5 py-1 rounded-full font-bold bg-rose-100 text-rose-800">{v["days_inactive"]} d</span>
                            </td>
                            <td class="py-3.5 px-4 font-medium text-slate-800">{v["actions"][0]["title"]}</td>
                        </tr>
                        ''' for i, v in enumerate(vips, 1)])}
                    </tbody>
                </table>
            </div>
        </div>

    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-slate-200 py-6 mt-12 text-center text-xs text-slate-500">
        <p>Generado automáticamente por el <strong>Agente de BI de Retail</strong> &bull; Basado en PostgreSQL (Supabase) & LLM Analytics</p>
    </footer>

    <!-- Chart.js Scripts -->
    <script>
        // Gráfico 1: Segmentos
        const ctxSegment = document.getElementById('segmentChart').getContext('2d');
        new Chart(ctxSegment, {{
            type: 'doughnut',
            data: {{
                labels: {json.dumps(segment_labels)},
                datasets: [{{
                    data: {json.dumps(segment_counts)},
                    backgroundColor: ['#10b981', '#f59e0b', '#f43f5e'],
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{ boxWidth: 12, font: {{ size: 11 }} }}
                    }}
                }}
            }}
        }});

        // Gráfico 2: Top 5 VIPs Gasto vs Inactividad
        const ctxVip = document.getElementById('vipChart').getContext('2d');
        new Chart(ctxVip, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(vip_labels)},
                datasets: [
                    {{
                        label: 'Gasto Total (£)',
                        data: {json.dumps(vip_spends)},
                        backgroundColor: '#6366f1',
                        borderRadius: 8,
                        yAxisID: 'y'
                    }},
                    {{
                        label: 'Días Inactivo',
                        data: {json.dumps(vip_inactivity)},
                        type: 'line',
                        borderColor: '#e11d48',
                        backgroundColor: '#e11d48',
                        borderWidth: 2,
                        pointRadius: 4,
                        yAxisID: 'y1'
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    y: {{
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {{ display: true, text: 'Gasto (£)', font: {{ size: 10 }} }}
                    }},
                    y1: {{
                        type: 'linear',
                        display: true,
                        position: 'right',
                        grid: {{ drawOnChartArea: false }},
                        title: {{ display: true, text: 'Días de Inactividad', font: {{ size: 10 }} }}
                    }}
                }},
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{ boxWidth: 12, font: {{ size: 11 }} }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"[DASHBOARD] HTML generado con éxito en: {output_file.resolve()}")
    return str(output_file.resolve())

