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
st.markdown('<div class="subtitle">Panel con Porcentajes de Avance y Control de Cuotas Reales 🌸💜</div>', unsafe_allow_html=True)

# Memoria de obligaciones con cuotas reales (incluyendo Tarjeta de Crédito a 8 cuotas)
if 'obligaciones' not in st.session_state:
    st.session_state.obligaciones = [
        # Créditos / Préstamos / TC a cuotas
        {"nombre": "Deuda Camilo", "valor": 373500.0, "tipo": "Crédito", "total": 6, "pagadas": 2},
        {"nombre": "Gas", "valor": 390000.0, "tipo": "Servicio Cuotas", "total": 12, "pagadas": 7},
        {"nombre": "Tarjeta de Crédito (TC)", "valor": 160000.0, "tipo": "Crédito TC", "total": 8, "pagadas": 0},
        {"nombre": "Addi Totto", "valor": 15000.0, "tipo": "Crédito", "total": 3, "pagadas": 1},
        {"nombre": "Addi Puntos", "valor": 110000.0, "tipo": "Crédito", "total": 3, "pagadas": 1},
        {"nombre": "Sistecredito Vestido", "valor": 39000.0, "tipo": "Crédito", "total": 4, "pagadas": 2},
        {"nombre": "Sistecredito Sudadera", "valor": 59000.0, "tipo": "Crédito", "total": 4, "pagadas": 2},
        {"nombre": "Sistecredito Maleta", "valor": 66000.0, "tipo": "Crédito", "total": 4, "pagadas": 2},
        
        # Gastos Fijos reales (servicios mensuales recurrentes)
        {"nombre": "Internet Q1", "valor": 55000.0, "tipo": "Fijo", "estado_mes": False},
        {"nombre": "Internet Q2", "valor": 77000.0, "tipo": "Fijo", "estado_mes": False},
        {"nombre": "Parqueadero Q1", "valor": 25000.0, "tipo": "Fijo", "estado_mes": False},
        {"nombre": "Parqueadero Q2", "valor": 25000.0, "tipo": "Fijo", "estado_mes": False},
    ]

# Sidebar de Configuración Real
st.sidebar.header("⚙️ Tus Cuentas y Nómina")
saldo_actual_banco = st.sidebar.number_input("Saldo Actual en Bancolombia (COP)", value=2800000.0, step=100000.0)
nomina_quincenal_neta = st.sidebar.number_input("Pago Neto Quincenal (Desprendible Davivienda)", value=1294007.0, step=10000.0)

st.markdown("---")

# SECCIÓN SUPERIOR: Gráfico y Métricas de Avance Global del Mes
st.markdown("### 📈 Progreso General de Pagos")

total_deuda_global = sum(item["valor"] * item["total"] if "total" in item else item["valor"] for item in st.session_state.obligaciones)
total_pagado_global = sum(item["valor"] * item["pagadas"] if "total" in item else (item["valor"] if item.get("estado_mes", False) else 0) for item in st.session_state.obligaciones)
porcentaje_avance_global = int((total_pagado_global / total_deuda_global) * 100) if total_deuda_global > 0 else 0

col_g1, col_g2, col_g3 = st.columns(3)
with col_g1:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color:#7C3AED; font-size:1rem;">💰 Total Histórico Obligaciones</h4>
        <h3 style="color:#333;">{formato_COP(total_deuda_global)}</h3>
    </div>
    """, unsafe_allow_html=True)
with col_g2:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color:#10B981; font-size:1rem;">✅ Ya Pagado</h4>
        <h3 style="color:#333;">{formato_COP(total_pagado_global)}</h3>
    </div>
    """, unsafe_allow_html=True)
with col_g3:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color:#DB2777; font-size:1rem;">🚀 Avance Global</h4>
        <h3 style="color:#333;">{porcentaje_avance_global}%</h3>
    </div>
    """, unsafe_allow_html=True)

st.progress(porcentaje_avance_global / 100)

st.markdown("---")

# SECCIÓN PRINCIPAL: Control con Chulitos, Porcentaje y Saldo Pendiente
st.markdown("### 🎯 Control de Cuotas y Motivación (¡Mira tu saldo pendiente y % de avance!)")

for idx, item in enumerate(st.session_state.obligaciones):
    col_i1, col_i2, col_i3, col_i4 = st.columns([3, 2, 2, 2])
    
    with col_i1:
        badge_color = "#7C3AED" if "Crédito" in item["tipo"] or "Servicio" in item["tipo"] else "#DB2777"
        valor_str = formato_COP(item['valor'])
        sub_label = f"Cuota: {valor_str}" if "total" in item else f"Valor: {valor_str}"
        st.markdown(f"**{item['nombre']}** <br><span style='color:{badge_color}; font-size:0.85rem; font-weight:bold;'>[{item['tipo']}] - {sub_label}</span>", unsafe_allow_html=True)
    
    with col_i2:
        if "total" in item:
            porcentaje_item = int((item["pagadas"] / item["total"]) * 100)
            saldo_pendiente = item["valor"] * (item["total"] - item["pagadas"])
            st.markdown(f"Progreso: **{item['pagadas']} de {item['total']} ({porcentaje_item}%)**<br><span style='color:#E11D48; font-size:0.85rem;'>Pendiente: {formato_COP(saldo_pendiente)}</span>", unsafe_allow_html=True)
        else:
            estado_txt = "✅ Pagado" if item.get("estado_mes", False) else "⏳ Pendiente"
            saldo_fijo = 0 if item.get("estado_mes", False) else item["valor"]
            st.markdown(f"Estado: **{estado_txt}**<br><span style='color:#E11D48; font-size:0.85rem;'>Pendiente: {formato_COP(saldo_fijo)}</span>", unsafe_allow_html=True)
        
    with col_i3:
        if "total" in item:
            if item["pagadas"] < item["total"]:
                if st.button(f"✅ Pagar Cuota", key=f"pagar_{idx}"):
                    st.session_state.obligaciones[idx]["pagadas"] += 1
                    st.rerun()
            else:
                st.markdown("🎉 **¡Completado!**")
        else:
            if not item.get("estado_mes", False):
                if st.button(f"✅ Marcar Pagado", key=f"pagar_fijo_{idx}"):
                    st.session_state.obligaciones[idx]["estado_mes"] = True
                    st.rerun()
            else:
                st.markdown("✔️ **¡Pagado!**")
                
    with col_i4:
        if "total" in item:
            if item["pagadas"] > 0:
                if st.button(f"↩️ Deshacer", key=f"deshacer_{idx}"):
                    st.session_state.obligaciones[idx]["pagadas"] -= 1
                    st.rerun()
        else:
            if item.get("estado_mes", False):
                if st.button(f"↩️ Deshacer", key=f"deshacer_fijo_{idx}"):
                    st.session_state.obligaciones[idx]["estado_mes"] = False
                    st.rerun()
