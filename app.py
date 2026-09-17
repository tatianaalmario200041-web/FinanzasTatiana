import streamlit as st
import pandas as pd
import datetime

st.set_page_config(
    page_title="Finanzas Tatis",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS KiuT: Lilas, morados, rosas suaves y panel lateral totalmente FIJO
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        font-size: 14.5px;
        color: #4A3B5C;
    }
    
    /* Fondo principal súper suave en tonos perla, lila y rosa sutil */
    .main {
        background: linear-gradient(135deg, #FBF8FD 0%, #F5EEF8 50%, #FAF0F5 100%);
    }
    
    /* BARRA LATERAL FIJA Y ESTÁTICA */
    [data-testid="stSidebar"] {
        min-width: 400px;
        max-width: 430px;
        background: linear-gradient(180deg, #F3E5F5 0%, #E1BEE7 100%);
        border-right: 2px solid #D1C4E9;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        position: sticky;
        top: 0px;
        height: 100vh;
        overflow-y: auto;
        padding-bottom: 2rem;
    }
    
    .header-title {
        font-family: 'Montserrat', sans-serif;
        font-weight: 800;
        font-size: 2.5rem;
        background: linear-gradient(135deg, #7B1FA2 0%, #9C27B0 50%, #E91E63 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding-bottom: 0.1rem;
    }
    
    .subtitle {
        text-align: center;
        color: #8E24AA;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 1.2rem;
    }

    .stButton>button {
        background: linear-gradient(135deg, #AB47BC 0%, #EC407A 100%);
        color: white;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        font-weight: 700;
        font-size: 0.9rem;
        border: none;
        box-shadow: 0 4px 12px rgba(171, 71, 188, 0.25);
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #8E24AA 0%, #D81B60 100%);
        color: white;
        transform: translateY(-2px);
    }

    /* Tarjetas de métricas en la barra lateral fija */
    .metric-card-sidebar {
        background-color: #FFFFFF;
        padding: 14px 10px;
        border-radius: 16px;
        box-shadow: 0 6px 16px rgba(156, 39, 176, 0.1);
        border: 2px solid #CE93D8;
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-value-gigante {
        color: #7B1FA2; 
        font-size: 1.65rem; 
        font-weight: 900; 
        margin: 4px 0;
    }

    /* Contenedores centrales armónicos */
    .config-box-central {
        background: rgba(255, 255, 255, 0.85);
        padding: 20px;
        border-radius: 20px;
        border: 2px solid #E1BEE7;
        box-shadow: 0 6px 20px rgba(186, 104, 200, 0.1);
        margin-bottom: 20px;
    }
    
    .kiut-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 18px;
        border: 2px solid #E1BEE7;
        box-shadow: 0 4px 15px rgba(156, 39, 176, 0.06);
        margin-bottom: 14px;
    }

    /* CUADROS MORADOS OSCUROS PARA SIDEBAR */
    .global-dark-box-sidebar {
        background: linear-gradient(135deg, #6A1B9A 0%, #8E24AA 100%);
        padding: 14px;
        border-radius: 16px;
        color: white;
        box-shadow: 0 4px 15px rgba(106, 27, 154, 0.25);
        text-align: center;
        border: 2px solid #CE93D8;
        margin-top: 8px;
        margin-bottom: 8px;
    }

    /* Barra de progreso personalizada KiuT */
    .progress-container {
        width: 100%;
        background-color: #F3E5F5;
        border-radius: 10px;
        height: 14px;
        margin: 6px 0;
        overflow: hidden;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.04);
    }
    .progress-bar-kiut {
        height: 100%;
        background: linear-gradient(135deg, #AB47BC 0%, #EC407A 100%);
        border-radius: 10px;
        transition: width 0.4s ease;
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

        # Fin de Mes (Incluye Addi, Tecnomecánica moto, etc.)
        {"id": "camilo_f", "nombre": "Deuda Camilo (Fin)", "valor": 373500.0, "tipo": "Crédito", "total": 6, "pagadas": 2, "periodo": "Fin de Mes", "fecha_pago": "Día 20 (Nómina)"},
        {"id": "tecno_moto", "nombre": "Tecnomecánica Moto (1ra Cuota)", "valor": 223700.0, "tipo": "Crédito Moto", "total": 6, "pagadas": 0, "periodo": "Fin de Mes", "fecha_pago": "28 de Marzo"},
        {"id": "gas_f", "nombre": "Gas (Fin)", "valor": 390000.0, "tipo": "Servicio Cuotas", "total": 12, "pagadas": 7, "periodo": "Fin de Mes", "fecha_pago": "Día 20 (Nómina)"},
        {"id": "tc_f", "nombre": "Tarjeta de Crédito (TC Fin)", "valor": 160000.0, "tipo": "Crédito TC", "total": 8, "pagadas": 0, "periodo": "Fin de Mes", "fecha_pago": "Día 20 (Nómina)"},
        {"id": "internet_f", "nombre": "Internet Q2", "valor": 77000.0, "tipo": "Fijo", "periodo": "Fin de Mes", "fecha_pago": "Día 20 (Nómina)"},
        {"id": "parq_f", "nombre": "Parqueadero Q2", "valor": 60000.0, "tipo": "Fijo", "periodo": "Fin de Mes", "fecha_pago": "Día 20 (Nómina)"},
        {"id": "libres_f", "nombre": "Gastos Libres Q2", "valor": 100000.0, "tipo": "Libre", "periodo": "Fin de Mes", "fecha_pago": "Día 20 (Nómina)"},
        {"id": "addi_m", "nombre": "Cuota Addi (Mamá)", "valor": 110000.0, "tipo": "Crédito Addi", "total": 3, "pagadas": 1, "periodo": "Fin de Mes", "fecha_pago": "Día 20 (Nómina)"},
    ]

if 'pagos_por_periodo' not in st.session_state:
    st.session_state.pagos_por_periodo = {}
if 'imprevistos_por_periodo' not in st.session_state:
    st.session_state.imprevistos_por_periodo = {}
if 'prestamos_por_cobrar' not in st.session_state:
    st.session_state.prestamos_por_cobrar = []

# --- 2. TÍTULO PRINCIPAL ---
st.markdown('<div class="header-title">Finanzas Tatis</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">💜 Tu Panel KiuT de Control Financiero & Deudas 🌸</div>', unsafe_allow_html=True)

# --- 3. CONFIGURACIÓN BASE Y SELECTOR EN PANTALLA PRINCIPAL ---
st.markdown('<div class="config-box-central">', unsafe_allow_html=True)
st.markdown("### 🌸 Configuración Base y Selección de Periodo")

col_cfg1, col_cfg2, col_cfg3 = st.columns(3)
with col_cfg1:
    saldo_actual_banco = st.number_input("Saldo Actual en Bancolombia (COP)", value=2800000.0, step=100000.0)
with col_cfg2:
    nomina_quincenal_neta = st.number_input("Pago Neto Quincenal Base", value=2200000.0, step=10000.0)
with col_cfg3:
    ingresos_extra = st.number_input("➕ Ingresos Extras (COP)", value=0.0, step=10000.0)

col_sel1, col_sel2 = st.columns(2)
with col_sel1:
    mes_seleccionado = st.selectbox(
        "🌸 Selecciona el Mes:",
        ["Marzo 2026", "Abril 2026", "Mayo 2026", "Junio 2026", "Julio 2026", "Agosto 2026"],
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

if clave_periodo_actual not in st.session_state.pagos_por_periodo:
    st.session_state.pagos_por_periodo[clave_periodo_actual] = {}
if clave_periodo_actual not in st.session_state.imprevistos_por_periodo:
    st.session_state.imprevistos_por_periodo[clave_periodo_actual] = []


# =========================================================================
# --- 4. BARRA LATERAL IZQUIERDA: FIJA Y CON MÉTRICAS GIGANTES ---
# =========================================================================
st.sidebar.markdown(f"## 💜 Panel: {clave_periodo_actual}")

presupuesto_quincena_inicial = nomina_quincenal_neta

pagos_actuales = st.session_state.pagos_por_periodo[clave_periodo_actual]
total_pagado_obligaciones_actual = sum(item["valor"] for item in st.session_state.obligaciones_base if item["periodo"] == periodo_filtro and pagos_actuales.get(item["id"], False))
total_imprevistos = sum(imp["valor"] for imp in st.session_state.imprevistos_por_periodo[clave_periodo_actual])
quincena_que_queda = (presupuesto_quincena_inicial + ingresos_extra) - total_pagado_obligaciones_actual - total_imprevistos

# Tarjetas de métricas gigantes en la barra lateral fija
st.sidebar.markdown(f'''
    <div class="metric-card-sidebar">
        <h4 style="color:#6A1B9A; margin:0; font-size:1rem; font-weight:700;">📥 Ingresos Totales</h4>
        <div class="metric-value-gigante">{formato_COP(presupuesto_quincena_inicial + ingresos_extra)}</div>
    </div>
''', unsafe_allow_html=True)

st.sidebar.markdown(f'''
    <div class="metric-card-sidebar">
        <h4 style="color:#7B1FA2; margin:0; font-size:1rem; font-weight:700;">📤 Pagado Periodo</h4>
        <div class="metric-value-gigante">{formato_COP(total_pagado_obligaciones_actual)}</div>
    </div>
''', unsafe_allow_html=True)

st.sidebar.markdown(f'''
    <div class="metric-card-sidebar">
        <h4 style="color:#AD1457; margin:0; font-size:1rem; font-weight:700;">🚨 Imprevistos</h4>
        <div class="metric-value-gigante">{formato_COP(total_imprevistos)}</div>
    </div>
''', unsafe_allow_html=True)

color_queda = "#00897B" if quincena_que_queda >= 0 else "#E53935"
st.sidebar.markdown(f'''
    <div class="metric-card-sidebar" style="border: 2px solid {color_queda};">
        <h4 style="color:{color_queda}; margin:0; font-size:1.05rem; font-weight:800;">✨ QUEDA ✨</h4>
        <div class="metric-value-gigante" style="color:{color_queda}; font-size:1.8rem;">{formato_COP(quincena_que_queda)}</div>
    </div>
''', unsafe_allow_html=True)

total_deuda_periodo = sum(item["valor"] for item in st.session_state.obligaciones_base if item["periodo"] == periodo_filtro)
porcentaje_periodo = int((total_pagado_obligaciones_actual / total_deuda_periodo) * 100) if total_deuda_periodo > 0 else 0

st.sidebar.markdown(f"💜 **Progreso Periodo: {porcentaje_periodo}%**")
st.sidebar.markdown(f'''
    <div class="progress-container">
        <div class="progress-bar-kiut" style="width: {porcentaje_periodo}%;"></div>
    </div>
''', unsafe_allow_html=True)

# Cuadros globales en la barra lateral
total_deuda_global = sum(item["valor"] * item["total"] if "total" in item else item["valor"] for item in st.session_state.obligaciones_base)
total_pagado_global = sum(item["valor"] * item["pagadas"] if "total" in item else (item["valor"] if item.get("pagadas", False) else 0) for item in st.session_state.obligaciones_base)
porcentaje_global = int((total_pagado_global / total_deuda_global) * 100) if total_deuda_global > 0 else 0

st.sidebar.markdown(f"""
<div class="global-dark-box-sidebar">
    <div style="font-size: 0.9rem; font-weight: 800; text-transform: uppercase;">👑 Total Global Deudas</div>
    <div style="font-size: 1.5rem; font-weight: 900; margin-top: 4px; color: #FFFFFF;">{formato_COP(total_deuda_global)}</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"""
<div class="global-dark-box-sidebar">
    <div style="font-size: 0.9rem; font-weight: 800; text-transform: uppercase;">🚀 Avance Total Deudas</div>
    <div style="font-size: 1.5rem; font-weight: 900; margin-top: 4px; color: #FCE4EC;">{porcentaje_global}% <span style="font-size: 1rem; color: #FFE082;">({formato_COP(total_pagado_global)})</span></div>
</div>
""", unsafe_allow_html=True)


# =========================================================================
# --- 5. PANTALLA PRINCIPAL: OBLIGACIONES Y NUEVAS DEUDAS ---
# =========================================================================
st.markdown(f"### 🎯 Obligaciones a Pagar en: **{clave_periodo_actual}**")

for item in st.session_state.obligaciones_base:
    if item["periodo"] != periodo_filtro:
        continue
        
    item_id = item["id"]
    esta_pagado = pagos_actuales.get(item_id, False)
    
    st.markdown(f'<div class="kiut-card">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([3, 2, 1])
    
    with c1:
        st.markdown(f"<span style='font-size: 1.2rem; font-weight: 800; color: #6A1B9A;'>{item['nombre']}</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='color:#8E24AA; font-size:1.05rem; font-weight:bold;'>[{item['tipo']}] • Cuota: {formato_COP(item['valor'])}</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='color:#7E57C2; font-size:0.9rem;'>📅 Vence: <b>{item.get('fecha_pago', 'N/A')}</b></span>", unsafe_allow_html=True)
        
    with c2:
        if "total" in item:
            pct = int((item["pagadas"] / item["total"]) * 100) if item["total"] > 0 else 100
            pend = item["valor"] * max(0, (item["total"] - item["pagadas"]))
            st.markdown(f"<span style='font-size: 1rem;'>Progreso: <b>{item['pagadas']} de {item['total']} ({pct}%)</b></span>", unsafe_allow_html=True)
            st.markdown(f'''
                <div class="progress-container">
                    <div class="progress-bar-kiut" style="width: {pct}%;"></div>
                </div>
            ''', unsafe_allow_html=True)
            st.markdown(f"<span style='color:#C2185B; font-size:0.95rem; font-weight:bold;'>Faltante total: {formato_COP(pend)}</span>", unsafe_allow_html=True)
        else:
            estado_txt = "🌸 <b>Pagado (100%)</b>" if esta_pagado else "⏳ <b>Pendiente (0%)</b>"
            pct_fijo = 100 if esta_pagado else 0
            st.markdown(f"<span style='font-size: 1rem;'>Estado: {estado_txt}</span>", unsafe_allow_html=True)
            st.markdown(f'''
                <div class="progress-container">
                    <div class="progress-bar-kiut" style="width: {pct_fijo}%;"></div>
                </div>
            ''', unsafe_allow_html=True)
            
    with c3:
        st.markdown("<br>", unsafe_allow_html=True)
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

# --- 6. GESTIÓN DE NUEVAS DEUDAS Y PRÉSTAMOS ---
st.markdown("### 📋 Gestión de Nuevas Deudas y Cuentas por Cobrar")
tab_deudas, tab_prestamos = st.tabs(["💸 Registrar / Ver Nuevas Deudas", "🤝 Dinero que Te Deben"])

with tab_deudas:
    st.markdown("#### Agrega un nuevo crédito o cuota:")
    with st.form(key="form_nueva_deuda_main"):
        col_nd1, col_nd2 = st.columns(2)
        with col_nd1:
            n_nombre = st.text_input("Nombre de la Deuda o Artículo")
            n_valor_cuota = st.number_input("Valor de la Cuota (COP)", min_value=0.0, step=10000.0)
        with col_nd2:
            n_total_cuotas = st.number_input("Número Total de Cuotas", min_value=1, value=1, step=1)
            n_periodo = st.selectbox("¿A qué quincena pertenece?", ["Mitad de Mes", "Fin de Mes"])
        
        n_fecha_pago = st.text_input("Fecha estimada de pago (Ej: Semanal todos los martes)")
        btn_guardar_deuda = st.form_submit_button("💜 Guardar Nueva Deuda en el Sistema")
        
        if btn_guardar_deuda and n_nombre and n_valor_cuota > 0:
            nuevo_id = f"deuda_nueva_{len(st.session_state.obligaciones_base)}"
            st.session_state.obligaciones_base.append({
                "id": nuevo_id,
                "nombre": n_nombre,
                "valor": n_valor_cuota,
                "tipo": "Crédito Nuevo",
                "total": int(n_total_cuotas),
                "pagadas": 0,
                "periodo": n_periodo,
                "fecha_pago": n_fecha_pago if n_fecha_pago else "Por definir"
            })
            st.success(f"¡Deuda '{n_nombre}' guardada con éxito!")
            st.rerun()

with tab_prestamos:
    st.markdown("#### Registra los préstamos o dinero que le diste a alguien y te deben pagar:")
    with st.form(key="form_prestamo_main"):
        col_pr1, col_pr2 = st.columns(2)
        with col_pr1:
            p_deudor = st.text_input("Nombre de la persona que te debe")
            p_valor = st.number_input("Valor Prestado / Por Cobrar (COP)", min_value=0.0, step=10000.0)
        with col_pr2:
            p_fecha = st.text_input("Fecha estimada en que te van a pagar (Ej: 30 de Marzo)")
            
        btn_guardar_prestamo = st.form_submit_button("✨ Guardar Préstamo / Cuenta por Cobrar")
        
        if btn_guardar_prestamo and p_deudor and p_valor > 0:
            st.session_state.prestamos_por_cobrar.append({
                "deudor": p_deudor,
                "valor": p_valor,
                "fecha_pago": p_fecha if p_fecha else "Por definir"
            })
            st.success(f"¡Préstamo de {p_deudor} registrado con éxito!")
            st.rerun()

    st.markdown("---")
    st.markdown("#### 🔍 Listado de Dinero que Te Deben:")
    if st.session_state.prestamos_por_cobrar:
        for idx_p, prestamo in enumerate(st.session_state.prestamos_por_cobrar):
            st.markdown(f'<div class="kiut-card">', unsafe_allow_html=True)
            cp1, cp2, cp3 = st.columns([3, 3, 1])
            with cp1:
                st.markdown(f"👤 **Deudor:** <span style='font-size:1.1rem;'>{prestamo['deudor']}</span>", unsafe_allow_html=True)
                st.markdown(f"💰 **Monto:** <span style='font-size:1.15rem; color:#00897B; font-weight:bold;'>{formato_COP(prestamo['valor'])}</span>", unsafe_allow_html=True)
            with cp2:
                st.markdown(f"📅 **Fecha estimada en que te pagan:** <br><span style='color:#8E24AA; font-weight:bold; font-size:1.1rem;'>{prestamo['fecha_pago']}</span>", unsafe_allow_html=True)
            with cp3:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️ Ya pagó", key=f"cobrado_{idx_p}"):
                    st.session_state.prestamos_por_cobrar.pop(idx_p)
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("🌸 No tienes cuentas por cobrar registradas en este momento. ¡Usa el formulario de arriba para agregarlas!")

st.markdown("---")

# =========================================================================
# --- 7. GASTO IMPREVISTO RÁPIDO Y EXPORTAR EN PANTALLA PRINCIPAL ---
# =========================================================================
st.markdown("### 🛠️ Herramientas y Acciones Rápidas")
col_herram1, col_herram2 = st.columns(2)

with col_herram1:
    st.markdown('<div class="kiut-card">', unsafe_allow_html=True)
    st.markdown("#### 🚨 Gasto Imprevisto Rápido")
    with st.form(key="form_imprevisto_main_central"):
        nombre_imp_m = st.text_input("Descripción del imprevisto")
        valor_imp_m = st.number_input("Valor (COP)", min_value=0.0, step=10000.0, key="val_imp_m")
        btn_agregar_imp_m = st.form_submit_button("💜 Registrar Imprevisto en el Periodo")
        if btn_agregar_imp_m and nombre_imp_m and valor_imp_m > 0:
            st.session_state.imprevistos_por_periodo[clave_periodo_actual].append({"nombre": nombre_imp_m, "valor": valor_imp_m})
            st.success("¡Imprevisto registrado con éxito!")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col_herram2:
    st.markdown('<div class="kiut-card">', unsafe_allow_html=True)
    st.markdown("#### 📊 Exportar Reporte Financiero")
    st.markdown("Guarda todos tus datos actuales y el estado de tus obligaciones directamente en un archivo de Excel (CSV).")
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📥 Generar y Descargar Reporte en Excel"):
        df_export = pd.DataFrame(st.session_state.obligaciones_base)
        csv_data = df_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="💾 Clic aquí para descargar archivo",
            data=csv_data,
            file_name="Finanzas_Tatis_Reporte.csv",
            mime="text/csv"
        )
    st.markdown('</div>', unsafe_allow_html=True)
