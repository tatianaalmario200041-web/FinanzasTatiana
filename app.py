import streamlit as st
import pandas as pd
import datetime

st.set_page_config(
    page_title="Finanzas Tatiana - CyberPink KiuT",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS Ultra KiuT
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,600;0,800;1,400&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #FDF4FF 0%, #FAE8FF 50%, #FCE7F3 100%);
    }
    
    .header-title {
        font-family: 'Montserrat', sans-serif;
        font-weight: 800;
        font-size: 2.8rem;
        background: linear-gradient(135deg, #9333EA 0%, #DB2777 50%, #F43F5E 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding-bottom: 0.2rem;
    }
    
    .subtitle {
        text-align: center;
        color: #831843;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    .stButton>button {
        background: linear-gradient(135deg, #A855F7 0%, #EC4899 100%);
        color: white;
        border-radius: 14px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 10px rgba(236, 72, 153, 0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #9333EA 0%, #DB2777 100%);
        color: white;
        transform: translateY(-2px);
    }
    
    .metric-card {
        background-color: #FFFFFF;
        padding: 18px;
        border-radius: 18px;
        box-shadow: 0 6px 16px rgba(219, 39, 119, 0.1);
        border: 2px solid #F472B6;
        text-align: center;
    }
    
    .period-box {
        background: linear-gradient(135deg, #F3E8FF 0%, #FCE7F3 100%);
        padding: 20px;
        border-radius: 20px;
        border: 3px dashed #EC4899;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.15);
        margin-bottom: 20px;
    }
    
    .card-item {
        background-color: #FFFFFF;
        padding: 15px 20px;
        border-radius: 16px;
        border-left: 6px solid #EC4899;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        margin-bottom: 12px;
    }
    </style>
""", unsafe_allow_html=True)

def formato_COP(valor):
    return f"$ {valor:,.0f}".replace(",", ".")

# --- 1. INICIALIZAR ESTADOS ---
if 'obligaciones_base' not in st.session_state:
    st.session_state.obligaciones_base = [
        # Mitad de Mes
        {"id": "camilo_m", "nombre": "Deuda Camilo", "valor": 373500.0, "tipo": "Crédito", "total": 6, "pagadas": 2, "periodo": "Mitad de Mes", "fecha_pago": "Día 15"},
        {"id": "gas_m", "nombre": "Gas", "valor": 390000.0, "tipo": "Servicio Cuotas", "total": 12, "pagadas": 7, "periodo": "Mitad de Mes", "fecha_pago": "Día 15"},
        {"id": "tc_m", "nombre": "Tarjeta de Crédito (TC)", "valor": 160000.0, "tipo": "Crédito TC", "total": 8, "pagadas": 0, "periodo": "Mitad de Mes", "fecha_pago": "Día 15"},
        {"id": "sist_vest", "nombre": "Sistecredito Vestido", "valor": 39000.0, "tipo": "Crédito", "total": 4, "pagadas": 2, "periodo": "Mitad de Mes", "fecha_pago": "Día 15"},
        {"id": "sist_sud", "nombre": "Sistecredito Sudadera", "valor": 59000.0, "tipo": "Crédito", "total": 4, "pagadas": 2, "periodo": "Mitad de Mes", "fecha_pago": "Día 15"},
        {"id": "sist_mal", "nombre": "Sistecredito Maleta", "valor": 66000.0, "tipo": "Crédito", "total": 4, "pagadas": 2, "periodo": "Mitad de Mes", "fecha_pago": "Día 15"},
        {"id": "internet_m", "nombre": "Internet Q1", "valor": 55000.0, "tipo": "Fijo", "periodo": "Mitad de Mes", "fecha_pago": "Día 15"},
        {"id": "parq_m", "nombre": "Parqueadero Q1", "valor": 25000.0, "tipo": "Fijo", "periodo": "Mitad de Mes", "fecha_pago": "Día 15"},
        {"id": "libres_m", "nombre": "Gastos Libres Q1", "valor": 100000.0, "tipo": "Libre", "periodo": "Mitad de Mes", "fecha_pago": "Día 15"},

        # Fin de Mes (Incluye Addi)
        {"id": "camilo_f", "nombre": "Deuda Camilo (Fin)", "valor": 373500.0, "tipo": "Crédito", "total": 6, "pagadas": 2, "periodo": "Fin de Mes", "fecha_pago": "Día 20 (Nómina)"},
        {"id": "gas_f", "nombre": "Gas (Fin)", "valor": 390000.0, "tipo": "Servicio Cuotas", "total": 12, "pagadas": 7, "periodo": "Fin de Mes", "fecha_pago": "Día 20 (Nómina)"},
        {"id": "tc_f", "nombre": "Tarjeta de Crédito (TC Fin)", "valor": 160000.0, "tipo": "Crédito TC", "total": 8, "pagadas": 0, "periodo": "Fin de Mes", "fecha_pago": "Día 20 (Nómina)"},
        {"id": "internet_f", "nombre": "Internet Q2", "valor": 77000.0, "tipo": "Fijo", "periodo": "Fin de Mes", "fecha_pago": "Día 20 (Nómina)"},
        {"id": "parq_f", "nombre": "Parqueadero Q2", "valor": 25000.0, "tipo": "Fijo", "periodo": "Fin de Mes", "fecha_pago": "Día 20 (Nómina)"},
        {"id": "libres_f", "nombre": "Gastos Libres Q2", "valor": 100000.0, "tipo": "Libre", "periodo": "Fin de Mes", "fecha_pago": "Día 20 (Nómina)"},
        {"id": "addi_p", "nombre": "Addi Puntos", "valor": 110000.0, "tipo": "Crédito Addi", "total": 3, "pagadas": 1, "periodo": "Fin de Mes", "fecha_pago": "Día 20 (Nómina)"},
        {"id": "addi_m", "nombre": "Addi Movilidad", "valor": 35000.0, "tipo": "Crédito Addi", "total": 3, "pagadas": 1, "periodo": "Fin de Mes", "fecha_pago": "Día 20 (Nómina)"},
        {"id": "addi_t", "nombre": "Addi Totto", "valor": 15000.0, "tipo": "Crédito Addi", "total": 3, "pagadas": 1, "periodo": "Fin de Mes", "fecha_pago": "Día 20 (Nómina)"},
    ]

if 'pagos_por_periodo' not in st.session_state:
    st.session_state.pagos_por_periodo = {}
if 'imprevistos_por_periodo' not in st.session_state:
    st.session_state.imprevistos_por_periodo = {}
if 'prestamos_por_cobrar' not in st.session_state:
    st.session_state.prestamos_por_cobrar = []

# --- 2. TÍTULO Y SELECTOR DE QUINCENA PRINCIPAL (ARRIBA) ---
st.markdown('<div class="header-title">✨ Finanzas Tatiana - CyberPink ✨</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Tu Panel KiuT de Control Financiero 🌸💜</div>', unsafe_allow_html=True)

st.markdown('<div class="period-box">', unsafe_allow_html=True)
st.markdown("### 🗓️🌸 Selecciona tu Quincena Activa")
col_sel1, col_sel2 = st.columns(2)

with col_sel1:
    mes_seleccionado = st.selectbox(
        "🌸 Selecciona el Mes:",
        ["Agosto 2026", "Septiembre 2026", "Octubre 2026", "Noviembre 2026", "Diciembre 2026", "Enero 2027"],
        key="select_mes_main"
    )
with col_sel2:
    quincena_tipo = st.selectbox(
        "🌸 Selecciona la Quincena:",
        ["Mitad de Mes (Día 15)", "Fin de Mes (Cierre / Día 20)"],
        key="select_quincena_main"
    )
st.markdown('</div>', unsafe_allow_html=True)

periodo_filtro = "Mitad de Mes" if "Mitad" in quincena_tipo else "Fin de Mes"
clave_periodo_actual = f"{mes_seleccionado} - {periodo_filtro}"
nombre_periodo_corto = f"{mes_seleccionado[:3]}-15" if periodo_filtro == "Mitad de Mes" else f"{mes_seleccionado[:3]}-Fin"

if clave_periodo_actual not in st.session_state.pagos_por_periodo:
    st.session_state.pagos_por_periodo[clave_periodo_actual] = {}
if clave_periodo_actual not in st.session_state.imprevistos_por_periodo:
    st.session_state.imprevistos_por_periodo[clave_periodo_actual] = []

st.markdown(f"💖 **Periodo Activo:** `{clave_periodo_actual}` | 💰 **Fecha estimada de ingreso de nómina:** {'Día 15' if periodo_filtro == 'Mitad de Mes' else 'Día 20'}")

st.markdown("---")

# --- 3. SIDEBAR: Nuevos Registros ---
st.sidebar.header("🌸 KiuT Registros")
saldo_actual_banco = st.sidebar.number_input("Saldo Actual en Bancolombia (COP)", value=2800000.0, step=100000.0)
nomina_quincenal_neta = st.sidebar.number_input("Pago Neto Quincenal Base", value=1294007.0, step=10000.0)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🚨 Gasto Imprevisto")
with st.sidebar.form(key="form_imprevisto"):
    nombre_imp = st.text_input("Descripción")
    valor_imp = st.number_input("Valor (COP)", min_value=0.0, step=10000.0)
    btn_agregar_imp = st.form_submit_button("🎀 Registrar Imprevisto")
    if btn_agregar_imp and nombre_imp and valor_imp > 0:
        st.session_state.imprevistos_por_periodo[clave_periodo_actual].append({"nombre": nombre_imp, "valor": valor_imp})
        st.success("¡Agregado!")
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 💸 Registrar Nueva Deuda")
with st.sidebar.form(key="form_nueva_deuda"):
    n_nombre = st.text_input("Nombre de la Deuda")
    n_valor_cuota = st.number_input("Valor de la Cuota (COP)", min_value=0.0, step=10000.0)
    n_total_cuotas = st.number_input("Total de Cuotas", min_value=1, value=1, step=1)
    n_periodo = st.selectbox("¿A qué quincena va?", ["Mitad de Mes", "Fin de Mes"])
    n_fecha_pago = st.text_input("Fecha estimada de pago (Ej: 28 de Septiembre)")
    btn_guardar_deuda = st.form_submit_button("💖 Guardar Deuda")
    
    if btn_guardar_deuda and n_nombre and n_valor_cuota > 0:
        nuevo_id = f"deuda_nueva_{len(st.session_state.obligaciones_base)}"
        st.session_state.obligaciones_base.append({
            "id": nuevo_id,
            "nombre": n_nombre,
            "valor": n_valor_cuota,
            "tipo": "Deuda Nueva",
            "total": int(n_total_cuotas),
            "pagadas": 0,
            "periodo": n_periodo,
            "fecha_pago": n_fecha_pago if n_fecha_pago else "Por definir"
        })
        st.success("¡Nueva deuda guardada!")
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 🤝 Dinero que Te Deben")
with st.sidebar.form(key="form_prestamo"):
    p_deudor = st.text_input("Nombre del Deudor")
    p_valor = st.number_input("Valor (COP)", min_value=0.0, step=10000.0)
    p_fecha = st.text_input("Fecha estimada que te pagan")
    btn_guardar_prestamo = st.form_submit_button("✨ Guardar Préstamo")
    
    if btn_guardar_prestamo and p_deudor and p_valor > 0:
        st.session_state.prestamos_por_cobrar.append({
            "deudor": p_deudor,
            "valor": p_valor,
            "fecha_pago": p_fecha if p_fecha else "Por definir"
        })
        st.success("¡Préstamo guardado!")
        st.rerun()


# --- 4. RENDIMIENTO DE LA QUINCENA ---
st.markdown(f"### 💸 Rendimiento Financiero: {clave_periodo_actual}")

col_config1, col_config2 = st.columns(2)
with col_config1:
    presupuesto_quincena_inicial = st.number_input("📥 Valor Inicial / Base Quincena (COP)", value=nomina_quincenal_neta, step=10000.0, key=f"base_{clave_periodo_actual}")
with col_config2:
    ingresos_extra = st.number_input("➕ Ingresos Extras (COP)", value=0.0, step=10000.0, key=f"extra_{clave_periodo_actual}")

pagos_actuales = st.session_state.pagos_por_periodo[clave_periodo_actual]
total_pagado_obligaciones_actual = sum(item["valor"] for item in st.session_state.obligaciones_base if item["periodo"] == periodo_filtro and pagos_actuales.get(item["id"], False))
total_imprevistos = sum(imp["valor"] for imp in st.session_state.imprevistos_por_periodo[clave_periodo_actual])
quincena_que_queda = (presupuesto_quincena_inicial + ingresos_extra) - total_pagado_obligaciones_actual - total_imprevistos

col_q1, col_q2, col_q3, col_q4 = st.columns(4)
with col_q1:
    st.markdown(f'<div class="metric-card"><h4 style="color:#9333EA; font-size:0.9rem;">📥 Ingresos</h4><h3 style="color:#333; font-size:1.2rem;">{formato_COP(presupuesto_quincena_inicial + ingresos_extra)}</h3></div>', unsafe_allow_html=True)
with col_q2:
    st.markdown(f'<div class="metric-card"><h4 style="color:#DB2777; font-size:0.9rem;">📤 Pagado</h4><h3 style="color:#333; font-size:1.2rem;">{formato_COP(total_pagado_obligaciones_actual)}</h3></div>', unsafe_allow_html=True)
with col_q3:
    st.markdown(f'<div class="metric-card"><h4 style="color:#D97706; font-size:0.9rem;">🚨 Imprevistos</h4><h3 style="color:#333; font-size:1.2rem;">{formato_COP(total_imprevistos)}</h3></div>', unsafe_allow_html=True)
with col_q4:
    color_queda = "#10B981" if quincena_que_queda >= 0 else "#EF4444"
    st.markdown(f'<div class="metric-card" style="border: 2px solid {color_queda};"><h4 style="color:{color_queda}; font-size:0.9rem;">✨ QUEDA</h4><h3 style="color:#333; font-size:1.2rem;">{formato_COP(quincena_que_queda)}</h3></div>', unsafe_allow_html=True)

st.markdown("---")

# --- 5. CONTROL DE PAGOS ORGANIZADO EN TARJETAS LIMPIAS ---
st.markdown(f"### 🎯 Obligaciones a Pagar en: **{clave_periodo_actual}**")

for item in st.session_state.obligaciones_base:
    if item["periodo"] != periodo_filtro:
        continue
        
    item_id = item["id"]
    esta_pagado = pagos_actuales.get(item_id, False)
    
    # Tarjeta limpia organizada
    st.markdown(f'<div class="card-item">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([3, 2, 1])
    
    with c1:
        st.markdown(f"**{item['nombre']}**")
        st.markdown(f"<span style='color:#9333EA; font-size:0.85rem; font-weight:bold;'>[{item['tipo']}] • Cuota: {formato_COP(item['valor'])}</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='color:#64748B; font-size:0.8rem;'>📅 Fecha estimada de pago: <b>{item.get('fecha_pago', 'N/A')}</b></span>", unsafe_allow_html=True)
        
    with c2:
        if "total" in item:
            pct = int((item["pagadas"] / item["total"]) * 100) if item["total"] > 0 else 100
            pend = item["valor"] * max(0, (item["total"] - item["pagadas"]))
            st.markdown(f"Progreso: **{item['pagadas']} de {item['total']} ({pct}%)**")
            st.markdown(f"<span style='color:#E11D48; font-size:0.8rem;'>Faltante total: {formato_COP(pend)}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"Estado: {'🌸 **Pagado**' if esta_pagado else '⏳ **Pendiente**'}")
            
    with c3:
        if not esta_pagado:
            if st.button("🌸 Pagar", key=f"pagar_{clave_periodo_actual}_{item_id}"):
                st.session_state.pagos_por_periodo[clave_periodo_actual][item_id] = True
                if "total" in item and item["pagadas"] < item["total"]:
                    item["pagadas"] += 1
                st.rerun()
        else:
            if st.button("↩️ Deshacer", key=f"deshacer_{clave_periodo_actual}_{item_id}"):
                st.session_state.pagos_por_periodo[clave_periodo_actual][item_id] = False
                if "total" in item and item["pagadas"] > 0:
                    item["pagadas"] -= 1
                st.rerun()
                
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# --- 6. DINERO QUE TE DEBEN (CON FECHAS VISIBLES) ---
st.markdown("### 🤝 Dinero que Te Deben (Cuentas por Cobrar)")
if st.session_state.prestamos_por_cobrar:
    for idx_p, prestamo in enumerate(st.session_state.prestamos_por_cobrar):
        st.markdown(f'<div class="card-item" style="border-left-color: #9333EA;">', unsafe_allow_html=True)
        cp1, cp2, cp3 = st.columns([3, 3, 1])
        with cp1:
            st.markdown(f"👤 **Deudor:** {prestamo['deudor']}")
            st.markdown(f"💰 **Monto:** {formato_COP(prestamo['valor'])}")
        with cp2:
            st.markdown(f"📅 **Fecha estimada en que te pagan:** <br><span style='color:#9333EA; font-weight:bold;'>{prestamo['fecha_pago']}</span>", unsafe_allow_html=True)
        with cp3:
            if st.button("🗑️ Ya pagó", key=f"cobrado_{idx_p}"):
                st.session_state.prestamos_por_cobrar.pop(idx_p)
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("🌸 No tienes préstamos por cobrar registrados. Puedes agregarlos usando la barra lateral izquierda.")
