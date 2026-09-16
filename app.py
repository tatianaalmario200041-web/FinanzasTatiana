import streamlit as st
import pandas as pd
import datetime

st.set_page_config(
    page_title="Finanzas Tatiana - CyberPink KiuT",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS Ultra KiuT (Tonos Rosas, Morados y Degradados CyberPink)
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
        font-size: 3rem;
        background: linear-gradient(135deg, #9333EA 0%, #DB2777 50%, #F43F5E 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding-bottom: 0.2rem;
        text-shadow: 2px 2px 4px rgba(219, 39, 119, 0.1);
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
        border-radius: 16px;
        padding: 0.6rem 1.2rem;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 12px rgba(236, 72, 153, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #9333EA 0%, #DB2777 100%);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(219, 39, 119, 0.4);
    }
    
    .metric-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 8px 20px rgba(219, 39, 119, 0.12);
        border: 2px solid #F472B6;
        text-align: center;
    }
    
    .period-box {
        background: linear-gradient(135deg, #F3E8FF 0%, #FCE7F3 100%);
        padding: 25px;
        border-radius: 24px;
        border: 3px dashed #EC4899;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.15);
        margin-bottom: 25px;
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
        {"id": "camilo_f", "nombre": "Deuda Camilo (Fin)", "valor": 373500.0, "tipo": "Crédito", "total": 6, "pagadas": 2, "periodo": "Fin de Mes", "fecha_pago": "Día 30/31"},
        {"id": "gas_f", "nombre": "Gas (Fin)", "valor": 390000.0, "tipo": "Servicio Cuotas", "total": 12, "pagadas": 7, "periodo": "Fin de Mes", "fecha_pago": "Día 30/31"},
        {"id": "tc_f", "nombre": "Tarjeta de Crédito (TC Fin)", "valor": 160000.0, "tipo": "Crédito TC", "total": 8, "pagadas": 0, "periodo": "Fin de Mes", "fecha_pago": "Día 30/31"},
        {"id": "internet_f", "nombre": "Internet Q2", "valor": 77000.0, "tipo": "Fijo", "periodo": "Fin de Mes", "fecha_pago": "Día 30/31"},
        {"id": "parq_f", "nombre": "Parqueadero Q2", "valor": 25000.0, "tipo": "Fijo", "periodo": "Fin de Mes", "fecha_pago": "Día 30/31"},
        {"id": "libres_f", "nombre": "Gastos Libres Q2", "valor": 100000.0, "tipo": "Libre", "periodo": "Fin de Mes", "fecha_pago": "Día 30/31"},
        {"id": "addi_p", "nombre": "Addi Puntos", "valor": 110000.0, "tipo": "Crédito Addi", "total": 3, "pagadas": 1, "periodo": "Fin de Mes", "fecha_pago": "Día 30/31"},
        {"id": "addi_m", "nombre": "Addi Movilidad", "valor": 35000.0, "tipo": "Crédito Addi", "total": 3, "pagadas": 1, "periodo": "Fin de Mes", "fecha_pago": "Día 30/31"},
        {"id": "addi_t", "nombre": "Addi Totto", "valor": 15000.0, "tipo": "Crédito Addi", "total": 3, "pagadas": 1, "periodo": "Fin de Mes", "fecha_pago": "Día 30/31"},
    ]

if 'pagos_por_periodo' not in st.session_state:
    st.session_state.pagos_por_periodo = {}

if 'imprevistos_por_periodo' not in st.session_state:
    st.session_state.imprevistos_por_periodo = {}

if 'prestamos_por_cobrar' not in st.session_state:
    st.session_state.prestamos_por_cobrar = []

# --- 2. TÍTULO Y SELECTOR DE QUINCENA PRINCIPAL ---
st.markdown('<div class="header-title">✨ Finanzas Tatiana - CyberPink ✨</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Tu Panel KiuT de Control Financiero e Independiente por Periodo 🌸💜</div>', unsafe_allow_html=True)

# Contenedor especial super visible para el Selector de Quincena
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
        ["Mitad de Mes (Día 15)", "Fin de Mes (Cierre)"],
        key="select_quincena_main"
    )
st.markdown('</div>', unsafe_allow_html=True)

periodo_filtro = "Mitad de Mes" if "Mitad" in quincena_tipo else "Fin de Mes"
clave_periodo_actual = f"{mes_seleccionado} - {periodo_filtro}"
nombre_periodo_corto = f"{mes_seleccionado[:3]}-15" if periodo_filtro == "Mitad de Mes" else f"{mes_seleccionado[:3]}-Fin"

# Inicializar registros independientes para este periodo exacto
if clave_periodo_actual not in st.session_state.pagos_por_periodo:
    st.session_state.pagos_por_periodo[clave_periodo_actual] = {}
if clave_periodo_actual not in st.session_state.imprevistos_por_periodo:
    st.session_state.imprevistos_por_periodo[clave_periodo_actual] = []

st.markdown(f"💖 **Periodo Activo Actual:** `{clave_periodo_actual}` (Los pagos y registros de imprevistos que hagas aquí se quedan guardados exclusivamente para esta quincena).")

st.markdown("---")

# --- 3. SIDEBAR: Configuración y Nuevos Registros con Fechas ---
st.sidebar.header("🌸 Configuración & KiuT Registros")
saldo_actual_banco = st.sidebar.number_input("Saldo Actual en Bancolombia (COP)", value=2800000.0, step=100000.0)
nomina_quincenal_neta = st.sidebar.number_input("Pago Neto Quincenal Base", value=1294007.0, step=10000.0)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🚨 Agregar Gasto Imprevisto")
with st.sidebar.form(key="form_imprevisto"):
    nombre_imp = st.text_input("Descripción del Imprevisto")
    valor_imp = st.number_input("Valor (COP)", min_value=0.0, step=10000.0)
    btn_agregar_imp = st.form_submit_button("🎀 Registrar en este Periodo")
    if btn_agregar_imp and nombre_imp and valor_imp > 0:
        st.session_state.imprevistos_por_periodo[clave_periodo_actual].append({"nombre": nombre_imp, "valor": valor_imp})
        st.success(f"¡Imprevisto agregado a {nombre_periodo_corto}!")
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 💸 Registrar Nueva Deuda")
with st.sidebar.form(key="form_nueva_deuda"):
    n_nombre = st.text_input("Nombre de la Deuda o Artículo")
    n_valor_cuota = st.number_input("Valor de la Cuota (COP)", min_value=0.0, step=10000.0)
    n_total_cuotas = st.number_input("Número Total de Cuotas", min_value=1, value=1, step=1)
    n_periodo = st.selectbox("¿A qué quincena corresponde?", ["Mitad de Mes", "Fin de Mes"])
    n_fecha_pago = st.text_input("Fecha estimada de pago (Ej: 28 de Septiembre)")
    btn_guardar_deuda = st.form_submit_button("💖 Guardar Nueva Deuda")
    
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
        st.success(f"¡Deuda '{n_nombre}' guardada con éxito!")
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 🤝 Dinero que Te Deben")
with st.sidebar.form(key="form_prestamo"):
    p_deudor = st.text_input("¿Quién te debe? (Nombre)")
    p_valor = st.number_input("Valor Prestado / Por Cobrar (COP)", min_value=0.0, step=10000.0)
    p_fecha = st.text_input("Fecha estimada de pago (Ej: 30 de Septiembre)")
    btn_guardar_prestamo = st.form_submit_button("✨ Guardar Préstamo")
    
    if btn_guardar_prestamo and p_deudor and p_valor > 0:
        st.session_state.prestamos_por_cobrar.append({
            "deudor": p_deudor,
            "valor": p_valor,
            "fecha_pago": p_fecha if p_fecha else "Por definir"
        })
        st.success(f"¡Préstamo registrado!")
        st.rerun()


# --- 4. RENDIMIENTO DE LA QUINCENA SELECCIONADA ---
st.markdown(f"### 💸 Rendimiento Financiero para: {clave_periodo_actual}")

col_config1, col_config2 = st.columns(2)
with col_config1:
    presupuesto_quincena_inicial = st.number_input(
        "📥 Valor Inicial / Base de esta Quincena (COP)", 
        value=nomina_quincenal_neta, 
        step=10000.0,
        key=f"input_base_{clave_periodo_actual}"
    )
with col_config2:
    ingresos_extra = st.number_input(
        "➕ Ingresos Extras en este periodo (COP)", 
        value=0.0, 
        step=10000.0,
        key=f"input_extras_{clave_periodo_actual}"
    )

pagos_actuales = st.session_state.pagos_por_periodo[clave_periodo_actual]
total_pagado_obligaciones_actual = 0

for item in st.session_state.obligaciones_base:
    if item["periodo"] == periodo_filtro:
        if pagos_actuales.get(item["id"], False):
            total_pagado_obligaciones_actual += item["valor"]

imprevistos_actuales = st.session_state.imprevistos_por_periodo[clave_periodo_actual]
total_imprevistos = sum(imp["valor"] for imp in imprevistos_actuales)

quincena_que_queda = (presupuesto_quincena_inicial + ingresos_extra) - total_pagado_obligaciones_actual - total_imprevistos

col_q1, col_q2, col_q3, col_q4 = st.columns(4)
with col_q1:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color:#9333EA; font-size:0.9rem;">📥 Ingresos Periodo</h4>
        <h3 style="color:#333; font-size:1.3rem;">{formato_COP(presupuesto_quincena_inicial + ingresos_extra)}</h3>
    </div>
    """, unsafe_allow_html=True)
with col_q2:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color:#DB2777; font-size:0.9rem;">📤 Pagado en Periodo</h4>
        <h3 style="color:#333; font-size:1.3rem;">{formato_COP(total_pagado_obligaciones_actual)}</h3>
    </div>
    """, unsafe_allow_html=True)
with col_q3:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color:#D97706; font-size:0.9rem;">🚨 Imprevistos</h4>
        <h3 style="color:#333; font-size:1.3rem;">{formato_COP(total_imprevistos)}</h3>
    </div>
    """, unsafe_allow_html=True)
with col_q4:
    color_queda = "#10B981" if quincena_que_queda >= 0 else "#EF4444"
    st.markdown(f"""
    <div class="metric-card" style="border: 2px solid {color_queda};">
        <h4 style="color:{color_queda}; font-size:0.9rem;">✨ QUEDA</h4>
        <h3 style="color:#333; font-size:1.3rem;">{formato_COP(quincena_que_queda)}</h3>
    </div>
    """, unsafe_allow_html=True)

if imprevistos_actuales:
    with st.expander(f"📌 Ver Imprevistos de {nombre_periodo_corto}"):
        for idx_imp, imp in enumerate(imprevistos_actuales):
            c_imp1, c_imp2 = st.columns([4, 1])
            with c_imp1:
                st.write(f"• **{imp['nombre']}**: {formato_COP(imp['valor'])}")
            with c_imp2:
                if st.button("❌ Borrar", key=f"del_imp_{clave_periodo_actual}_{idx_imp}"):
                    st.session_state.imprevistos_por_periodo[clave_periodo_actual].pop(idx_imp)
                    st.rerun()

st.markdown("---")

# --- 5. CONTROL DE PAGOS CORRESPONDIENTES A ESTA QUINCENA ---
st.markdown(f"### 🎯 Lo que te corresponde pagar en: **{clave_periodo_actual}**")

for idx, item in enumerate(st.session_state.obligaciones_base):
    if item["periodo"] != periodo_filtro:
        continue
        
    col_i1, col_i2, col_i3, col_i4 = st.columns([3, 2, 2, 2])
    item_id = item["id"]
    esta_pagado_en_periodo = pagos_actuales.get(item_id, False)
    
    fecha_info = f" | 📅 Vence: {item.get('fecha_pago', 'N/A')}" if item.get('fecha_pago') else ""
    
    with col_i1:
        badge_color = "#9333EA" if "Crédito" in item["tipo"] or "Servicio" in item["tipo"] else "#DB2777"
        valor_str = formato_COP(item['valor'])
        sub_label = f"Cuota: {valor_str}" if "total" in item else f"Valor: {valor_str}"
        st.markdown(f"**{item['nombre']}** <br><span style='color:{badge_color}; font-size:0.85rem; font-weight:bold;'>[{item['tipo']}] - {sub_label}{fecha_info}</span>", unsafe_allow_html=True)
    
    with col_i2:
        if "total" in item:
            porcentaje_item = int((item["pagadas"] / item["total"]) * 100) if item["total"] > 0 else 100
            saldo_pendiente = item["valor"] * max(0, (item["total"] - item["pagadas"]))
            estado_q_txt = "🌸 Pagado en este periodo" if esta_pagado_en_periodo else "⏳ Pendiente en este periodo"
            st.markdown(f"Progreso: **{item['pagadas']} de {item['total']} ({porcentaje_item}%)**<br><span style='color:#E11D48; font-size:0.85rem;'>Pendiente total: {formato_COP(saldo_pendiente)}</span><br><span style='font-size:0.75rem; color:#9333EA;'>{estado_q_txt}</span>", unsafe_allow_html=True)
        else:
            estado_txt = "🌸 Pagado en este periodo" if esta_pagado_en_periodo else "⏳ Pendiente en este periodo"
            saldo_fijo = 0 if esta_pagado_en_periodo else item["valor"]
            st.markdown(f"Estado: **{estado_txt}**<br><span style='color:#E11D48; font-size:0.85rem;'>Pendiente: {formato_COP(saldo_fijo)}</span>", unsafe_allow_html=True)
        
    with col_i3:
        if not esta_pagado_en_periodo:
            if st.button(f"🌸 Pagar", key=f"pagar_{clave_periodo_actual}_{item_id}"):
                st.session_state.pagos_por_periodo[clave_periodo_actual][item_id] = True
                if "total" in item and item["pagadas"] < item["total"]:
                    item["pagadas"] += 1
                st.rerun()
        else:
            st.markdown("✨ **¡Registrado!**")
                
    with col_i4:
        if esta_pagado_en_periodo:
            if st.button(f"↩️ Deshacer", key=f"deshacer_{clave_periodo_actual}_{item_id}"):
                st.session_state.pagos_por_periodo[clave_periodo_actual][item_id] = False
                if "total" in item and item["pagadas"] > 0:
                    item["pagadas"] -= 1
                st.rerun()

st.markdown("---")

# --- 6. DINERO QUE TE DEBEN CON FECHAS ---
st.markdown("### 🤝 Dinero que Te Deben (Cuentas por Cobrar)")
if st.session_state.prestamos_por_cobrar:
    for idx_p, prestamo in enumerate(st.session_state.prestamos_por_cobrar):
        col_p1, col_p2, col_p3 = st.columns([3, 3, 1])
        with col_p1:
            st.markdown(f"👤 **Deudor:** {prestamo['deudor']} <br>💰 **Monto:** {formato_COP(prestamo['valor'])}", unsafe_allow_html=True)
        with col_p2:
            st.markdown(f"📅 **Fecha estimada de pago:** <br><span style='color:#9333EA; font-weight:bold; font-size:1.1rem;'>{prestamo['fecha_pago']}</span>", unsafe_allow_html=True)
        with col_p3:
            if st.button("🗑️ Ya pagó", key=f"cobrado_{idx_p}"):
                st.session_state.prestamos_por_cobrar.pop(idx_p)
                st.rerun()
else:
    st.info("No tienes préstamos por cobrar registrados. Puedes agregarlos en la barra lateral.")
