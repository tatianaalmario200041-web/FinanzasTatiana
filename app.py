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
st.markdown('<div class="subtitle">Control Real, Nómina Neta, Por Pagar & Progreso de Cuotas (Addi/Sistecredito) 🌸💜</div>', unsafe_allow_html=True)

# Memoria para gastos dinámicos y créditos a cuotas
if 'gastos_extra' not in st.session_state:
    st.session_state.gastos_extra = []

if 'creditos_cuotas' not in st.session_state:
    # Agregamos unos ejemplos iniciales basados en lo que mencionaste
    st.session_state.creditos_cuotas = [
        {"Crédito / Tienda": "Addi Totto", "Valor Cuota Mensual": 85000.0, "Cuotas Totales": 3, "Cuotas Pagadas": 1},
        {"Crédito / Tienda": "Sistecredito Vestido de Baño", "Valor Cuota Mensual": 65000.0, "Cuotas Totales": 4, "Cuotas Pagadas": 2}
    ]

# Sidebar de Configuración Real
st.sidebar.header("⚙️ Tus Cuentas y Nómina Real")
saldo_actual_banco = st.sidebar.number_input("Saldo Actual en Bancolombia (COP)", value=2800000.0, step=100000.0)

st.sidebar.subheader("💼 Nómina Real (Quincenal Neta)")
nomina_quincenal_neta = st.sidebar.number_input("Pago Neto por Quincena (Desprendible)", value=1294007.0, step=10000.0)

st.sidebar.subheader("📌 Gastos Fijos y Bolsillos")
gas_mensual = st.sidebar.number_input("Recibo de Gas (Mensual)", value=780000.0, step=10000.0)
gas_quincenal = gas_mensual / 2  
fondo_emergencia = st.sidebar.number_input("Aporte Fondo de Emergencia (Quincena)", value=50000.0, step=10000.0)
parqueadero = st.sidebar.number_input("Parqueadero", value=60000.0, step=5000.0)

st.sidebar.subheader("📉 Deudas Principales ('Por Pagar')")
deuda_negro = st.sidebar.number_input("Deuda Negro (Total pendiente)", value=1600000.0, step=50000.0)
cuota_camilo = st.sidebar.number_input("Cuota Camilo / Préstamo mensual", value=1000000.0, step=50000.0)
rapicredid = st.sidebar.number_input("Rapicredid", value=350000.0, step=10000.0)

st.markdown("---")

# SECCIÓN 1: Registrar o Administrar Créditos a Cuotas (Addi / Sistecredito)
st.markdown("### 🛍️ Seguimiento de Créditos a Cuotas (Addi, Sistecredito, etc.)")
st.markdown("Lleva la cuenta exacta de cuántas cuotas has pagado y cuántas te faltan.")

with st.expander("➕ Registrar un nuevo crédito a cuotas o actualizar progreso", expanded=False):
    col_c1, col_c2, col_c3, col_c4 = st.columns([2, 1, 1, 1])
    with col_c1:
        nombre_credito = st.text_input("Nombre (Ej: Addi Totto, Sistecredito...)", placeholder="Tienda o producto")
    with col_c2:
        valor_cuota = st.number_input("Valor de la Cuota (COP)", value=0.0, step=10000.0)
    with col_c3:
        cuotas_tot = st.number_input("Total de Cuotas", value=3, min_value=1, step=1)
    with col_c4:
        cuotas_pag = st.number_input("Cuotas ya Pagadas", value=0, min_value=0, step=1)
    
    if st.button("Guardar Crédito en la Lista"):
        if nombre_credito and valor_cuota > 0:
            st.session_state.creditos_cuotas.append({
                "Crédito / Tienda": nombre_credito,
                "Valor Cuota Mensual": valor_cuota,
                "Cuotas Totales": int(cuotas_tot),
                "Cuotas Pagadas": int(cuotas_pag)
            })
            st.success(f"¡Crédito '{nombre_credito}' agregado exitosamente!")
            st.rerun()

# Procesar tabla de créditos para mostrar cuotas faltantes, porcentaje de avance y deuda restante
if st.session_state.creditos_cuotas:
    datos_tabla_creditos = []
    total_cuotas_mes_actual = 0
    
    for item in st.session_state.creditos_cuotas:
        pendientes = item["Cuotas Totales"] - item["Cuotas Pagadas"]
        deuda_restante = pendientes * item["Valor Cuota Mensual"]
        progreso_pct = int((item["Cuotas Pagadas"] / item["Cuotas Totales"]) * 100)
        
        # Si aún le quedan cuotas, suma al valor que pagas este mes
        if pendientes > 0:
            total_cuotas_mes_actual += item["Valor Cuota Mensual"]
            
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
    
    col_btn_c1, col_btn_c2 = st.columns([1, 4])
    with col_btn_c1:
        if st.button("🗑️ Borrar lista de créditos"):
            st.session_state.creditos_cuotas = []
            st.rerun()
else:
    total_cuotas_mes_actual = 0
    st.info("No hay créditos a cuotas registrados por el momento.")

st.markdown("---")

# SECCIÓN 2: Registrar Otros Gastos Adicionales
st.markdown("### ➕ Registrar Otro Gasto o Imprevisto Extra")
col_add1, col_add2, col_add3 = st.columns([2, 2, 1])

with col_add1:
    nombre_gasto_nuevo = st.text_input("Concepto (Ej: Gasolina, salida...):", placeholder="Nombre del gasto...")
with col_add2:
    valor_gasto_nuevo = st.number_input("Monto (COP):", value=0.0, step=10000.0)
with col_add3:
    st.markdown("<br>", unsafe_allow_html=True)
    agregar_btn = st.button("Añadir a la lista")

if agregar_btn and nombre_gasto_nuevo and valor_gasto_nuevo > 0:
    st.session_state.gastos_extra.append({"Concepto": nombre_gasto_nuevo, "Valor": valor_gasto_nuevo})
    st.success("¡Gasto extra agregado!")

total_gastos_extra = sum(item["Valor"] for item in st.session_state.gastos_extra)

if st.session_state.gastos_extra:
    df_extras = pd.DataFrame(st.session_state.gastos_extra)
    st.dataframe(df_extras, use_container_width=True)
    if st.button("🗑️ Limpiar extras"):
        st.session_state.gastos_extra = []
        st.rerun()

st.markdown("---")

# CÁLCULOS REALES Y ORGANIZADOS
# Salidas de la Quincena 1 actual (Incluye cuotas activas de Addi/Sistecredito correspondientes y gastos extras)
salidas_q1_fijas = gas_quincenal + parqueadero + fondo_emergencia + total_cuotas_mes_actual + total_gastos_extra
saldo_q1_real = saldo_actual_banco - salidas_q1_fijas

# Ingreso de la quincena del día 20 (Neta real)
saldo_tras_nomina = saldo_q1_real + nomina_quincenal_neta

# Salidas de la Quincena 2 (Camilo, Rapicredid y compromisos de fin de mes)
salidas_q2_fijas = cuota_camilo + gas_quincenal + fondo_emergencia + rapicredid
balance_final_mes = saldo_tras_nomina - salidas_q2_fijas

# Tarjetas de Métricas Clave y Reales
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color:#7C3AED;">💳 Saldo Disponible Q1</h4>
        <h2>$ {saldo_q1_real:,.0f} COP</h2>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color:#DB2777;">💰 Tras Nómina Día 20</h4>
        <h2>$ {saldo_tras_nomina:,.0f} COP</h2>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color:#4C1D95;">✨ Balance Final del Mes</h4>
        <h2>$ {balance_final_mes:,.0f} COP</h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Centro de Alertas Inteligentes
st.markdown("### 🚨 Estado Financiero y Alertas 'Por Pagar'")

if saldo_q1_real < 0:
    st.markdown(f"""
    <div class="alert-card-danger">
        ⚠️ <b>Déficit en Quincena 1:</b> Faltan <b>$ {abs(saldo_q1_real):,.0f} COP</b> para cubrir los gastos y cuotas actuales. 
        <br>💡 <i>Se cubrirá automáticamente cuando entre tu quincena neta de $ {nomina_quincenal_neta:,.0f} COP el 20 de septiembre.</i>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="alert-card-success">
        ✅ <b>Quincena 1 al día:</b> Cuentas con un sobrante real de $ {saldo_q1_real:,.0f} COP antes de la próxima nómina.
    </div>
    """, unsafe_allow_html=True)

if balance_final_mes < 0:
    st.markdown(f"""
    <div class="alert-card-danger" style="margin-top: 10px;">
        ⚠️ <b>Alerta de Cierre:</b> El mes cierra con un déficit de <b>$ {abs(balance_final_mes):,.0f} COP</b> debido a las deudas pendientes. Revisa tus gastos con precaución.
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="alert-card-success" style="margin-top: 10px;">
        ✅ <b>Mes Equilibrado:</b> Las obligaciones principales (Camilo, Rapicredid y cuotas) se cubren perfectamente con tu flujo real.
    </div>
    """, unsafe_allow_html=True)

# Tabla Organizada de Obligaciones
st.markdown("### 📊 Resumen Organizado de Obligaciones")

tabla_resumen = [
    {"Categoría": "Deuda Principal Pendiente", "Concepto": "Negro", "Valor Total": deuda_negro, "Estado": "Por Pagar (Aparte)"},
    {"Categoría": "Créditos Activos (Addi/Sistemas)", "Concepto": "Cuotas Activas del Mes", "Valor Total": total_cuotas_mes_actual, "Estado": "En Curso"},
    {"Categoría": "Deuda / Cuota Mensual", "Concepto": "Camilo", "Valor Total": cuota_camilo, "Estado": "Programada Q2"},
    {"Categoría": "Crédito Rápido", "Concepto": "Rapicredid", "Valor Total": rapicredid, "Estado": "Programada Q2"},
    {"Categoría": "Bolsillo Fijo", "Concepto": "Gas (Total Mes)", "Valor Total": gas_mensual, "Estado": "Dividido en Quincenas"},
]

df_resumen = pd.DataFrame(tabla_resumen)
st.dataframe(df_resumen, use_container_width=True)

# Botón de Exportar Reporte
st.markdown("### 📥 Descargar Reporte")
if st.button("📊 Generar Reporte CSV"):
    csv_data = df_resumen.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar archivo CSV",
        data=csv_data,
        file_name=f"finanzas_reales_tatiana_{datetime.date.today()}.csv",
        mime='text/css' if False else 'text/csv',
    )
    st.success("¡Listo para descargar!")
