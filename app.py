import streamlit as st
import pandas as pd
import altair as alt
import json

st.set_page_config(
    page_title="Finanzas Tatis Pro",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        font-size: 13px;
        color: #3E2723;
    }
    
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 100% !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    .main {
        background: linear-gradient(135deg, #F3E5F5 0%, #E1BEE7 50%, #CE93D8 100%);
    }
    
    [data-testid="stSidebar"] {
        min-width: 330px;
        max-width: 360px;
        background: linear-gradient(180deg, #E1BEE7 0%, #CE93D8 100%);
        border-right: 2px solid #AB47BC;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0.8rem;
        padding-bottom: 1rem;
    }
    
    .header-container {
        text-align: center;
        background: linear-gradient(135deg, #7B1FA2 0%, #8E24AA 50%, #C2185B 100%);
        padding: 12px 15px;
        border-radius: 14px;
        border: 2px solid #F3E5F5;
        box-shadow: 0 4px 15px rgba(123, 31, 162, 0.3);
        margin-bottom: 10px;
    }
    
    .header-title {
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 1.6rem;
        color: #FFFFFF;
        margin: 0;
        letter-spacing: 0.5px;
    }

    .stButton>button {
        background: linear-gradient(135deg, #8E24AA 0%, #D81B60 100%);
        color: white;
        border-radius: 8px;
        padding: 0.2rem 0.5rem;
        font-weight: 700;
        font-size: 0.75rem;
        border: none;
        box-shadow: 0 2px 6px rgba(142, 36, 170, 0.3);
        width: 100%;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #6A1B9A 0%, #AD1457 100%);
        transform: translateY(-1px);
        color: white;
    }

    .metric-card-sidebar {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 8px 10px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(123, 31, 162, 0.15);
        border: 1.5px solid #BA68C8;
        text-align: center;
        margin-bottom: 6px;
    }
    .metric-value-gigante {
        color: #6A1B9A; 
        font-size: 1.2rem; 
        font-weight: 900; 
        margin: 1px 0;
    }

    .config-box-compact {
        background: rgba(255, 255, 255, 0.95);
        padding: 10px 12px;
        border-radius: 12px;
        border: 1.5px solid #BA68C8;
        box-shadow: 0 3px 10px rgba(123, 31, 162, 0.1);
        margin-bottom: 10px;
    }
    
    .kiut-card-grid {
        background-color: rgba(255, 255, 255, 0.96);
        padding: 12px 14px;
        border-radius: 10px;
        border: 1.5px solid #CE93D8;
        box-shadow: 0 2px 8px rgba(123, 31, 162, 0.12);
        margin-bottom: 12px;
    }

    .global-dark-box-sidebar {
        background: linear-gradient(135deg, #4A148C 0%, #7B1FA2 100%);
        padding: 8px;
        border-radius: 10px;
        color: white;
        text-align: center;
        border: 2px solid #E1BEE7;
        margin-top: 4px;
        margin-bottom: 4px;
        box-shadow: 0 3px 8px rgba(74, 20, 140, 0.3);
    }
    
    .liberado-box {
        background: linear-gradient(135deg, #F3E5F5 0%, #FCE4EC 100%);
        padding: 6px 10px;
        border-radius: 8px;
        border: 1.5px solid #BA68C8;
        text-align: center;
        margin-bottom: 6px;
    }
    </style>
""", unsafe_allow_html=True)

def formato_COP(valor):
    return f"$ {valor:,.0f}".replace(",", ".")

if 'obligaciones_base' not in st.session_state:
    st.session_state.obligaciones_base = [
        {"id": "camilo_m", "nombre": "Deuda Camilo", "valor": 373500.0, "tipo": "Crédito", "total": 6, "pagadas": 2, "periodo": "Mitad de Mes", "fecha_pago": "Día 15"},
        {"id": "gas_m", "nombre": "Gas", "valor": 390000.0, "tipo": "Servicio Cuotas", "total": 12, "pagadas": 7, "periodo": "Mitad de Mes", "fecha_pago": "Día 15"},
        {"id": "tc_m", "nombre": "Tarjeta de Crédito (TC)", "valor": 160000.0, "tipo": "Crédito TC", "total": 8, "pagadas": 0, "periodo": "Mitad de Mes", "fecha_pago": "Día 15"},
        
        # Sistecredito
        {"id": "sist_vest", "nombre": "Sistecredito Vestido", "valor": 39413.0, "tipo": "Crédito", "total": 4, "pagadas": 3, "periodo": "Mitad de Mes", "fecha_pago": "Día 15"},
        {"id": "sist_sud", "nombre": "Sistecredito Sudadera", "valor": 59599.0, "tipo": "Crédito", "total": 4, "pagadas": 3, "periodo": "Mitad de Mes", "fecha_pago": "Día 15"},
        {"id": "sist_mal", "nombre": "Sistecredito Maleta (Totto)", "valor": 66051.0, "tipo": "Crédito", "total": 4, "pagadas": 3, "periodo": "Mitad de Mes", "fecha_pago": "Día 15"},
        
        # Préstamo Nicolás septiembre
        {"id": "nicolas_q1", "nombre": "Préstamo Nicolás (Cuota 1)", "valor": 216000.0, "tipo": "Préstamo 20%", "total": 5, "pagadas": 0, "periodo": "Mitad de Mes", "fecha_pago": "22 de Sept"},

        # Deuda pendiente Nicolás en Octubre
        {"id": "nicolas_oct_m", "nombre": "Deuda Nicolás Octubre (Q1)", "valor": 180000.0, "tipo": "Deuda Única", "total": 1, "pagadas": 0, "periodo": "Mitad de Mes", "fecha_pago": "Octubre Q1"},

        {"id": "internet_m", "nombre": "Internet Q1", "valor": 55000.0, "tipo": "Fijo", "periodo": "Mitad de Mes", "fecha_pago": "Día 15"},
        {"id": "parq_m", "nombre": "Parqueadero Q1", "valor": 25000.0, "tipo": "Fijo", "periodo": "Mitad de Mes", "fecha_pago": "Día 15"},
        {"id": "libres_m", "nombre": "Gastos Libres Q1", "valor": 100000.0, "tipo": "Libre", "periodo": "Mitad de Mes", "fecha_pago": "Día 15"},

        {"id": "camilo_f", "nombre": "Deuda Camilo (Fin)", "valor": 373500.0, "tipo": "Crédito", "total": 6, "pagadas": 2, "periodo": "Fin de Mes", "fecha_pago": "Día 20"},
        {"id": "tecno_moto", "nombre": "Tecnomecánica Moto", "valor": 223700.0, "tipo": "Crédito Moto", "total": 6, "pagadas": 0, "periodo": "Fin de Mes", "fecha_pago": "28 de Sept"},
        {"id": "gas_f", "nombre": "Gas (Fin)", "valor": 390000.0, "tipo": "Servicio Cuotas", "total": 12, "pagadas": 7, "periodo": "Fin de Mes", "fecha_pago": "Día 20"},
        {"id": "tc_f", "nombre": "Tarjeta de Crédito (Fin)", "valor": 160000.0, "tipo": "Crédito TC", "total": 8, "pagadas": 0, "periodo": "Fin de Mes", "fecha_pago": "Día 20"},
        
        {"id": "nicolas_oct_f", "nombre": "Deuda Nicolás Octubre (Q2)", "valor": 180000.0, "tipo": "Deuda Única", "total": 1, "pagadas": 0, "periodo": "Fin de Mes", "fecha_pago": "Octubre Q2"},

        {"id": "internet_f", "nombre": "Internet Q2", "valor": 77000.0, "tipo": "Fijo", "periodo": "Fin de Mes", "fecha_pago": "Día 20"},
        {"id": "parq_f", "nombre": "Parqueadero Q2", "valor": 60000.0, "tipo": "Fijo", "periodo": "Fin de Mes", "fecha_pago": "Día 20"},
        {"id": "libres_f", "nombre": "Gastos Libres Q2", "valor": 100000.0, "tipo": "Libre", "periodo": "Fin de Mes", "fecha_pago": "Día 20"},
        {"id": "addi_m", "nombre": "Cuota Addi (Mamá)", "valor": 110000.0, "tipo": "Crédito Addi", "total": 3, "pagadas": 1, "periodo": "Fin de Mes", "fecha_pago": "Día 20"},
    ]

if 'pagos_por_periodo' not in st.session_state:
    st.session_state.pagos_por_periodo = {}
if 'imprevistos_por_periodo' not in st.session_state:
    st.session_state.imprevistos_por_periodo = {}
if 'prestamos_por_cobrar' not in st.session_state:
    st.session_state.prestamos_por_cobrar = [
        {"deudor": "Tania", "valor": 20000.0, "fecha_pago": "Pendiente"}
    ]

# TÍTULO PRINCIPAL
st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🌸 Finanzas Tatis Pro 🌸</h1>
    </div>
""", unsafe_allow_html=True)

# CONFIGURACIÓN SUPERIOR COMPACTA
st.markdown('<div class="config-box-compact">', unsafe_allow_html=True)
col_cfg1, col_cfg2, col_cfg3, col_cfg4 = st.columns(4)
with col_cfg1:
    saldo_actual_banco = st.number_input("Banco + Nequi (COP)", value=540427.0, step=10000.0)
with col_cfg2:
    nomina_quincenal_neta = st.number_input("Nómina Neta", value=1294007.0, step=10000.0)
with col_cfg3:
    mes_seleccionado = st.selectbox("Mes", ["Marzo 2026", "Abril 2026", "Mayo 2026", "Junio 2026", "Julio 2026", "Agosto 2026", "Septiembre 2026", "Octubre 2026", "Noviembre 2026", "Diciembre 2026"], key="select_mes_main")
with col_cfg4:
    quincena_tipo = st.selectbox("Quincena", ["Mitad de Mes (Día 15)", "Fin de Mes (Día 20)"], key="select_quincena_main")
st.markdown('</div>', unsafe_allow_html=True)

periodo_filtro = "Mitad de Mes" if "Mitad" in quincena_tipo else "Fin de Mes"
clave_periodo_actual = f"{mes_seleccionado} - {periodo_filtro}"

# Marcamos por defecto como pagados lo que ya pagaste (Camilo, Tarjeta, Sistecredito)
if clave_periodo_actual not in st.session_state.pagos_por_periodo:
    st.session_state.pagos_por_periodo[clave_periodo_actual] = {
        "camilo_m": True,
        "tc_m": True,
        "sist_vest": True,
        "sist_sud": True,
        "sist_mal": True
    }
if clave_periodo_actual not in st.session_state.imprevistos_por_periodo:
    st.session_state.imprevistos_por_periodo[clave_periodo_actual] = [
        {"nombre": "Tanqueo Moto Semanal", "valor": 40000.0}
    ]

obligaciones_activas = []
dinero_liberado_total = 0.0

for item in st.session_state.obligaciones_base:
    if "total" in item and item["total"] > 0:
        if item["pagadas"] >= item["total"]:
            dinero_liberado_total += item["valor"]
    obligaciones_activas.append(item)

presupuesto_quincena_inicial = nomina_quincenal_neta
pagos_actuales = st.session_state.pagos_por_periodo[clave_periodo_actual]
total_pagado_obligaciones_actual = sum(item["valor"] for item in obligaciones_activas if item["periodo"] == periodo_filtro and pagos_actuales.get(item["id"], False))
total_imprevistos = sum(imp["valor"] for imp in st.session_state.imprevistos_por_periodo[clave_periodo_actual])
quincena_que_queda = presupuesto_quincena_inicial - total_pagado_obligaciones_actual - total_imprevistos

# -------------------------------------------------------------
# BARRA LATERAL UNIFORME
# -------------------------------------------------------------
st.sidebar.markdown(f"### 💜 {clave_periodo_actual}")

st.sidebar.markdown(f'''
    <div class="liberado-box">
        <span style="font-size:0.7rem; font-weight:800; color:#6A1B9A;">✨ Dinero Liberado ✨</span><br>
        <span style="font-size:1.05rem; font-weight:900; color:#8E24AA;">{formato_COP(dinero_liberado_total)}</span>
    </div>
''', unsafe_allow_html=True)

st.sidebar.markdown(f'''
    <div class="metric-card-sidebar">
        <h6 style="color:#6A1B9A; margin:0; font-weight:700;">📥 Nómina Neta</h6>
        <div class="metric-value-gigante">{formato_COP(presupuesto_quincena_inicial)}</div>
    </div>
''', unsafe_allow_html=True)

st.sidebar.markdown(f'''
    <div class="metric-card-sidebar">
        <h6 style="color:#7B1FA2; margin:0; font-weight:700;">📤 Pagado Periodo</h6>
        <div class="metric-value-gigante">{formato_COP(total_pagado_obligaciones_actual)}</div>
    </div>
''', unsafe_allow_html=True)

st.sidebar.markdown(f'''
    <div class="metric-card-sidebar">
        <h6 style="color:#AD1457; margin:0; font-weight:700;">🚨 Imprevistos / Gas / Moto</h6>
        <div class="metric-value-gigante">{formato_COP(total_imprevistos)}</div>
    </div>
''', unsafe_allow_html=True)

color_queda = "#7B1FA2" if quincena_que_queda >= 0 else "#C2185B"
st.sidebar.markdown(f'''
    <div class="metric-card-sidebar" style="border: 2px solid {color_queda}; background: #FCE4EC;">
        <h6 style="color:{color_queda}; margin:0; font-weight:800;">✨ LO QUE QUEDA ✨</h6>
        <div class="metric-value-gigante" style="color:{color_queda}; font-size:1.3rem;">{formato_COP(quincena_que_queda)}</div>
    </div>
''', unsafe_allow_html=True)

total_deuda_global = sum(item["valor"] * max(0, (item["total"] - item["pagadas"])) if "total" in item else item["valor"] for item in obligaciones_activas)

st.sidebar.markdown(f"""
<div class="global-dark-box-sidebar">
    <div style="font-size: 0.75rem; font-weight: 800; text-transform: uppercase;">👑 Deuda Global Pendiente</div>
    <div style="font-size: 1.05rem; font-weight: 900; color: #FFFFFF; margin-top:2px;">{formato_COP(total_deuda_global)}</div>
</div>
""", unsafe_allow_html=True)

# GESTIÓN DE RESPALDO (EXPORTAR / IMPORTAR) EN SIDEBAR
with st.sidebar.expander("💾 Guardar / Cargar Respaldo"):
    data_backup = {
        "obligaciones_base": st.session_state.obligaciones_base,
        "pagos_por_periodo": st.session_state.pagos_por_periodo,
        "imprevistos_por_periodo": st.session_state.imprevistos_por_periodo,
        "prestamos_por_cobrar": st.session_state.prestamos_por_cobrar
    }
    json_str = json.dumps(data_backup, ensure_ascii=False, indent=4)
    st.download_button("📥 Descargar Archivo Respaldo", data=json_str, file_name="respaldo_finanzas_tatis.json", mime="application/json")
    
    uploaded_file = st.file_uploader("📤 Cargar Archivo Respaldo", type=["json"])
    if uploaded_file is not None:
        try:
            loaded_data = json.load(uploaded_file)
            st.session_state.obligaciones_base = loaded_data.get("obligaciones_base", st.session_state.obligaciones_base)
            st.session_state.pagos_por_periodo = loaded_data.get("pagos_por_periodo", {})
            st.session_state.imprevistos_por_periodo = loaded_data.get("imprevistos_por_periodo", {})
            st.session_state.prestamos_por_cobrar = loaded_data.get("prestamos_por_cobrar", [])
            st.success("¡Respaldo cargado con éxito!")
            st.rerun()
        except Exception as e:
            st.error("Error al cargar el archivo.")

# GRÁFICO DE BARRAS PORCENTUALES
st.sidebar.markdown("<hr style='border: 1px solid #BA68C8; margin: 10px 0;'>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='color: #4A148C; font-weight: 800; text-align: center; margin-bottom: 2px;'>💖 Distribución de Fondos</h4>", unsafe_allow_html=True)

val_pagado = float(total_pagado_obligaciones_actual)
val_pendiente = float(sum(item["valor"] for item in obligaciones_activas if item["periodo"] == periodo_filtro and not pagos_actuales.get(item["id"], False)))
val_imprevistos = float(total_imprevistos)
val_disponible = float(max(0.0, quincena_que_queda))

total_base_calc = val_pagado + val_pendiente + val_imprevistos + val_disponible
if total_base_calc <= 0:
    total_base_calc = 1.0

df_grafico = pd.DataFrame({
    'Categoría': ['Pagado', 'Pendiente', 'Imprevistos', 'Disponible'],
    'Monto': [val_pagado, val_pendiente, val_imprevistos, val_disponible],
    'Porcentaje': [
        (val_pagado / total_base_calc) * 100,
        (val_pendiente / total_base_calc) * 100,
        (val_imprevistos / total_base_calc) * 100,
        (val_disponible / total_base_calc) * 100
    ]
})

orden_categorias = ['Disponible', 'Imprevistos', 'Pendiente', 'Pagado']
df_grafico['Categoría'] = pd.Categorical(df_grafico['Categoría'], categories=orden_categorias, ordered=True)

bar_chart = alt.Chart(df_grafico).mark_bar(cornerRadius=6).encode(
    x=alt.X('Porcentaje:Q', title=None, axis=None, scale=alt.Scale(domain=[0, 100])),
    y=alt.Y('Categoría:N', title=None, axis=alt.Axis(labelFontSize=11, labelColor="#3E2723")),
    color=alt.Color(
        'Categoría:N',
        scale=alt.Scale(
            domain=['Pagado', 'Pendiente', 'Imprevistos', 'Disponible'],
            range=['#6A1B9A', '#D81B60', '#BA68C8', '#F48FB1']
        ),
        legend=None
    ),
    tooltip=[
        alt.Tooltip('Categoría', title="Concepto"),
        alt.Tooltip('Monto', title="Monto Real (COP)", format="$,.0f"),
        alt.Tooltip('Porcentaje', title="Porcentaje", format=".1f")
    ]
).properties(
    width=260,
    height=150
)

st.sidebar.altair_chart(bar_chart, use_container_width=True)


# -------------------------------------------------------------
# PANEL CENTRAL: CONTROL DE PAGOS EN MULTICOLUMNA
# -------------------------------------------------------------
st.markdown("<h4 style='color: #4A148C; font-weight: 800; margin-top: 5px;'>⚡ Control de Pagos de la Quincena</h4>", unsafe_allow_html=True)

items_filtrados = [item for item in obligaciones_activas if item["periodo"] == periodo_filtro]

cols_por_fila = 3
for i in range(0, len(items_filtrados), cols_por_fila):
    cols = st.columns(cols_por_fila)
    for j in range(cols_por_fila):
        if i + j < len(items_filtrados):
            item = items_filtrados[i + j]
            item_id = item["id"]
            esta_pagado = pagos_actuales.get(item_id, False)
            
            if "total" in item and item["total"] > 0:
                porcentaje = int(round((item["pagadas"] / item["total"]) * 100))
            else:
                porcentaje = 100 if esta_pagado else 0
            
            with cols[j]:
                st.markdown('<div class="kiut-card-grid">', unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div style="background-color: #E1BEE7; border-radius: 8px; height: 22px; width: 100%; position: relative; margin-bottom: 8px; overflow: hidden; border: 1.5px solid #BA68C8;">
                        <div style="background: linear-gradient(135deg, #7B1FA2 0%, #8E24AA 100%); width: {porcentaje}%; height: 100%; border-radius: 6px 0 0 6px; transition: width 0.4s ease;"></div>
                        <div style="position: absolute; width: 100%; top: 0; left: 0; text-align: center; font-size: 11px; font-weight: 800; color: #FFFFFF; line-height: 20px; text-shadow: 0px 1px 2px rgba(0,0,0,0.4);">
                            {porcentaje}% Avance
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                info_sec = f"Q {item['pagadas']}/{item['total']}" if "total" in item else f"{item.get('fecha_pago', '-')}"
                estado_txt = "✅ Pagado" if esta_pagado else "⏳ Pendiente"
                color_est = "#6A1B9A" if esta_pagado else "#C2185B"
                
                st.markdown(f"""
                    <div style='font-weight:800; font-size:13.5px; color:#3E2723; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>{item['nombre']}</div>
                    <div style='font-size:0.7rem; color:#8E24AA; font-weight:700;'>{item['tipo']} • {info_sec}</div>
                    <div style='font-weight:900; font-size:13px; color:#6A1B9A; margin-top:2px; margin-bottom: 8px;'>{formato_COP(item['valor'])} <span style='font-weight:700; color:{color_est}; font-size:11px; float:right;'>{estado_txt}</span></div>
                """, unsafe_allow_html=True)
                
                if not esta_pagado:
                    if st.button("Pagar ✅", key=f"pagar_{clave_periodo_actual}_{item_id}"):
                        st.session_state.pagos_por_periodo[clave_periodo_actual][item_id] = True
                        if "total" in item and item["pagadas"] < item["total"]:
                            item["pagadas"] += 1
                        st.rerun()
                else:
                    if st.button("Deshacer 🔄", key=f"deshacer_{clave_periodo_actual}_{item_id}"):
                        st.session_state.pagos_por_periodo[clave_periodo_actual][item_id] = False
                        if "total" in item and item["pagadas"] > 0:
                            item["pagadas"] -= 1
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid #CE93D8; margin: 15px 0;'>", unsafe_allow_html=True)

# PESTAÑAS INFERIORES PRO (CON RESUMEN POR QUINCENA Y MES)
tab_deudas, tab_resumen, tab_editar, tab_prestamos, tab_extras = st.tabs(["➕ Nueva Deuda", "📊 Resumen Quincena & Mes", "✏️ Modificar Cuotas", "🤝 Cuentas por Cobrar", "🚨 Imprevistos & Exportar"])

with tab_deudas:
    with st.form(key="form_nueva_deuda_main"):
        c_nd1, c_nd2, c_nd3 = st.columns(3)
        with c_nd1:
            n_nombre = st.text_input("Nombre de la obligación")
            n_valor_cuota = st.number_input("Valor Cuota / Deuda Total", min_value=0.0, step=10000.0)
        with c_nd2:
            n_total_cuotas = st.number_input("Total Cuotas (1 si es pago único)", min_value=1, value=1, step=1)
            n_periodo = st.selectbox("Asignar a Quincena / Tipo", ["Mitad de Mes", "Fin de Mes", "Deuda Libre / Sin Quincena Fija"])
        with c_nd3:
            n_fecha_pago = st.text_input("Fecha / Frecuencia (Ej. Libre, Día 15)")
            st.markdown("<br>", unsafe_allow_html=True)
            submit_deuda = st.form_submit_button("Guardar Nueva Deuda 💜")
        
        if submit_deuda and n_nombre and n_valor_cuota > 0:
            nuevo_id = f"deuda_nueva_{len(st.session_state.obligaciones_base)}"
            st.session_state.obligaciones_base.append({
                "id": nuevo_id, "nombre": n_nombre, "valor": n_valor_cuota,
                "tipo": "Crédito Nuevo" if n_total_cuotas > 1 else "Deuda Única", 
                "total": int(n_total_cuotas), "pagadas": 0,
                "periodo": n_periodo, "fecha_pago": n_fecha_pago if n_fecha_pago else "Por definir"
            })
            st.success("¡Deuda guardada correctamente y sumada a la deuda global!")
            st.rerun()

with tab_resumen:
    st.markdown("<h4 style='color: #4A148C; font-weight: 800;'>📊 Resumen General por Periodos y Meses</h4>", unsafe_allow_html=True)
    st.markdown(f"**Mes consultado:** {mes_seleccionado}")
    
    # Resumen Mitad de Mes
    tot_mitad = sum(item["valor"] for item in st.session_state.obligaciones_base if item["periodo"] == "Mitad de Mes")
    pagado_mitad = sum(item["valor"] for item in st.session_state.obligaciones_base if item["periodo"] == "Mitad de Mes" and st.session_state.pagos_por_periodo.get(f"{mes_seleccionado} - Mitad de Mes", {}).get(item["id"], False))
    
    # Resumen Fin de Mes
    tot_fin = sum(item["valor"] for item in st.session_state.obligaciones_base if item["periodo"] == "Fin de Mes")
    pagado_fin = sum(item["valor"] for item in st.session_state.obligaciones_base if item["periodo"] == "Fin de Mes" and st.session_state.pagos_por_periodo.get(f"{mes_seleccionado} - Fin de Mes", {}).get(item["id"], False))

    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.markdown(f"""
            <div class="kiut-card-grid">
                <h5 style="color:#6A1B9A; margin-top:0;">🌸 Mitad de Mes (Día 15)</h5>
                <p><b>Total Obligaciones:</b> {formato_COP(tot_mitad)}</p>
                <p><b>Pagado:</b> {formato_COP(pagado_mitad)}</p>
                <p><b>Pendiente:</b> {formato_COP(tot_mitad - pagado_mitad)}</p>
            </div>
        """, unsafe_allow_html=True)
    with col_res2:
        st.markdown(f"""
            <div class="kiut-card-grid">
                <h5 style="color:#7B1FA2; margin-top:0;">🌸 Fin de Mes (Día 20)</h5>
                <p><b>Total Obligaciones:</b> {formato_COP(tot_fin)}</p>
                <p><b>Pagado:</b> {formato_COP(pagado_fin)}</p>
                <p><b>Pendiente:</b> {formato_COP(tot_fin - pagado_fin)}</p>
            </div>
        """, unsafe_allow_html=True)

with tab_editar:
    st.markdown("<p style='font-weight: 700; color: #4A148C;'>Si alguna cuota subió o bajó de precio este mes, selecciónala aquí y actualiza su valor:</p>", unsafe_allow_html=True)
    with st.form(key="form_editar_cuota_val"):
        nombres_obligaciones = {item["nombre"] + f" ({item['periodo']})": item for item in st.session_state.obligaciones_base}
        sel_nombre_edit = st.selectbox("Selecciona la obligación a modificar", list(nombres_obligaciones.keys()))
        item_a_editar = nombres_obligaciones[sel_nombre_edit]
        
        nuevo_valor_edit = st.number_input("Nuevo Valor (COP)", value=float(item_a_editar["valor"]), step=1000.0)
        
        if st.form_submit_button("Actualizar Valor de Cuota 💜"):
            item_a_editar["valor"] = nuevo_valor_edit
            st.success(f"¡Se actualizó el valor de {item_a_editar['nombre']} a {formato_COP(nuevo_valor_edit)}!")
            st.rerun()

with tab_prestamos:
    with st.form(key="form_prestamo_main"):
        cp1, cp2, cp3 = st.columns(3)
        with cp1:
            p_deudor = st.text_input("Deudor")
        with cp2:
            p_valor = st.number_input("Monto (COP)", min_value=0.0, step=10000.0)
        with cp3:
            p_fecha = st.text_input("Fecha estimada de pago")
            
        if st.form_submit_button("Registrar Préstamo 🤝") and p_deudor and p_valor > 0:
            st.session_state.prestamos_por_cobrar.append({"deudor": p_deudor, "valor": p_valor, "fecha_pago": p_fecha or "Por definir"})
            st.success("¡Préstamo registrado!")
            st.rerun()

    if st.session_state.prestamos_por_cobrar:
        st.markdown("<br>", unsafe_allow_html=True)
        for idx_p, prestamo in enumerate(st.session_state.prestamos_por_cobrar):
            st.markdown('<div class="kiut-card-grid">', unsafe_allow_html=True)
            st.markdown(f"**{prestamo['deudor']}** - {formato_COP(prestamo['valor'])} (Paga: {prestamo['fecha_pago']})")
            if st.button("Cobrado ✅", key=f"cobrado_{idx_p}"):
                st.session_state.prestamos_por_cobrar.pop(idx_p)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

with tab_extras:
    col_ex1, col_ex2 = st.columns(2)
    with col_ex1:
        with st.form(key="form_imprevisto_main_central"):
            nombre_imp_m = st.text_input("Concepto Gasto Hormiga / Imprevisto")
            valor_imp_m = st.number_input("Valor (COP)", min_value=0.0, step=10000.0)
            if st.form_submit_button("Registrar Imprevisto") and nombre_imp_m and valor_imp_m > 0:
                st.session_state.imprevistos_por_periodo[clave_periodo_actual].append({"nombre": nombre_imp_m, "valor": valor_imp_m})
                st.success("¡Registrado!")
                st.rerun()
    with col_ex2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📥 Descargar Base Completa en Excel (CSV)"):
            df_export = pd.DataFrame(st.session_state.obligaciones_base)
            csv_data = df_export.to_csv(index=False).encode('utf-8')
            st.download_button("Confirmar Descarga", data=csv_data, file_name="Finanzas_Tatis_Pro.csv", mime="text/csv")
