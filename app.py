import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Finanzas Tatis",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"  # CAMBIADO A COLLAPSED PARA QUE EN CELULAR ABRA PERFECTO SIN TAPAR
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        font-size: 15px; /* LETRA MÁS GRANDE Y CÓMODA */
        color: #4A3B5C;
    }
    
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        max-width: 100% !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    .main {
        background: linear-gradient(135deg, #FAF5FD 0%, #F3E5F5 40%, #FCE4EC 100%);
    }
    
    /* CONFIGURACIÓN SIDEBAR PARA CELULAR Y PC */
    [data-testid="stSidebar"] {
        min-width: 320px;
        max-width: 360px;
        background: linear-gradient(180deg, #F3E5F5 0%, #E1BEE7 100%);
        border-right: 2px solid #BA68C8;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* TÍTULO HERMOSO CON ROSAS Y TONOS LILAS/MORADOS PERFECTOS */
    .header-container {
        text-align: center;
        background: linear-gradient(135deg, #7B1FA2 0%, #9C27B0 50%, #D81B60 100%);
        padding: 20px 15px;
        border-radius: 18px;
        border: 2px solid #E1BEE7;
        box-shadow: 0 6px 20px rgba(156, 39, 176, 0.25);
        margin-bottom: 18px;
    }
    
    .header-title {
        font-family: 'Montserrat', sans-serif;
        font-weight: 900;
        font-size: 1.9rem;
        color: #FFFFFF;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        margin: 0;
        padding: 0;
        letter-spacing: 0.8px;
    }

    /* BOTONES ESTILIZADOS KIUT */
    .stButton>button {
        background: linear-gradient(135deg, #9C27B0 0%, #E91E63 100%);
        color: white;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        font-weight: 700;
        font-size: 0.95rem;
        border: none;
        box-shadow: 0 4px 12px rgba(156, 39, 176, 0.3);
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #7B1FA2 0%, #C2185B 100%);
        box-shadow: 0 6px 15px rgba(156, 39, 176, 0.4);
        transform: translateY(-1px);
        color: white;
    }

    /* BOTÓN FLOTANTE / ESPECIAL DE GASTO HORMIGA */
    .btn-hormiga-container {
        background: linear-gradient(135deg, #E1BEE7 0%, #F8BBD0 100%);
        padding: 14px 16px;
        border-radius: 16px;
        border: 2px dashed #8E24AA;
        box-shadow: 0 4px 14px rgba(142, 36, 170, 0.18);
        margin-bottom: 18px;
        text-align: center;
    }

    .metric-card-sidebar {
        background-color: #FFFFFF;
        padding: 12px 14px;
        border-radius: 14px;
        box-shadow: 0 4px 12px rgba(156, 39, 176, 0.1);
        border: 2px solid #CE93D8;
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-value-gigante {
        color: #7B1FA2; 
        font-size: 1.5rem; 
        font-weight: 900; 
        margin: 3px 0;
    }

    .config-box-compact {
        background: rgba(255, 255, 255, 0.98);
        padding: 15px;
        border-radius: 16px;
        border: 2px solid #D1C4E9;
        box-shadow: 0 4px 15px rgba(156, 39, 176, 0.08);
        margin-bottom: 18px;
    }
    
    .kiut-card {
        background-color: #FFFFFF;
        padding: 14px 16px;
        border-radius: 14px;
        border: 1.5px solid #E1BEE7;
        box-shadow: 0 3px 12px rgba(156, 39, 176, 0.06);
        margin-bottom: 10px;
    }

    .global-dark-box-sidebar {
        background: linear-gradient(135deg, #6A1B9A 0%, #8E24AA 100%);
        padding: 12px;
        border-radius: 14px;
        color: white;
        text-align: center;
        border: 2px solid #CE93D8;
        margin-top: 8px;
        margin-bottom: 8px;
        box-shadow: 0 4px 10px rgba(106, 27, 154, 0.2);
    }

    .progress-container {
        width: 100%;
        background-color: #F3E5F5;
        border-radius: 8px;
        height: 12px;
        margin: 8px 0;
        overflow: hidden;
        border: 1px solid #E1BEE7;
    }
    .progress-bar-kiut {
        height: 100%;
        background: linear-gradient(135deg, #AB47BC 0%, #EC407A 100%);
        border-radius: 8px;
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

# TÍTULO LIMPIO, HERMOSO Y ELEGANTE
st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🌸 Finanzas Tatis 🌸</h1>
    </div>
""", unsafe_allow_html=True)

# BOTÓN RÁPIDO SUPERIOR PARA GASTO HORMIGA (ESTILO POPUP / PESTAÑITA CHIQUITA Y HERMOSA)
st.markdown('<div class="btn-hormiga-container">', unsafe_allow_html=True)
with st.expander("✨ ☕ Registrar Gasto Hormiga / Imprevisto Rápido (Click Aquí)", expanded=False):
    with st.form(key="form_flash_celular_top"):
        flash_nombre = st.text_input("¿En qué gastaste?", placeholder="Ej. Un cafecito, mecato...")
        flash_valor = st.number_input("Valor (COP)", min_value=0.0, step=2000.0)
        
        st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)
        submit_flash = st.form_submit_button("💾 Guardar Gasto Hormiga 💖")
        
        if submit_flash and flash_nombre and flash_valor > 0:
            clave_temp_act = f"{st.session_state.get('select_mes_main', 'Marzo 2026')} - {'Mitad de Mes' if 'Mitad' in st.session_state.get('select_quincena_main', 'Mitad de Mes') else 'Fin de Mes'}"
            if clave_temp_act not in st.session_state.imprevistos_por_periodo:
                st.session_state.imprevistos_por_periodo[clave_temp_act] = []
            st.session_state.imprevistos_por_periodo[clave_temp_act].append({"nombre": flash_nombre, "valor": flash_valor})
            st.success("¡Gasto guardado al instante con éxito! 💖")
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Configuración compacta superior adaptada para celular (en columnas verticales u organizadas)
st.markdown('<div class="config-box-compact">', unsafe_allow_html=True)
col_cfg1, col_cfg2 = st.columns(2)
with col_cfg1:
    st.markdown("<span style='font-size:0.85rem; font-weight:700; color:#7B1FA2;'>Banco (COP)</span>", unsafe_allow_html=True)
    saldo_actual_banco = st.number_input("Banco (COP)", value=2800000.0, step=100000.0, label_visibility="collapsed")
    
    st.markdown("<span style='font-size:0.85rem; font-weight:700; color:#7B1FA2;'>Nómina Base</span>", unsafe_allow_html=True)
    nomina_quincenal_neta = st.number_input("Nómina Base", value=2200000.0, step=10000.0, label_visibility="collapsed")

with col_cfg2:
    st.markdown("<span style='font-size:0.85rem; font-weight:700; color:#7B1FA2;'>Extras (COP)</span>", unsafe_allow_html=True)
    ingresos_extra = st.number_input("Extras (COP)", value=0.0, step=10000.0, label_visibility="collapsed")
    
    st.markdown("<span style='font-size:0.85rem; font-weight:700; color:#7B1FA2;'>Mes</span>", unsafe_allow_html=True)
    mes_seleccionado = st.selectbox("Mes", ["Marzo 2026", "Abril 2026", "Mayo 2026", "Junio 2026", "Julio 2026", "Agosto 2026", "Septiembre 2026"], key="select_mes_main", label_visibility="collapsed")

st.markdown("<span style='font-size:0.85rem; font-weight:700; color:#7B1FA2;'>Quincena</span>", unsafe_allow_html=True)
quincena_tipo = st.selectbox("Quincena", ["Mitad de Mes (Día 15)", "Fin de Mes (Día 20)"], key="select_quincena_main", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

periodo_filtro = "Mitad de Mes" if "Mitad" in quincena_tipo else "Fin de Mes"
clave_periodo_actual = f"{mes_seleccionado} - {periodo_filtro}"

if clave_periodo_actual not in st.session_state.pagos_por_periodo:
    st.session_state.pagos_por_periodo[clave_periodo_actual] = {}
if clave_periodo_actual not in st.session_state.imprevistos_por_periodo:
    st.session_state.imprevistos_por_periodo[clave_periodo_actual] = []

# BARRA LATERAL PERFECTAMENTE DISTRIBUIDA
st.sidebar.markdown(f"### 💜 {clave_periodo_actual}")
presupuesto_quincena_inicial = nomina_quincenal_neta
pagos_actuales = st.session_state.pagos_por_periodo[clave_periodo_actual]
total_pagado_obligaciones_actual = sum(item["valor"] for item in st.session_state.obligaciones_base if item["periodo"] == periodo_filtro and pagos_actuales.get(item["id"], False))
total_imprevistos = sum(imp["valor"] for imp in st.session_state.imprevistos_por_periodo[clave_periodo_actual])
quincena_que_queda = (presupuesto_quincena_inicial + ingresos_extra) - total_pagado_obligaciones_actual - total_imprevistos

st.sidebar.markdown(f'''
    <div class="metric-card-sidebar">
        <h6 style="color:#6A1B9A; margin:0; font-weight:700;">📥 Ingresos Totales</h6>
        <div class="metric-value-gigante">{formato_COP(presupuesto_quincena_inicial + ingresos_extra)}</div>
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
        <h6 style="color:#AD1457; margin:0; font-weight:700;">🚨 Imprevistos / Hormiga</h6>
        <div class="metric-value-gigante">{formato_COP(total_imprevistos)}</div>
    </div>
''', unsafe_allow_html=True)

color_queda = "#00897B" if quincena_que_queda >= 0 else "#E53935"
st.sidebar.markdown(f'''
    <div class="metric-card-sidebar" style="border: 2.5px solid {color_queda}; background: #FFFDE7;">
        <h6 style="color:{color_queda}; margin:0; font-weight:800;">✨ LO QUE QUEDA ✨</h6>
        <div class="metric-value-gigante" style="color:{color_queda}; font-size:1.6rem;">{formato_COP(quincena_que_queda)}</div>
    </div>
''', unsafe_allow_html=True)

total_deuda_periodo = sum(item["valor"] for item in st.session_state.obligaciones_base if item["periodo"] == periodo_filtro)
porcentaje_periodo = int((total_pagado_obligaciones_actual / total_deuda_periodo) * 100) if total_deuda_periodo > 0 else 0

st.sidebar.markdown(f"<div style='font-weight:700; color:#4A3B5C; margin-top:10px;'>Progreso Periodo: {porcentaje_periodo}%</div>", unsafe_allow_html=True)
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
    <div style="font-size: 0.85rem; font-weight: 800; text-transform: uppercase; letter-spacing:0.5px;">👑 Total Global Deudas</div>
    <div style="font-size: 1.3rem; font-weight: 900; color: #FFFFFF; margin-top:4px;">{formato_COP(total_deuda_global)}</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"""
<div class="global-dark-box-sidebar">
    <div style="font-size: 0.85rem; font-weight: 800; text-transform: uppercase; letter-spacing:0.5px;">🚀 Avance Global</div>
    <div style="font-size: 1.3rem; font-weight: 900; color: #FCE4EC; margin-top:4px;">{porcentaje_global}% <span style="font-size: 0.95rem; color: #FFE082;">({formato_COP(total_pagado_global)})</span></div>
</div>
""", unsafe_allow_html=True)

# TABLA RÁPIDA DE OBLIGACIONES PERFECTAMENTE DISEÑADA PARA CELULAR Y PC
st.markdown("<h3 style='color: #6A1B9A; font-weight: 800; margin-top: 15px;'>⚡ Control de Pagos de la Quincena</h3>", unsafe_allow_html=True)

for item in st.session_state.obligaciones_base:
    if item["periodo"] != periodo_filtro:
        continue
    
    item_id = item["id"]
    esta_pagado = pagos_actuales.get(item_id, False)
    
    st.markdown('<div class="kiut-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([2.2, 1.2])
    
    with c1:
        st.markdown(f"<span style='font-weight:800; font-size:15px; color:#4A3B5C;'>{item['nombre']}</span><br><span style='font-size:0.8rem; color:#8E24AA; font-weight:700;'>{item['tipo']}</span>", unsafe_allow_html=True)
        if "total" in item:
            st.markdown(f"<span style='font-size:0.85rem; font-weight:600; color:#666;'>Cuota {item['pagadas']}/{item['total']}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<span style='font-size:0.85rem; font-weight:600; color:#666;'>Vence: {item.get('fecha_pago', '-')}</span>", unsafe_allow_html=True)
            
    with c2:
        st.markdown(f"<div style='text-align: right;'><span style='font-weight:900; font-size:15px; color:#7B1FA2;'>{formato_COP(item['valor'])}</span></div>", unsafe_allow_html=True)
        estado_txt = "✅ Pagado" if esta_pagado else "⏳ Pendiente"
        color_est = "#2E7D32" if esta_pagado else "#EF6C00"
        st.markdown(f"<div style='text-align: right; margin-top: 2px;'><span style='font-weight:700; color:{color_est}; font-size:13px;'>{estado_txt}</span></div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
    if not esta_pagado:
        if st.button("Marcar como Pagado ✅", key=f"pagar_{clave_periodo_actual}_{item_id}"):
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

st.markdown("<hr style='border: 1px solid #E1BEE7; margin: 20px 0;'>", unsafe_allow_html=True)

# GESTIÓN Y HERRAMIENTAS ADICIONALES EN TABS CLARAS
tab_deudas, tab_prestamos, tab_extras = st.tabs(["➕ Nueva Deuda", "🤝 Cuentas por Cobrar", "📊 Imprevistos & Excel"])

with tab_deudas:
    st.markdown("<h4 style='color:#7B1FA2;'>Registrar Nueva Obligación o Crédito</h4>", unsafe_allow_html=True)
    with st.form(key="form_nueva_deuda_main"):
        n_nombre = st.text_input("Nombre de la obligación")
        n_valor_cuota = st.number_input("Valor Cuota", min_value=0.0, step=10000.0)
        n_total_cuotas = st.number_input("Total Cuotas", min_value=1, value=1, step=1)
        n_periodo = st.selectbox("Quincena a aplicar", ["Mitad de Mes", "Fin de Mes"])
        n_fecha_pago = st.text_input("Fecha / Frecuencia (Ej. Día 15, 28 de Marzo)")
        
        if st.form_submit_button("Guardar Nueva Deuda 💜") and n_nombre and n_valor_cuota > 0:
            nuevo_id = f"deuda_nueva_{len(st.session_state.obligaciones_base)}"
            st.session_state.obligaciones_base.append({
                "id": nuevo_id, "nombre": n_nombre, "valor": n_valor_cuota,
                "tipo": "Crédito Nuevo", "total": int(n_total_cuotas), "pagadas": 0,
                "periodo": n_periodo, "fecha_pago": n_fecha_pago if n_fecha_pago else "Por definir"
            })
            st.success("¡Deuda guardada correctamente!")
            st.rerun()

with tab_prestamos:
    st.markdown("<h4 style='color:#7B1FA2;'>Préstamos por Cobrar</h4>", unsafe_allow_html=True)
    with st.form(key="form_prestamo_main"):
        p_deudor = st.text_input("Nombre de quien debe")
        p_valor = st.number_input("Monto (COP)", min_value=0.0, step=10000.0)
        p_fecha = st.text_input("Fecha estimada de pago")
            
        if st.form_submit_button("Registrar Préstamo 🤝") and p_deudor and p_valor > 0:
            st.session_state.prestamos_por_cobrar.append({"deudor": p_deudor, "valor": p_valor, "fecha_pago": p_fecha or "Por definir"})
            st.success("¡Préstamo registrado!")
            st.rerun()

    if st.session_state.prestamos_por_cobrar:
        st.markdown("<br>", unsafe_allow_html=True)
        for idx_p, prestamo in enumerate(st.session_state.prestamos_por_cobrar):
            st.markdown('<div class="kiut-card">', unsafe_allow_html=True)
            st.markdown(f"**{prestamo['deudor']}** - {formato_COP(prestamo['valor'])} (Paga: {prestamo['fecha_pago']})")
            if st.button("Cobrado ✅", key=f"cobrado_{idx_p}"):
                st.session_state.prestamos_por_cobrar.pop(idx_p)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

with tab_extras:
    st.markdown("<h4 style='color:#7B1FA2;'>Registro Detallado Imprevistos</h4>", unsafe_allow_html=True)
    with st.form(key="form_imprevisto_main_central"):
        nombre_imp_m = st.text_input("Concepto Imprevisto")
        valor_imp_m = st.number_input("Valor Imprevisto (COP)", min_value=0.0, step=10000.0)
        if st.form_submit_button("Registrar en Periodo") and nombre_imp_m and valor_imp_m > 0:
            st.session_state.imprevistos_por_periodo[clave_periodo_actual].append({"nombre": nombre_imp_m, "valor": valor_imp_m})
            st.success("¡Imprevisto registrado!")
            st.rerun()
            
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#7B1FA2;'>Exportar Datos</h4>", unsafe_allow_html=True)
    if st.button("📥 Descargar Excel (CSV)"):
        df_export = pd.DataFrame(st.session_state.obligaciones_base)
        csv_data = df_export.to_csv(index=False).encode('utf-8')
        st.download_button("Confirmar Descarga", data=csv_data, file_name="Finanzas_Tatis.csv", mime="text/csv")
