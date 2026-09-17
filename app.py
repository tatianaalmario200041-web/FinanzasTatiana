import streamlit as st
import pandas as pd
import datetime

st.set_page_config(
    page_title="Finanzas Tatis",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS KiuT: Más rosa, números gigantes y diseño ordenado
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        font-size: 15px;
    }
    
    .main {
        background: linear-gradient(135deg, #FFF0F5 0%, #FFE4E1 50%, #FFC0CB 100%);
    }
    
    /* Barra lateral exclusiva para paneles financieros gigantes */
    [data-testid="stSidebar"] {
        min-width: 400px;
        max-width: 440px;
        background-color: #FFB6C1;
    }
    
    .header-title {
        font-family: 'Montserrat', sans-serif;
        font-weight: 800;
        font-size: 2.5rem;
        background: linear-gradient(135deg, #C71585 0%, #FF1493 50%, #FF69B4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding-bottom: 0.1rem;
    }
    
    .subtitle {
        text-align: center;
        color: #8B008B;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 1rem;
    }

    .stButton>button {
        background: linear-gradient(135deg, #FF1493 0%, #FF69B4 100%);
        color: white;
        border-radius: 14px;
        padding: 0.5rem 1rem;
        font-weight: 700;
        font-size: 0.95rem;
        border: none;
        box-shadow: 0 4px 10px rgba(255, 20, 147, 0.4);
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #C71585 0%, #FF1493 100%);
        color: white;
        transform: translateY(-2px);
    }

    /* Tarjetas de métricas gigantes en la barra lateral */
    .metric-card-sidebar {
        background-color: #FFFFFF;
        padding: 18px 12px;
        border-radius: 20px;
        box-shadow: 0 8px 20px rgba(199, 21, 133, 0.2);
        border: 3px solid #FF69B4;
        text-align: center;
        margin-bottom: 12px;
    }
    .metric-value-gigante {
        color: #C71585; 
        font-size: 1.75rem; 
        font-weight: 900; 
        margin: 6px 0;
    }

    .config-box-central {
        background: rgba(255, 255, 255, 0.85);
        padding: 20px;
        border-radius: 22px;
        border: 3px solid #FF69B4;
        box-shadow: 0 8px 20px rgba(255, 105, 180, 0.2);
        margin-bottom: 25px;
    }
    
    .kiut-card {
        background-color: #FFFFFF;
        padding: 22px;
        border-radius: 20px;
        border: 2.5px solid #FFB6C1;
        box-shadow: 0 6px 18px rgba(255, 20, 147, 0.12);
        margin-bottom: 15px;
    }

    /* CUADROS ROSADOS OSCUROS PARA SIDEBAR */
    .global-dark-box-sidebar {
        background: linear-gradient(135deg, #C71585 0%, #FF1493 100%);
        padding: 16px;
        border-radius: 18px;
        color: white;
        box-shadow: 0 6px 18px rgba(199, 21, 133, 0.4);
        text-align: center;
        border: 2px solid #FFC0CB;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    /* Barra de progreso personalizada KiuT */
    .progress-container {
        width: 100%;
        background-color: #FFE4E1;
        border-radius: 12px;
        height: 16px;
        margin: 8px 0;
        overflow: hidden;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.08);
    }
    .progress-bar-kiut {
        height: 100%;
        background: linear-gradient(135deg, #FF1493 0%, #FF69B4 100%);
        border-radius: 12px;
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

# --- 2. TÍTULO PRINCIPAL ---
st.markdown('<div class="header-title">Finanzas Tatis</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">🌸 Tu Panel KiuT de Control Financiero 🌸</div>', unsafe_allow_html=True)

# --- 3. CONFIGURACIÓN BASE Y SELECTOR EN PANTALLA PRINCIPAL ---
st.markdown('<div class="config-box-central">', unsafe_allow_html=True)
st.markdown("### 🌸 Configuración Base y Selección de Periodo")

col_cfg1, col_cfg2, col_cfg3 = st.columns(3)
with col_cfg1:
    saldo_actual_banco = st.number_input("Saldo Actual en Bancolombia (COP)", value=2800000.0, step=100000.0)
with col_cfg2:
    nomina_quincenal_neta = st.number_input("Pago Neto Quincenal Base", value=1294007.0, step=10000.0)
with col_cfg3:
    ingresos_extra = st.number_input("➕ Ingresos Extras (COP)", value=0.0, step=10000.0)

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

if clave_periodo_actual not in st.session_state.pagos_por_periodo:
    st.session_state.pagos_por_periodo[clave_periodo_actual] = {}
if clave_periodo_actual not in st.session_state.imprevistos_por_periodo:
    st.session_state.imprevistos_por_periodo[clave_periodo_actual] = []


# =========================================================================
# --- 4. BARRA LATERAL IZQUIERDA: PANELES FINANCIEROS GIGANTES Y MÉTRICAS ---
# =========================================================================
st.sidebar.markdown(f"## 🌸 Panel: {clave_periodo_actual}")

presupuesto_quincena_inicial = nomina_quincenal_neta

pagos_actuales = st.session_state.pagos_por_periodo[clave_periodo_actual]
total_pagado_obligaciones_actual = sum(item["valor"] for item in st.session_state.obligaciones_base if item["periodo"] == periodo_filtro and pagos_actuales.get(item["id"], False))
total_imprevistos = sum(imp["valor"] for imp in st.session_state.imprevistos_por_periodo[clave_periodo_actual])
quincena_que_queda = (presupuesto_quincena_inicial + ingresos_extra) - total_pagado_obligaciones_actual - total_imprevistos

# Tarjetas de métricas gigantes en la barra lateral
st.sidebar.markdown(f'''
    <div class="metric-card-sidebar">
        <h4 style="color:#C71585; margin:0; font-size:1.05rem; font-weight:700;">📥 Ingresos Totales</h4>
        <div class="metric-value-gigante">{formato_COP(presupuesto_quincena_inicial + ingresos_extra)}</div>
    </div>
''', unsafe_allow_html=True)

st.sidebar.markdown(f'''
    <div class="metric-card-sidebar">
        <h4 style="color:#FF1493; margin:0; font-size:1.05rem; font-weight:700;">📤 Pagado Periodo</h4>
        <div class="metric-value-gigante">{formato_COP(total_pagado_obligaciones_actual)}</div>
    </div>
''', unsafe_allow_html=True)

st.sidebar.markdown(f'''
    <div class="metric-card-sidebar">
        <h4 style="color:#FF8C00; margin:0; font-size:1.05rem; font-weight:700;">🚨 Imprevistos</h4>
        <div class="metric-value-gigante">{formato_COP(total_imprevistos)}</div>
    </div>
''', unsafe_allow_html=True)

color_queda = "#10B981" if quincena_que_queda >= 0 else "#EF4444"
st.sidebar.markdown(f'''
    <div class="metric-card-sidebar" style="border: 3px solid {color_queda};">
        <h4 style="color:{color_queda}; margin:0; font-size:1.1rem; font-weight:800;">✨ QUEDA ✨</h4>
        <div class="metric-value-gigante" style="color:{color_queda}; font-size:2rem;">{formato_COP(quincena_que_queda)}</div>
    </div>
''', unsafe_allow_html=True)

total_deuda_periodo = sum(item["valor"] for item in st.session_state.obligaciones_base if item["periodo"] == periodo_filtro)
porcentaje_periodo = int((total_pagado_obligaciones_actual / total_deuda_periodo) * 100) if total_deuda_periodo > 0 else 0

st.sidebar.markdown(f"🌸 **Progreso Periodo: {porcentaje_periodo}%**")
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
    <div style="font-size: 0.95rem; font-weight: 800; text-transform: uppercase;">👑 Total Global Deudas</div>
    <div style="font-size: 1.6rem; font-weight: 900; margin-top: 6px; color: #FFFFFF;">{formato_COP(total_deuda_global)}</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"""
<div class="global-dark-box-sidebar">
    <div style="font-size: 0.95rem; font-weight: 800; text-transform: uppercase;">🚀 Avance Total Deudas</div>
    <div style="font-size: 1.6rem; font-weight: 900; margin-top: 6px; color: #FFF0F5;">{porcentaje_global}% <span style="font-size: 1.1rem; color: #FFD700;">({formato_COP(total_pagado_global)})</span></div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🚨 Gasto Imprevisto Rápido")
with st.sidebar.form(key="form_imprevisto_side"):
    nombre_imp = st.text_input("Descripción")
    valor_imp = st.number_input("Valor (COP)", min_value=0.0, step=10000.0)
    btn_agregar_imp = st.form_submit_button("🎀 Registrar Imprevisto")
    if btn_agregar_imp and nombre_imp and valor_imp > 0:
        st.session_state.imprevistos_por_periodo[clave_periodo_actual].append({"nombre": nombre_imp, "valor": valor_imp})
        st.success("¡Agregado!")
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Exportar a Excel")
if st.sidebar.button("📥 Descargar Reporte en Excel"):
    df_export = pd.DataFrame(st.session_state.obligaciones_base)
    csv_data = df_export.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="💾 Clic para guardar archivo",
        data=csv_data,
        file_name="Finanzas_Tatis_Reporte.csv",
        mime="text/csv"
    )


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
        st.markdown(f"<span style='font-size: 1.25rem; font-weight: 800; color: #8B008B;'>{item['nombre']}</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='color:#C71585; font-size:1.1rem; font-weight:bold;'>[{item['tipo']}] • Cuota: {formato_COP(item['valor'])}</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='color:#64748B; font-size:0.95rem;'>📅 Vence: <b>{item.get('fecha_pago', 'N/A')}</b></span>", unsafe_allow_html=True)
        
    with c2:
        if "total" in item:
            pct = int((item["pagadas"] / item["total"]) * 100) if item["total"] > 0 else 100
            pend = item["valor"] * max(0, (item["total"] - item["pagadas"]))
            st.markdown(f"<span style='font-size: 1.05rem;'>Progreso: <b>{item['pagadas']} de {item['total']} ({pct}%)</b></span>", unsafe_allow_html=True)
            st.markdown(f'''
                <div class="progress-container">
                    <div class="progress-bar-kiut" style="width: {pct}%;"></div>
                </div>
            ''', unsafe_allow_html=True)
            st.markdown(f"<span style='color:#C71585; font-size:1rem; font-weight:bold;'>Faltante total: {formato_COP(pend)}</span>", unsafe_allow_html=True)
        else:
            estado_txt = "🌸 <b>Pagado (100%)</b>" if esta_pagado else "⏳ <b>Pendiente (0%)</b>"
            pct_fijo = 100 if esta_pagado else 0
            st.markdown(f"<span style='font-size: 1.05rem;'>Estado: {estado_txt}</span>", unsafe_allow_html=True)
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
        btn_guardar_deuda = st.form_submit_button("💖 Guardar Nueva Deuda en el Sistema")
        
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
            p_fecha = st.text_input("Fecha estimada en que te van a pagar (Ej: 30 de Septiembre)")
            
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
                st.markdown(f"👤 **Deudor:** <span style='font-size:1.15rem;'>{prestamo['deudor']}</span>", unsafe_allow_html=True)
                st.markdown(f"💰 **Monto:** <span style='font-size:1.2rem; color:#10B981; font-weight:bold;'>{formato_COP(prestamo['valor'])}</span>", unsafe_allow_html=True)
            with cp2:
                st.markdown(f"📅 **Fecha estimada en que te pagan:** <br><span style='color:#C71585; font-weight:bold; font-size:1.2rem;'>{prestamo['fecha_pago']}</span>", unsafe_allow_html=True)
            with cp3:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️ Ya pagó", key=f"cobrado_{idx_p}"):
                    st.session_state.prestamos_por_cobrar.pop(idx_p)
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("🌸 No tienes cuentas por cobrar registradas en este momento. ¡Usa el formulario de arriba para agregarlas!")
