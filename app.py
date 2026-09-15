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
        font-size: 2.8rem;
        background: linear-gradient(135deg, #7C3AED 0%, #DB2777 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #6B21A8;
        font-weight: 600;
        margin-bottom: 2rem;
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
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(219, 39, 119, 0.08);
        border-left: 5px solid #DB2777;
    }
    
    .alert-card-danger {
        background-color: #FEE2E2;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #EF4444;
        color: #991B1B;
        font-weight: bold;
    }
    
    .alert-card-success {
        background-color: #ECFDF5;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #10B981;
        color: #065F46;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Título y subtítulo
st.markdown('<div class="header-title">✨ Finanzas Tatiana ✨</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Control por Quincena Real, Gas Actualizado, Créditos y Ahorros 🌸💜</div>', unsafe_allow_html=True)

# Memoria para créditos y gastos extra
if 'creditos_cuotas' not in st.session_state:
    st.session_state.creditos_cuotas = [
        {"Crédito / Tienda": "Addi Totto", "Valor Cuota Mensual": 15000.0, "Cuotas Totales": 3, "Cuotas Pagadas": 1},
        {"Crédito / Tienda": "Addi Puntos", "Valor Cuota Mensual": 110000.0, "Cuotas Totales": 3, "Cuotas Pagadas": 1},
        {"Crédito / Tienda": "Sistecredito Vestido", "Valor Cuota Mensual": 39000.0, "Cuotas Totales": 4, "Cuotas Pagadas": 2},
        {"Crédito / Tienda": "Sistecredito Sudadera", "Valor Cuota Mensual": 59000.0, "Cuotas Totales": 4, "Cuotas Pagadas": 2},
        {"Crédito / Tienda": "Sistecredito Maleta", "Valor Cuota Mensual": 66000.0, "Cuotas Totales": 4, "Cuotas Pagadas": 2}
    ]

if 'gastos_extra' not in st.session_state:
    st.session_state.gastos_extra = []

# Sidebar de Configuración de Ingresos y Gas
st.sidebar.header("⚙️ Tus Cuentas y Nómina Real")
saldo_actual_banco = st.sidebar.number_input("Saldo Actual en Bancolombia (COP)", value=2800000.0, step=100000.0)
nomina_quincenal_neta = st.sidebar.number_input("Pago Neto por Quincena (Desprendible)", value=1294007.0, step=10000.0)

st.sidebar.subheader("🔥 Servicio de Gas (Actualizado)")
gas_mensual = st.sidebar.number_input("Recibo de Gas Total Mensual", value=780000.0, step=10000.0)
gas_quincenal = gas_mensual / 2  # Se divide equitativamente entre las dos quincenas ($390.000 c/u)

st.sidebar.subheader("📌 Otros Gastos Fijos por Quincena")
camilo_q = st.sidebar.number_input("Cuota Camilo (Cada Quincena)", value=373500.0, step=10000.0)
tc_q = st.sidebar.number_input("Tarjeta de Crédito / TC (Cada Quincena)", value=160000.0, step=10000.0)
gastos_libres_q = st.sidebar.number_input("Gastos Libres (Cada Quincena)", value=100000.0, step=10000.0)

st.markdown("---")

# SECCIÓN 1: Gestión de Cuotas (Addi / Sistecredito)
st.markdown("### 🛍️ Seguimiento de Créditos a Cuotas (Addi / Sistecredito)")

with st.expander("➕ Administrar o ver progreso de tus cuotas", expanded=False):
    col_c1, col_c2, col_c3, col_c4 = st.columns([2, 1, 1, 1])
    with col_c1:
        nombre_credito = st.text_input("Nombre (Ej: Addi Totto...)", placeholder="Tienda")
    with col_c2:
        valor_cuota = st.number_input("Valor Cuota", value=0.0, step=10000.0)
    with col_c3:
        cuotas_tot = st.number_input("Total Cuotas", value=3, min_value=1, step=1)
    with col_c4:
        cuotas_pag = st.number_input("Pagadas", value=0, min_value=0, step=1)
    
    if st.button("Guardar Crédito"):
        if nombre_credito and valor_cuota > 0:
            st.session_state.creditos_cuotas.append({
                "Crédito / Tienda": nombre_credito,
                "Valor Cuota Mensual": valor_cuota,
                "Cuotas Totales": int(cuotas_tot),
                "Cuotas Pagadas": int(cuotas_pag)
            })
            st.success("¡Agregado!")
            st.rerun()

# Mostrar tabla de créditos activos
datos_tabla_creditos = []
for item in st.session_state.creditos_cuotas:
    pendientes = item["Cuotas Totales"] - item["Cuotas Pagadas"]
    deuda_restante = pendientes * item["Valor Cuota Mensual"]
    progreso_pct = int((item["Cuotas Pagadas"] / item["Cuotas Totales"]) * 100) if item["Cuotas Totales"] > 0 else 100
    
    datos_tabla_creditos.append({
        "Crédito / Tienda": item["Crédito / Tienda"],
        "Cuota Mensual": item["Valor Cuota Mensual"],
        "Pagadas": f"{item['Cuotas Pagadas']} de {item['Cuotas Totales']}",
        "Faltantes": pendientes,
        "Deuda Restante": deuda_restante,
        "Avance": f"{progreso_pct}%"
    })

df_creditos_view = pd.DataFrame(datos_tabla_creditos)
st.dataframe(df_creditos_view, use_container_width=True)

if st.button("🗑️ Borrar lista de créditos"):
    st.session_state.creditos_cuotas = []
    st.rerun()

st.markdown("---")

# SECCIÓN 2: Desglose Específico por Quincena (Basado en tu Tabla Real)
st.markdown("### 📊 Desglose de Gastos por Quincena")

col_q1, col_q2 = st.columns(2)

# Quincena 1 (Mitad de mes)
with col_q1:
    st.markdown("#### 🗓️ Quincena 15 (Mitad de Mes)")
    internet_q1 = 55000.0
    parqueadero_q1 = 25000.0
    # Sistecreditos activos en la quincena 1
    sistecredito_total_q1 = 39000.0 + 59000.0 + 66000.0  # Vestido + Sudadera + Maleta
    
    total_gastos_q1 = camilo_q + tc_q + gas_quincenal + internet_q1 + parqueadero_q1 + sistecredito_total_q1 + gastos_libres_q
    
    st.write(f"- Camilo: $ {camilo_q:,.0f}")
    st.write(f"- TC: $ {tc_q:,.0f}")
    st.write(f"- Gas (Actualizado): $ {gas_quincenal:,.0f}")
    st.write(f"- Internet: $ {internet_q1:,.0f}")
    st.write(f"- Parqueadero: $ {parqueadero_q1:,.0f}")
    st.write(f"- Sistecreditos (Vestido, Sudadera, Maleta): $ {sistecredito_total_q1:,.0f}")
    st.write(f"- Gastos Libres: $ {gastos_libres_q:,.0f}")
    st.markdown(f"**Total Gastos Quincena 15: 🔴 $ {total_gastos_q1:,.0f} COP**")
    
    # Saldo tras Q1
    saldo_tras_q1 = saldo_actual_banco - total_gastos_q1
    st.markdown(f"**Saldo Disponible Post-Gastos Q1:** $ {saldo_tras_q1:,.0f} COP")

# Quincena Fin de Mes
with col_q2:
    st.markdown("#### 🗓️ Quincena Fin de Mes")
    internet_q_fin = 77000.0
    parqueadero_q_fin = 25000.0
    # Addis activos en fin de mes
    addi_total_qfin = 110000.0 + 15000.0  # Addi Puntos + Addi Totto
    
    total_gastos_qfin = camilo_q + tc_q + gas_quincenal + internet_q_fin + parqueadero_q_fin + addi_total_qfin + gastos_libres_q
    
    st.write(f"- Camilo: $ {camilo_q:,.0f}")
    st.write(f"- TC: $ {tc_q:,.0f}")
    st.write(f"- Gas (Actualizado): $ {gas_quincenal:,.0f}")
    st.write(f"- Internet: $ {internet_q_fin:,.0f}")
    st.write(f"- Parqueadero: $ {parqueadero_q_fin:,.0f}")
    st.write(f"- Addis (Puntos + Totto): $ {addi_total_qfin:,.0f}")
    st.write(f"- Gastos Libres: $ {gastos_libres_q:,.0f}")
    st.markdown(f"**Total Gastos Fin de Mes: 🔴 $ {total_gastos_qfin:,.0f} COP**")
    
    # Saldo tras Nómina del 20 y fin de mes
    saldo_tras_nomina_real = saldo_tras_q1 + nomina_quincenal_neta
    balance_final_mes = saldo_tras_nomina_real - total_gastos_qfin
    st.markdown(f"**Saldo Tras Nómina Día 20:** $ {saldo_tras_nomina_real:,.0f} COP")

st.markdown("---")

# Tarjetas de Resumen General Real
col_m1, col_m2 = st.columns(2)
with col_m1:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color:#7C3AED;">💳 Saldo Tras Quincena 15</h4>
        <h2>$ {saldo_tras_q1:,.0f} COP</h2>
    </div>
    """, unsafe_allow_html=True)
with col_m2:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color:#DB2777;">✨ Balance Final del Mes (Real)</h4>
        <h2>$ {balance_final_mes:,.0f} COP</h2>
    </div>
    """, unsafe_allow_html=True)

# Alertas inteligentes
st.markdown("### 🚨 Estado y Recomendaciones 'Por Pagar'")
if balance_final_mes < 0:
    st.markdown(f"""
    <div class="alert-card-danger">
        ⚠️ <b>Alerta Financiera:</b> Con el nuevo aumento del gas y tus compromisos actuales, el mes presenta un déficit proyectado de <b>$ {abs(balance_final_mes):,.0f} COP</b>. Te sugiero revisar los gastos libres o ajustar los abonos.
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="alert-card-success">
        ✅ <b>¡Excelente!</b> A pesar del aumento en el gas, tus ingresos netos de nómina cubren perfectamente las obligaciones de ambas quincenas y te queda un sobrante de <b>$ {balance_final_mes:,.0f} COP</b>.
    </div>
    """, unsafe_allow_html=True)
