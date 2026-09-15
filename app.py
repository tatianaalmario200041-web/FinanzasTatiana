import streamlit as st
import pandas as pd
import datetime

st.set_page_config(
    page_title="Finanzas Tatiana - CyberPink",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS modernos (Tonos Rosas y Morados)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,600;0,800;1,400&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }
    
    .main {
        background-color: #FAF5FF;
    }
    
    .header-title {
        font-family: 'Montserrat', sans-serif;
        font-weight: 800;
        font-size: 2.5rem;
        background: linear-gradient(135deg, #7C3AED 0%, #DB2777 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding-bottom: 0.2rem;
    }
    
    .subtitle {
        text-align: center;
        color: #6B21A8;
        font-weight: 600;
        margin-bottom: 1.5rem;
    }

    .stButton>button {
        background: linear-gradient(135deg, #7C3AED 0%, #DB2777 100%);
        color: white;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 6px rgba(124, 58, 237, 0.2);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #6D28D9 0%, #BE185D 100%);
        color: white;
    }
    
    .metric-card {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(219, 39, 119, 0.08);
        border-left: 5px solid #DB2777;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Función para formatear en pesos colombianos ($ 1.294.007)
def formato_COP(valor):
    return f"$ {valor:,.0f}".replace(",", ".")

# Título y subtítulo
st.markdown('<div class="header-title">✨ Finanzas Tatiana ✨</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Panel Limpio, Gráfico de Avance y Chulitos de Pago 🌸💜</div>', unsafe_allow_html=True)

# Memoria de créditos con estado de chulitos por cuota
if 'creditos_cuotas' not in st.session_state:
    st.session_state.creditos_cuotas = [
        {"tienda": "Addi Totto", "valor": 15000.0, "total_cuotas": 3, "pagadas": 1},
        {"tienda": "Addi Puntos", "valor": 110000.0, "total_cuotas": 3, "pagadas": 1},
        {"tienda": "Sistecredito Vestido", "valor": 39000.0, "total_cuotas": 4, "pagadas": 2},
        {"tienda": "Sistecredito Sudadera", "valor": 59000.0, "total_cuotas": 4, "pagadas": 2},
        {"tienda": "Sistecredito Maleta", "valor": 66000.0, "total_cuotas": 4, "pagadas": 2}
    ]

# Sidebar de Configuración Real
st.sidebar.header("⚙️ Tus Cuentas y Nómina")
saldo_actual_banco = st.sidebar.number_input("Saldo Actual en Bancolombia (COP)", value=2800000.0, step=100000.0)
nomina_quincenal_neta = st.sidebar.number_input("Pago Neto Quincenal (Desprendible Davivienda)", value=1294007.0, step=10000.0)

st.sidebar.subheader("🔥 Servicio de Gas")
gas_mensual = st.sidebar.number_input("Recibo de Gas Total Mensual", value=780000.0, step=10000.0)
gas_quincenal = gas_mensual / 2  # $ 390.000 por quincena

st.sidebar.subheader("📌 Gastos Fijos por Quincena")
camilo_q = st.sidebar.number_input("Cuota Camilo (Cada Quincena)", value=373500.0, step=10000.0)
tc_q = st.sidebar.number_input("Tarjeta de Crédito / TC (Cada Quincena)", value=160000.0, step=10000.0)
gastos_libres_q = st.sidebar.number_input("Gastos Libres (Cada Quincena)", value=100000.0, step=10000.0)

st.sidebar.subheader("📉 Deudas Principales")
deuda_negro = st.sidebar.number_input("Deuda Negro (Total)", value=1600000.0, step=50000.0)
rapicredid = st.sidebar.number_input("Rapicredid (Total)", value=350000.0, step=10000.0)

st.markdown("---")

# SECCIÓN SUPERIOR: Gráfico y Métricas de Avance de Créditos
st.markdown("### 📈 Progreso General de Tus Créditos")

total_deuda_inicial = sum(item["valor"] * item["total_cuotas"] for item in st.session_state.creditos_cuotas)
total_pagado_hasta_hoy = sum(item["valor"] * item["pagadas"] for item in st.session_state.creditos_cuotas)
porcentaje_avance_global = int((total_pagado_hasta_hoy / total_deuda_inicial) * 100) if total_deuda_inicial > 0 else 0

col_g1, col_g2, col_g3 = st.columns(3)
with col_g1:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color:#7C3AED; font-size:1rem;">💰 Total Deuda Créditos</h4>
        <h3 style="color:#333;">{formato_COP(total_deuda_inicial)}</h3>
    </div>
    """, unsafe_allow_html=True)
with col_g2:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color:#10B981; font-size:1rem;">✅ Ya Pagado</h4>
        <h3 style="color:#333;">{formato_COP(total_pagado_hasta_hoy)}</h3>
    </div>
    """, unsafe_allow_html=True)
with col_g3:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color:#DB2777; font-size:1rem;">🚀 Avance Total</h4>
        <h3 style="color:#333;">{porcentaje_avance_global}%</h3>
    </div>
    """, unsafe_allow_html=True)

st.progress(porcentaje_avance_global / 100)

st.markdown("---")

# SECCIÓN 1: Control con Chulitos de Pago (Addi / Sistecredito)
st.markdown("### 🛍️ Control de Cuotas con Chulitos (¡Marca cuando pagues!)")
st.write("Selecciona el chulito en la cuota que vayas pagando para actualizar automáticamente tu saldo y avance:")

for idx, item in enumerate(st.session_state.creditos_cuotas):
    col_i1, col_i2, col_i3, col_i4 = st.columns([3, 2, 2, 2])
    
    with col_i1:
        st.markdown(f"**{item['tienda']}** <br><span style='color:gray; font-size:0.85rem;'>Cuota: {formato_COP(item['valor'])}</span>", unsafe_allow_html=True)
    
    with col_i2:
        st.markdown(f"Progreso: **{item['pagadas']} de {item['total_cuotas']}**")
        
    with col_i3:
        # Botón para sumar cuota con chulito
        if st.button(f"✅ Pagar Cuota", key=f"pagar_{idx}"):
            if item['pagadas'] < item['total_cuotas']:
                st.session_state.creditos_cuotas[idx]['pagadas'] += 1
                st.rerun()
                
    with col_i4:
        # Botón para desmarcar si se equivocó
        if st.button(f"↩️ Deshacer", key=f"deshacer_{idx}"):
            if item['pagadas'] > 0:
                st.session_state.creditos_cuotas[idx]['pagadas'] -= 1
                st.rerun()

st.markdown("---")

# SECCIÓN 2: Desglose Limpio por Quincena
st.markdown("### 📊 Desglose Limpio de Gastos por Quincena")

col_q1, col_q2 = st.columns(2)

# Quincena 1
with col_q1:
    st.markdown("#### 🗓️ Quincena 15 (Mitad de Mes)")
    internet_q1 = 55000.0
    parqueadero_q1 = 25000.0
    sistecredito_activo_q1 = sum(item["valor"] for item in st.session_state.creditos_cuotas if "Sistecredito" in item["tienda"] and item["pagadas"] < item["total_cuotas"])
    
    total_gastos_q1 = camilo_q + tc_q + gas_quincenal + internet_q1 + parqueadero_q1 + sistecredito_activo_q1 + gastos_libres_q
    
    st.text(f"• Camilo: {formato_COP(camilo_q)}")
    st.text(f"• Tarjeta de Crédito (TC): {formato_COP(tc_q)}")
    st.text(f"• Gas (Actualizado): {formato_COP(gas_quincenal)}")
    st.text(f"• Internet: {formato_COP(internet_q1)}")
    st.text(f"• Parqueadero: {formato_COP(parqueadero_q1)}")
    st.text(f"• Sistecreditos Activos: {formato_COP(sistecredito_activo_q1)}")
    st.text(f"• Gastos Libres: {formato_COP(gastos_libres_q)}")
    st.markdown(f"**Total Salidas Q15:** 🔴 **{formato_COP(total_gastos_q1)}**")
    
    saldo_tras_q1 = saldo_actual_banco - total_gastos_q1
    st.markdown(f"**Saldo Disponible:** 🟢 **{formato_COP(saldo_tras_q1)}**")

# Quincena Fin de Mes
with col_q2:
    st.markdown("#### 🗓️ Quincena Fin de Mes (Día 20)")
    internet_q_fin = 77000.0
    parqueadero_q_fin = 25000.0
    addi_activo_qfin = sum(item["valor"] for item in st.session_state.creditos_cuotas if "Addi" in item["tienda"] and item["pagadas"] < item["total_cuotas"])
    
    total_gastos_qfin = camilo_q + tc_q + gas_quincenal + internet_q_fin + parqueadero_q_fin + addi_activo_qfin + gastos_libres_q
    
    st.text(f"• Camilo: {formato_COP(camilo_q)}")
    st.text(f"• Tarjeta de Crédito (TC): {formato_COP(tc_q)}")
    st.text(f"• Gas (Actualizado): {formato_COP(gas_quincenal)}")
    st.text(f"• Internet: {formato_COP(internet_q_fin)}")
    st.text(f"• Parqueadero: {formato_COP(parqueadero_q_fin)}")
    st.text(f"• Addis Activas: {formato_COP(addi_activo_qfin)}")
    st.text(f"• Gastos Libres: {formato_COP(gastos_libres_q)}")
    st.markdown(f"**Total Salidas Fin de Mes:** 🔴 **{formato_COP(total_gastos_qfin)}**")
    
    saldo_tras_nomina_real = saldo_tras_q1 + nomina_quincenal_neta
    balance_final_mes = saldo_tras_nomina_real - total_gastos_qfin
    st.markdown(f"**Ingreso Nómina Neta Real:** 🟢 **{formato_COP(nomina_quincenal_neta)}**")
    st.markdown(f"**Balance Final del Mes:** ✨ **{formato_COP(balance_final_mes)}**")

st.markdown("---")

# Resumen de Deudas Principales "Por Pagar"
st.markdown("### 🚨 Obligaciones Mayores 'Por Pagar'")
col_p1, col_p2 = st.columns(2)
with col_p1:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color:#7C3AED; font-size:1rem;">Deuda con Negro</h4>
        <h3 style="color:#333;">{formato_COP(deuda_negro)}</h3>
    </div>
    """, unsafe_allow_html=True)
with col_p2:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color:#DB2777; font-size:1rem;">Rapicredid</h4>
        <h3 style="color:#333;">{formato_COP(rapicredid)}</h3>
    </div>
    """, unsafe_allow_html=True)
