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
st.markdown('<div class="subtitle">Panel Libre de Deudas Pesadas & Control Total con Chulitos 🌸💜</div>', unsafe_allow_html=True)

# Memoria de obligaciones mensuales y créditos
if 'obligaciones' not in st.session_state:
    st.session_state.obligaciones = [
        # Créditos a cuotas
        {"nombre": "Addi Totto", "valor": 15000.0, "tipo": "Crédito", "total": 3, "pagadas": 1, "estado_mes": False},
        {"nombre": "Addi Puntos", "valor": 110000.0, "tipo": "Crédito", "total": 3, "pagadas": 1, "estado_mes": False},
        {"nombre": "Sistecredito Vestido", "valor": 39000.0, "tipo": "Crédito", "total": 4, "pagadas": 2, "estado_mes": False},
        {"nombre": "Sistecredito Sudadera", "valor": 59000.0, "tipo": "Crédito", "total": 4, "pagadas": 2, "estado_mes": False},
        {"nombre": "Sistecredito Maleta", "valor": 66000.0, "tipo": "Crédito", "total": 4, "pagadas": 2, "estado_mes": False},
        # Gastos Fijos / Servicios / Quincenales
        {"nombre": "Cuota Camilo (Q1)", "valor": 373500.0, "tipo": "Fijo", "estado_mes": False},
        {"nombre": "Cuota Camilo (Q2)", "valor": 373500.0, "tipo": "Fijo", "estado_mes": False},
        {"nombre": "Gas Quincenal (Parte 1)", "valor": 390000.0, "tipo": "Servicio", "estado_mes": False},
        {"nombre": "Gas Quincenal (Parte 2)", "valor": 390000.0, "tipo": "Servicio", "estado_mes": False},
        {"nombre": "Tarjeta de Crédito / TC (Q1)", "valor": 160000.0, "tipo": "Fijo", "estado_mes": False},
        {"nombre": "Tarjeta de Crédito / TC (Q2)", "valor": 160000.0, "tipo": "Fijo", "estado_mes": False},
        {"nombre": "Internet Q1", "valor": 55000.0, "tipo": "Servicio", "estado_mes": False},
        {"nombre": "Internet Q2", "valor": 77000.0, "tipo": "Servicio", "estado_mes": False},
        {"nombre": "Parqueadero Q1", "valor": 25000.0, "tipo": "Fijo", "estado_mes": False},
        {"nombre": "Parqueadero Q2", "valor": 25000.0, "tipo": "Fijo", "estado_mes": False},
    ]

# Sidebar de Configuración Real
st.sidebar.header("⚙️ Tus Cuentas y Nómina")
saldo_actual_banco = st.sidebar.number_input("Saldo Actual en Bancolombia (COP)", value=2800000.0, step=100000.0)
nomina_quincenal_neta = st.sidebar.number_input("Pago Neto Quincenal (Desprendible Davivienda)", value=1294007.0, step=10000.0)

st.markdown("---")

# SECCIÓN SUPERIOR: Gráfico y Métricas de Avance Global del Mes
st.markdown("### 📈 Progreso General de Pagos del Mes")

total_obligaciones_mes = sum(item["valor"] for item in st.session_state.obligaciones)
total_pagado_mes = sum(item["valor"] for item in st.session_state.obligaciones if item["estado_mes"] == True)
porcentaje_avance_mes = int((total_pagado_mes / total_obligaciones_mes) * 100) if total_obligaciones_mes > 0 else 0

col_g1, col_g2, col_g3 = st.columns(3)
with col_g1:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color:#7C3AED; font-size:1rem;">💰 Total Obligaciones</h4>
        <h3 style="color:#333;">{formato_COP(total_obligaciones_mes)}</h3>
    </div>
    """, unsafe_allow_html=True)
with col_g2:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color:#10B981; font-size:1rem;">✅ Ya Pagado</h4>
        <h3 style="color:#333;">{formato_COP(total_pagado_mes)}</h3>
    </div>
    """, unsafe_allow_html=True)
with col_g3:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color:#DB2777; font-size:1rem;">🚀 Avance del Mes</h4>
        <h3 style="color:#333;">{porcentaje_avance_mes}%</h3>
    </div>
    """, unsafe_allow_html=True)

st.progress(porcentaje_avance_mes / 100)

st.markdown("---")

# SECCIÓN PRINCIPAL: Control con Chulitos para Todo
st.markdown("### 🎯 Control Total de Pagos (¡Marca con tu chulito lo que vayas pagando!)")
st.write("Aquí tienes todas tus obligaciones del mes (gas, tarjeta de crédito, créditos a cuotas, servicios y Camilo) para marcar en tiempo real:")

for idx, item in enumerate(st.session_state.obligaciones):
    col_i1, col_i2, col_i3, col_i4 = st.columns([3, 2, 2, 2])
    
    with col_i1:
        badge_color = "#7C3AED" if item["tipo"] == "Crédito" else ("#DB2777" if item["tipo"] == "Fijo" else "#059669")
        st.markdown(f"**{item['nombre']}** <br><span style='color:{badge_color}; font-size:0.85rem; font-weight:bold;'>[{item['tipo']}] - {formato_COP(item['valor'])}</span>", unsafe_allow_html=True)
    
    with col_i2:
        if item["tipo"] == "Crédito":
            st.markdown(f"Cuota: **{item['pagadas']} de {item['total']}**")
        else:
            estado_txt = "✅ Pagado" if item["estado_mes"] else "⏳ Pendiente"
            st.markdown(f"Estado: **{estado_txt}**")
        
    with col_i3:
        if not item["estado_mes"]:
            if st.button(f"✅ Marcar Pagado", key=f"pagar_{idx}"):
                st.session_state.obligaciones[idx]["estado_mes"] = True
                if item["tipo"] == "Crédito" and item["pagadas"] < item["total"]:
                    st.session_state.obligaciones[idx]["pagadas"] += 1
                st.rerun()
        else:
            st.markdown("✔️ **¡Pagado!**")
                
    with col_i4:
        if item["estado_mes"]:
            if st.button(f"↩️ Deshacer", key=f"deshacer_{idx}"):
                st.session_state.obligaciones[idx]["estado_mes"] = False
                if item["tipo"] == "Crédito" and item["pagadas"] > 0:
                    st.session_state.obligaciones[idx]["pagadas"] -= 1
                st.rerun()
