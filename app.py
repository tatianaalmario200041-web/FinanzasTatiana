import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Finanzas Tatis",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        font-size: 13.5px;
        color: #4A3B5C;
    }
    
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    
    .main {
        background: linear-gradient(135deg, #FBF8FD 0%, #F5EEF8 50%, #FAF0F5 100%);
    }
    
    [data-testid="stSidebar"] {
        min-width: 360px;
        max-width: 390px;
        background: linear-gradient(180deg, #F3E5F5 0%, #E1BEE7 100%);
        border-right: 2px solid #D1C4E9;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        position: sticky;
        top: 0px;
        height: 100vh;
        overflow-y: auto;
        padding-bottom: 1rem;
        padding-top: 1rem;
    }
    
    .header-title {
        font-family: 'Montserrat', sans-serif;
        font-weight: 800;
        font-size: 1.8rem;
        background: linear-gradient(135deg, #7B1FA2 0%, #9C27B0 50%, #E91E63 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: -10px;
        margin-bottom: 8px;
    }

    .stButton>button {
        background: linear-gradient(135deg, #AB47BC 0%, #EC407A 100%);
        color: white;
        border-radius: 8px;
        padding: 0.25rem 0.6rem;
        font-weight: 700;
        font-size: 0.8rem;
        border: none;
        box-shadow: 0 2px 6px rgba(171, 71, 188, 0.2);
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #8E24AA 0%, #D81B60 100%);
        color: white;
    }

    .metric-card-sidebar {
        background-color: #FFFFFF;
        padding: 8px 10px;
        border-radius: 10px;
        box-shadow: 0 3px 10px rgba(156, 39, 176, 0.08);
        border: 2px solid #CE93D8;
        text-align: center;
        margin-bottom: 6px;
    }
    .metric-value-gigante {
        color: #7B1FA2; 
        font-size: 1.3rem; 
        font-weight: 900; 
        margin: 1px 0;
    }

    .config-box-compact {
        background: rgba(255, 255, 255, 0.9);
        padding: 8px 12px;
        border-radius: 10px;
        border: 1px solid #E1BEE7;
        box-shadow: 0 3px 10px rgba(186, 104, 200, 0.06);
        margin-bottom: 10px;
    }
    
    .kiut-card {
        background-color: #FFFFFF;
        padding: 8px 12px;
        border-radius: 10px;
        border: 1px solid #E1BEE7;
        box-shadow: 0 2px 8px rgba(156, 39, 176, 0.04);
        margin-bottom: 6px;
    }

    .global-dark-box-sidebar {
        background: linear-gradient(135deg, #6A1B9A 0%, #8E24AA 100%);
        padding: 8px;
        border-radius: 10px;
        color: white;
        text-align: center;
        border: 2px solid #CE93D8;
        margin-top: 4px;
        margin-bottom: 4px;
    }

    .progress-container {
        width: 100%;
        background-color: #F3E5F5;
        border-radius: 6px;
        height: 8px;
        margin: 3px 0;
        overflow: hidden;
    }
    .progress-bar-kiut {
        height: 100%;
        background: linear-gradient(135deg, #AB47BC 0%, #EC407A 100%);
        border-radius: 6px;
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
        {"id": "sist_vest", "nombre": "Sistecredito Vestido", "valor": 39000.0, "tipo": "Crédito", "total": 4, "pagadas": 2, "periodo": "Mitad de Mes", "fecha_pago": "Día 15"},
        {"id": "sist_sud", "nombre": "Sistecredito Sudadera", "valor": 59000.0, "tipo": "Crédito", "total": 4, "pagadas": 2, "periodo": "Mitad de Mes", "fecha_pago": "Día 15"},
        {"id": "sist_mal", "nombre": "Sistecredito Maleta", "valor": 66000.0, "tipo": "Crédito", "total": 4, "pagadas": 2, "periodo": "Mitad de Mes", "fecha_pago": "Día 15"},
        {"id": "internet_m", "nombre": "Internet Q1", "valor": 55000.0, "tipo": "Fijo", "periodo": "Mitad de Mes", "fecha_pago": "Día 15"},
        {"id": "parq_m", "nombre": "Parqueadero Q1", "valor": 25000.0, "tipo": "Fijo", "periodo": "Mitad de Mes", "fecha_pago": "Día 15"},
        {"id": "libres_m", "nombre": "Gastos Libres Q1", "valor": 100000.0, "tipo": "Libre", "periodo": "Mitad de Mes", "fecha_pago": "Día 15"},

        {"id": "camilo_f", "nombre": "Deuda Camilo (Fin)", "valor": 373500.0, "tipo": "Crédito", "total": 6, "pagadas": 2, "periodo": "Fin de Mes", "fecha_pago": "Día 20"},
        {"id": "tecno_moto", "nombre": "Tecnomecánica Moto", "valor": 223700.0, "tipo": "Crédito Moto", "total": 6, "pagadas": 0, "periodo": "Fin de Mes", "fecha_pago": "28 de Marzo"},
        {"id": "gas_f", "nombre": "Gas (Fin)", "valor": 390000.0, "tipo": "Servicio Cuotas", "total": 12, "pagadas": 7, "periodo": "Fin de Mes", "fecha_pago": "Día 20"},
        {"id": "tc_f", "nombre": "Tarjeta de Crédito (Fin)", "valor": 160000.0, "tipo": "Crédito TC", "total": 8, "pagadas": 0, "periodo": "Fin de Mes", "fecha_pago": "Día 20"},
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
    st.session_state.prestamos_por_cobrar = []

# Título limpio arriba sin subtítulos de relleno
st.markdown('<div class="header-title">Finanzas Tatis</div>', unsafe_allow_html=True)

# Configuración compacta superior
st.markdown('<div class="config-box-compact">', unsafe_allow_html=True)
col_cfg1, col_cfg2, col_cfg3, col_cfg4, col_cfg5 = st.columns([2, 2, 2, 2.2, 2.2])
with col_cfg1:
    saldo_actual_banco = st.number_input("Banco (COP)", value=2800000.0, step=100000.0, label_visibility="collapsed")
with col_cfg2:
    nomina_quincenal_neta = st.number_input("Nómina Base", value=2200000.0, step=10000.0, label_visibility="collapsed")
with col_cfg3:
    ingresos_extra = st.number_input("Extras (COP)", value=0.0, step=10000.0, label_visibility="collapsed")
with col_cfg4:
    mes_seleccionado = st.selectbox("Mes", ["Marzo 2026", "Abril 2026", "Mayo 2026", "Junio 2026", "Julio 2026", "Agosto 2026", "Septiembre 2026"], key="select_mes_main", label_visibility="collapsed")
with col_cfg5:
    quincena_tipo = st.selectbox("Quincena", ["Mitad de Mes (Día 15)", "Fin de Mes (Día 20)"], key="select_quincena_main", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

periodo_filtro = "Mitad de Mes" if "Mitad" in quincena_tipo else "Fin de Mes"
clave_periodo_actual = f"{mes_seleccionado} - {periodo_filtro}"

if clave_periodo_actual not in st.session_state.pagos_por_periodo:
    st.session_state.pagos_por_periodo[clave_periodo_actual] = {}
if clave_periodo_actual not in st.session_state.imprevistos_por_periodo:
    st.session_state.imprevistos_por_periodo[clave_periodo_actual] = []

# BARRA LATERAL
st.sidebar.markdown(f"### 💜 {clave_periodo_actual}")
presupuesto_quincena_inicial = nomina_quincenal_neta
pagos_actuales = st.session_state.pagos_por_periodo[clave_periodo_actual]
total_pagado_obligaciones_actual = sum(item["valor"] for item in st.session_state.obligaciones_base if item["periodo"] == periodo_filtro and pagos_actuales.get(item["id"], False))
total_imprevistos = sum(imp["valor"] for imp in st.session_state.imprevistos_por_periodo[clave_periodo_actual])
quincena_que_queda = (presupuesto_quincena_inicial + ingresos_extra) - total_pagado_obligaciones_actual - total_imprevistos

st.sidebar.markdown(f'''
    <div class="metric-card-sidebar">
        <h6 style="color:#6A1B9A; margin:0;">📥 Ingresos Totales</h6>
        <div class="metric-value-gigante">{formato_COP(presupuesto_quincena_inicial + ingresos_extra)}</div>
    </div>
''', unsafe_allow_html=True)

st.sidebar.markdown(f'''
    <div class="metric-card-sidebar">
        <h6 style="color:#7B1FA2; margin:0;">📤 Pagado Periodo</h6>
        <div class="metric-value-gigante">{formato_COP(total_pagado_obligaciones_actual)}</div>
    </div>
''', unsafe_allow_html=True)

st.sidebar.markdown(f'''
    <div class="metric-card-sidebar">
        <h6 style="color:#AD1457; margin:0;">🚨 Imprevistos</h6>
        <div class="metric-value-gigante">{formato_COP(total_imprevistos)}</div>
    </div>
''', unsafe_allow_html=True)

color_queda = "#00897B" if quincena_que_queda >= 0 else "#E53935"
st.sidebar.markdown(f'''
    <div class="metric-card-sidebar" style="border: 2px solid {color_queda};">
        <h6 style="color:{color_queda}; margin:0;">✨ QUEDA ✨</h6>
        <div class="metric-value-gigante" style="color:{color_queda}; font-size:1.4rem;">{formato_COP(quincena_que_queda)}</div>
    </div>
''', unsafe_allow_html=True)

total_deuda_periodo = sum(item["valor"] for item in st.session_state.obligaciones_base if item["periodo"] == periodo_filtro)
porcentaje_periodo = int((total_pagado_obligaciones_actual / total_deuda_periodo) * 100) if total_deuda_periodo > 0 else 0

st.sidebar.markdown(f"**Progreso Periodo: {porcentaje_periodo}%**")
st.sidebar.markdown(f'''
    <div class="progress-container">
        <div class="progress-bar-kiut" style="width: {porcentaje_periodo}%;"></div>
    </div>
''', unsafe_allow_html=True)

total_deuda_global = sum(item["valor"] * item["total"] if "total" in item else item["valor"] for item in st.session_state.obligaciones_base)
total_pagado_global = sum(item["valor"] * item["pagadas"] if "total" in item else (item["valor"] if item.get("pagadas", False) else 0) for item in st.session_state.obligaciones_base)
porcentaje_global = int((total_pagado_global / total_deuda_global) * 100) if total_deuda_global > 0 else 0

st.sidebar.markdown(f"""
<div class="global-dark-box-sidebar">
    <div style="font-size: 0.75rem; font-weight: 800; text-transform: uppercase;">👑 Total Global Deudas</div>
    <div style="font-size: 1.15rem; font-weight: 900; color: #FFFFFF;">{formato_COP(total_deuda_global)}</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"""
<div class="global-dark-box-sidebar">
    <div style="font-size: 0.75rem; font-weight: 800; text-transform: uppercase;">🚀 Avance Global</div>
    <div style="font-size: 1.15rem; font-weight: 900; color: #FCE4EC;">{porcentaje_global}% <span style="font-size: 0.85rem; color: #FFE082;">({formato_COP(total_pagado_global)})</span></div>
</div>
""", unsafe_allow_html=True)

# TABLA RÁPIDA DE OBLIGACIONES
st.markdown("### ⚡ Control de Pagos de la Quincena")

cols_header = st.columns([3.5, 2, 2, 1.5, 1.5])
with cols_header[0]: st.markdown("**Obligación**")
with cols_header[1]: st.markdown("**Valor**")
with cols_header[2]: st.markdown("**Cuotas / Vence**")
with cols_header[3]: st.markdown("**Estado**")
with cols_header[4]: st.markdown("**Acción**")

for item in st.session_state.obligaciones_base:
    if item["periodo"] != periodo_filtro:
        continue
    
    item_id = item["id"]
    esta_pagado = pagos_actuales.get(item_id, False)
    
    st.markdown('<div class="kiut-card" style="padding: 6px 10px; margin-bottom: 4px;">', unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns([3.5, 2, 2, 1.5, 1.5])
    
    with c1:
        st.markdown(f"**{item['nombre']}** <span style='font-size:0.75rem; color:#8E24AA;'>({item['tipo']})</span>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"**{formato_COP(item['valor'])}**", unsafe_allow_html=True)
    with c3:
        if "total" in item:
            st.markdown(f"{item['pagadas']}/{item['total']} cuotas", unsafe_allow_html=True)
        else:
            st.markdown(f"Vence: {item.get('fecha_pago', '-')}", unsafe_allow_html=True)
    with c4:
        st.markdown("✅ Pagado" if esta_pagado else "⏳ Pendiente", unsafe_allow_html=True)
    with c5:
        if not esta_pagado:
            if st.button("Pagar", key=f"pagar_{clave_periodo_actual}_{item_id}"):
                st.session_state.pagos_por_periodo[clave_periodo_actual][item_id] = True
                if "total" in item and item["pagadas"] < item["total"]:
                    item["pagadas"] += 1
                st.rerun()
        else:
            if st.button("Deshacer", key=f"deshacer_{clave_periodo_actual}_{item_id}"):
                st.session_state.pagos_por_periodo[clave_periodo_actual][item_id] = False
                if "total" in item and item["pagadas"] > 0:
                    item["pagadas"] -= 1
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# GESTIÓN Y HERRAMIENTAS
tab_deudas, tab_prestamos, tab_extras = st.tabs(["+ Nueva Deuda", "Cuentas por Cobrar", "Imprevistos & Excel"])

with tab_deudas:
    with st.form(key="form_nueva_deuda_main"):
        col_nd1, col_nd2 = st.columns(2)
        with col_nd1:
            n_nombre = st.text_input("Nombre")
            n_valor_cuota = st.number_input("Valor Cuota", min_value=0.0, step=10000.0)
        with col_nd2:
            n_total_cuotas = st.number_input("Total Cuotas", min_value=1, value=1, step=1)
            n_periodo = st.selectbox("Quincena", ["Mitad de Mes", "Fin de Mes"])
        
        n_fecha_pago = st.text_input("Fecha / Frecuencia")
        if st.form_submit_button("Guardar Deuda") and n_nombre and n_valor_cuota > 0:
            nuevo_id = f"deuda_nueva_{len(st.session_state.obligaciones_base)}"
            st.session_state.obligaciones_base.append({
                "id": nuevo_id, "nombre": n_nombre, "valor": n_valor_cuota,
                "tipo": "Crédito Nuevo", "total": int(n_total_cuotas), "pagadas": 0,
                "periodo": n_periodo, "fecha_pago": n_fecha_pago if n_fecha_pago else "Por definir"
            })
            st.success("¡Guardado!")
            st.rerun()

with tab_prestamos:
    with st.form(key="form_prestamo_main"):
        col_pr1, col_pr2 = st.columns(2)
        with col_pr1:
            p_deudor = st.text_input("Deudor")
            p_valor = st.number_input("Monto", min_value=0.0, step=10000.0)
        with col_pr2:
            p_fecha = st.text_input("Fecha de pago")
            
        if st.form_submit_button("Guardar Préstamo") and p_deudor and p_valor > 0:
            st.session_state.prestamos_por_cobrar.append({"deudor": p_deudor, "valor": p_valor, "fecha_pago": p_fecha or "Por definir"})
            st.success("¡Registrado!")
            st.rerun()

    if st.session_state.prestamos_por_cobrar:
        for idx_p, prestamo in enumerate(st.session_state.prestamos_por_cobrar):
            c_p1, c_p2, c_p3 = st.columns([3, 3, 1])
            with c_p1: st.markdown(f"**{prestamo['deudor']}**")
            with c_p2: st.markdown(f"{formato_COP(prestamo['valor'])} (Paga: {prestamo['fecha_pago']})")
            with c_p3:
                if st.button("Cobrado", key=f"cobrado_{idx_p}"):
                    st.session_state.prestamos_por_cobrar.pop(idx_p)
                    st.rerun()

with tab_extras:
    col_ext1, col_ext2 = st.columns(2)
    with col_ext1:
        with st.form(key="form_imprevisto_main_central"):
            nombre_imp_m = st.text_input("Imprevisto")
            valor_imp_m = st.number_input("Valor", min_value=0.0, step=10000.0)
            if st.form_submit_button("Registrar Imprevisto") and nombre_imp_m and valor_imp_m > 0:
                st.session_state.imprevistos_por_periodo[clave_periodo_actual].append({"nombre": nombre_imp_m, "valor": valor_imp_m})
                st.success("Registrado")
                st.rerun()
    with col_ext2:
        if st.button("Exportar a Excel (CSV)"):
            df_export = pd.DataFrame(st.session_state.obligaciones_base)
            csv_data = df_export.to_csv(index=False).encode('utf-8')
            st.download_button("Descargar Archivo", data=csv_data, file_name="Finanzas_Tatis.csv", mime="text/csv")
