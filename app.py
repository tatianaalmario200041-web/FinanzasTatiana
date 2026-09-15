import streamlit as st
import pandas as pd
import datetime

st.set_page_config(
    page_title="Finanzas Tatiana - CyberPink",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados con tipografía moderna, tonos rosas (#DB2777, #FCE7F3) y morados (#7C3AED, #4C1D95)
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
        text-shadow: 0px 2px 4px rgba(0,0,0,0.05);
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

# Título personalizado con letra estilizada y degradé
st.markdown('<div class="header-title">✨ Finanzas Tatiana ✨</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Control Quincenal, Bolsillos Davivienda, Alertas de Déficit & Recuperación 🌸💜</div>', unsafe_allow_html=True)

# Sidebar de configuración
st.sidebar.header("⚙️ Configuración de Cuentas")
saldo_banco = st.sidebar.number_input("Saldo Actual Bancolombia (COP)", value=2800000, step=100000)
salario_quincena = st.sidebar.number_input("Nómina Esperada Día 20 (COP)", value=2200000, step=100000)

st.sidebar.subheader("📌 Nuevos Gastos Fijos")
gas_mensual = st.sidebar.number_input("Recibo de Gas (Mensual)", value=780000, step=10000)
gas_quincenal = gas_mensual / 2  # Bolsillo quincenal

fondo_emergencia = st.sidebar.number_input("Aporte Fondo de Emergencia (Por quincena)", value=50000, step=10000)

st.sidebar.subheader("📉 Deudas Pendientes")
negro = st.sidebar.number_input("Deuda Negro", value=1600000, step=50000)
camilo = st.sidebar.number_input("Cuota Camilo", value=1000000, step=50000)
rapicredid = st.sidebar.number_input("Rapicredid", value=350000, step=10000)
parqueadero = st.sidebar.number_input("Parqueadero", value=60000, step=5000)

st.markdown("---")

# Registro de Imprevistos
st.markdown("### 📋 Registro de Gastos Imprevistos")
col_impr1, col_impr2 = st.columns(2)
with col_impr1:
    desc_imprevisto = st.text_input("Descripción de Gasto Imprevisto:", "Ej: Compra urgente / Repuesto moto")
with col_impr2:
    monto_imprevisto = st.number_input("Monto Imprevisto (COP):", value=0, step=10000)

# Simulación de Flujo de Caja por Quincena
salidas_q1 = gas_quincenal + parqueadero + fondo_emergencia + monto_imprevisto
balance_q1 = saldo_banco - salidas_q1

saldo_con_nomina = balance_q1 + salario_quincena

salidas_q2 = camilo + gas_quincenal + fondo_emergencia
balance_final = saldo_con_nomina - salidas_q2

# Métricas visuales
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color:#7C3AED;">💳 Saldo Q1 (Actual)</h4>
        <h2>$ {balance_q1:,.0f} COP</h2>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color:#DB2777;">💰 Saldo Post-Nómina (Día 20)</h4>
        <h2>$ {saldo_con_nomina:,.0f} COP</h2>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color:#4C1D95;">✨ Balance Final del Mes</h4>
        <h2>$ {balance_final:,.0f} COP</h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Sistema de Alertas Inteligentes de Déficit y Recuperación
st.markdown("### 🚨 Centro de Alertas y Recuperación Financiera")

if balance_q1 < 0:
    deficit_q1 = abs(balance_q1)
    st.markdown(f"""
    <div class="alert-card-danger">
        ⚠️ ¡DÉFICIT EN LA QUINCENA 1! Te faltan <b>$ {deficit_q1:,.0f} COP</b> para cubrir todos los gastos y bolsillos actuales. 
        <br>💡 <i>Tranquila: Este faltante se compensará de forma automática en cuanto entre tu salario de $ {salario_quincena:,.0f} COP el día 20.</i>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="alert-card-success">
        ✅ ¡Quincena 1 bajo control! Tienes un sobrante de $ {balance_q1:,.0f} COP antes de recibir la nómina.
    </div>
    """, unsafe_allow_html=True)

if balance_final < 0:
    st.markdown(f"""
    <div class="alert-card-danger" style="margin-top: 10px;">
        ⚠️ ¡Alerta de Cierre de Mes! El balance general arroja un déficit total de <b>$ {abs(balance_final):,.0f} COP</b>. Revisa los imprevistos o alguna deuda pendiente.
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="alert-card-success" style="margin-top: 10px;">
        ✅ ¡Mes equilibrado! El dinero de la segunda quincena alcanza perfectamente para cubrir todo y cerrar en positivo.
    </div>
    """, unsafe_allow_html=True)

# Tabla de Proyección detallada
st.markdown("### 📊 Tabla de Movimientos y Proyección Quincenal")
datos_proyeccion = [
    {"Periodo": "Sep-15 (Actual)", "Camilo": 0, "Gas (Bolsillo)": gas_quincenal, "Parqueadero": parqueadero, "Fondo Emergencia": fondo_emergencia, "Imprevistos": monto_imprevisto, "Total Salidas": salidas_q1, "Saldo Restante": balance_q1},
    {"Periodo": "Sep-Fin (Post-Nómina)", "Camilo": camilo, "Gas (Bolsillo)": gas_quincenal, "Parqueadero": 0, "Fondo Emergencia": fondo_emergencia, "Imprevistos": 0, "Total Salidas": salidas_q2, "Saldo Restante": balance_final},
]

df_proyeccion = pd.DataFrame(datos_proyeccion)
st.dataframe(df_proyeccion, use_container_width=True)

# Botón de Exportar
st.markdown("### 📥 Exportar tus Datos Financieros")
if st.button("📊 Generar y Descargar Reporte CSV"):
    csv_data = df_proyeccion.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Haz clic para descargar CSV",
        data=csv_data,
        file_name=f"finanzas_tatiana_{datetime.date.today()}.csv",
        mime='text/csv',
    )
    st.success("¡Reporte exportado con éxito!")
