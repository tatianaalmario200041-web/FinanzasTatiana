import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Tabla Maestra Finanzas Tatis",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        font-size: 13px;
        color: #3E2723;
    }
    
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        max-width: 100% !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }
    
    .main {
        background: linear-gradient(135deg, #F3E5F5 0%, #E1BEE7 50%, #CE93D8 100%);
    }
    
    .header-container {
        text-align: center;
        background: linear-gradient(135deg, #7B1FA2 0%, #8E24AA 50%, #C2185B 100%);
        padding: 15px;
        border-radius: 14px;
        border: 2px solid #F3E5F5;
        box-shadow: 0 4px 15px rgba(123, 31, 162, 0.3);
        margin-bottom: 20px;
    }
    
    .header-title {
        font-weight: 900;
        font-size: 1.8rem;
        color: #FFFFFF;
        margin: 0;
        letter-spacing: 0.5px;
    }

    .card-resumen {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 15px;
        border-radius: 12px;
        border: 1.5px solid #BA68C8;
        text-align: center;
        box-shadow: 0 3px 10px rgba(123, 31, 162, 0.15);
    }
    </style>
""",
    unsafe_allow_html=True,
)


def formato_COP(valor):
  if valor < 0:
    return f"- $ {abs(valor):,.0f}".replace(",", ".")
  return f"$ {valor:,.0f}".replace(",", ".")


# TÍTULO PRINCIPAL
st.markdown(
    """
    <div class="header-container">
        <h1 class="header-title">🌸 Tabla Maestra Definitiva - Finanzas Tatis 🌸</h1>
        <p style="color: #F3E5F5; margin: 5px 0 0 0; font-weight: 600;">Control milimétrico, entradas, salidas y saldo real al instante</p>
    </div>
""",
    unsafe_allow_html=True,
)

# INICIALIZAR MOVIMIENTOS DE LA TABLA MAESTRA
if "movimientos" not in st.session_state:
  st.session_state.movimientos = [
      {
          "id": 1,
          "fecha": "Oct 28 (Hoy)",
          "concepto": "Efectivo en mano actual",
          "tipo": "Disponible",
          "entrada": 100000.0,
          "salida": 0.0,
          "hecho": True,
      },
      {
          "id": 2,
          "fecha": "Oct 30",
          "concepto": "Entrada de efectivo Gerardo",
          "tipo": "Ingreso",
          "entrada": 900000.0,
          "salida": 0.0,
          "hecho": False,
      },
      {
          "id": 3,
          "fecha": "Oct 30",
          "concepto": "Entrada de efectivo Karen",
          "tipo": "Ingreso",
          "entrada": 880000.0,
          "salida": 0.0,
          "hecho": False,
      },
      {
          "id": 4,
          "fecha": "Oct 30",
          "concepto": "Pago neto a Cristian",
          "tipo": "Salida",
          "entrada": 0.0,
          "salida": 308000.0,
          "hecho": False,
      },
      {
          "id": 5,
          "fecha": "Oct 30",
          "concepto": "Saldo pendiente Nicolás (Base)",
          "tipo": "Salida",
          "entrada": 0.0,
          "salida": 60000.0,
          "hecho": False,
      },
      {
          "id": 6,
          "fecha": "Oct 30",
          "concepto": "Addi - Alkosto / Televisor (De Cristian)",
          "tipo": "Deuda",
          "entrada": 0.0,
          "salida": 286000.0,
          "hecho": False,
      },
      {
          "id": 7,
          "fecha": "Oct 30",
          "concepto": "Addi - Totto (Cuota 3 de 5 - Faltan 2)",
          "tipo": "Deuda",
          "entrada": 0.0,
          "salida": 68370.0,
          "hecho": False,
      },
      {
          "id": 8,
          "fecha": "Oct 30",
          "concepto": "Addi - Puntos Colombia (Cuota 8 de 9 - Faltan 2)",
          "tipo": "Deuda",
          "entrada": 0.0,
          "salida": 68370.0,
          "hecho": False,
      },
      {
          "id": 9,
          "fecha": "Oct 31",
          "concepto": "Salario quincenal (Est. aprox.)",
          "tipo": "Ingreso",
          "entrada": 1194000.0,
          "salida": 0.0,
          "hecho": False,
      },
      {
          "id": 10,
          "fecha": "Oct 31",
          "concepto": "Última cuota de Camilo (¡Liquidado!)",
          "tipo": "Logro",
          "entrada": 0.0,
          "salida": 373500.0,
          "hecho": False,
      },
      {
          "id": 11,
          "fecha": "Nov 3",
          "concepto": "1.ª Cuota Martes Nicolás",
          "tipo": "Deuda",
          "entrada": 0.0,
          "salida": 360000.0,
          "hecho": False,
      },
      {
          "id": 12,
          "fecha": "Nov 10",
          "concepto": "2.ª Cuota Martes Nicolás",
          "tipo": "Deuda",
          "entrada": 0.0,
          "salida": 360000.0,
          "hecho": False,
      },
      {
          "id": 13,
          "fecha": "Nov 10",
          "concepto": "Factura del Gas (Completa)",
          "tipo": "Fuerte",
          "entrada": 0.0,
          "salida": 800000.0,
          "hecho": False,
      },
      {
          "id": 14,
          "fecha": "Nov 10",
          "concepto": "Cuota Tarjeta de Crédito (TC)",
          "tipo": "Deuda",
          "entrada": 0.0,
          "salida": 160000.0,
          "hecho": False,
      },
      {
          "id": 15,
          "fecha": "Nov 15",
          "concepto": "Desembolso Préstamo de Nómina (Moderline)",
          "tipo": "Rescate",
          "entrada": 1500000.0,
          "salida": 0.0,
          "hecho": False,
      },
      {
          "id": 16,
          "fecha": "Nov 15",
          "concepto": "Salario Quincenal Regular",
          "tipo": "Ingreso",
          "entrada": 1194000.0,
          "salida": 0.0,
          "hecho": False,
      },
      {
          "id": 17,
          "fecha": "Nov 15",
          "concepto": "Pago total deuda Alexa (¡Paz y Salvo!)",
          "tipo": "Logro",
          "entrada": 0.0,
          "salida": 1000000.0,
          "hecho": False,
      },
      {
          "id": 18,
          "fecha": "Nov 15",
          "concepto": "Sistecredito - Vestido (Cuota final)",
          "tipo": "Deuda",
          "entrada": 0.0,
          "salida": 39413.0,
          "hecho": False,
      },
      {
          "id": 19,
          "fecha": "Nov 15",
          "concepto": "Sistecredito - Sudadera (Cuota final)",
          "tipo": "Deuda",
          "entrada": 0.0,
          "salida": 59599.0,
          "hecho": False,
      },
      {
          "id": 20,
          "fecha": "Nov 15",
          "concepto": "Sistecredito - Maleta Totto (Cuota final)",
          "tipo": "Deuda",
          "entrada": 0.0,
          "salida": 66051.0,
          "hecho": False,
      },
      {
          "id": 21,
          "fecha": "Nov 15",
          "concepto": "Separación 1.ª Cuota Gerardo (Se aparta desde el 15)",
          "tipo": "Reserva",
          "entrada": 0.0,
          "salida": 275000.0,
          "hecho": False,
      },
      {
          "id": 22,
          "fecha": "Nov 17",
          "concepto": "3.ª Cuota Martes Nicolás",
          "tipo": "Deuda",
          "entrada": 0.0,
          "salida": 360000.0,
          "hecho": False,
      },
      {
          "id": 23,
          "fecha": "Nov 24",
          "concepto": "4.ª Cuota Martes Nicolás (Final)",
          "tipo": "Logro",
          "entrada": 0.0,
          "salida": 360000.0,
          "hecho": False,
      },
      {
          "id": 24,
          "fecha": "Nov 25",
          "concepto": "Pago de la 1.ª Cuota Gerardo (Con lo separado el 15)",
          "tipo": "Pagado",
          "entrada": 0.0,
          "salida": 0.0,
          "hecho": False,
      },
      {
          "id": 25,
          "fecha": "Nov 30",
          "concepto": "Salario Quincenal Regular",
          "tipo": "Ingreso",
          "entrada": 1194000.0,
          "salida": 0.0,
          "hecho": False,
      },
      {
          "id": 26,
          "fecha": "Dic 10",
          "concepto": "2.ª Cuota Gerardo",
          "tipo": "Deuda",
          "entrada": 0.0,
          "salida": 275000.0,
          "hecho": False,
      },
      {
          "id": 27,
          "fecha": "Dic 15",
          "concepto": "Salario Quincenal Regular",
          "tipo": "Ingreso",
          "entrada": 1194000.0,
          "salida": 0.0,
          "hecho": False,
      },
      {
          "id": 28,
          "fecha": "Dic 15",
          "concepto": "Separación 3.ª Cuota Gerardo (Se aparta desde el 15)",
          "tipo": "Reserva",
          "entrada": 0.0,
          "salida": 275000.0,
          "hecho": False,
      },
      {
          "id": 29,
          "fecha": "Dic 25",
          "concepto": "3.ª Cuota Gerardo (Con lo separado el 15)",
          "tipo": "Pagado",
          "entrada": 0.0,
          "salida": 0.0,
          "hecho": False,
      },
      {
          "id": 30,
          "fecha": "Dic 30",
          "concepto": "Salario Quincenal Regular",
          "tipo": "Ingreso",
          "entrada": 1194000.0,
          "salida": 0.0,
          "hecho": False,
      },
      {
          "id": 31,
          "fecha": "Ene 10",
          "concepto": "4.ª Cuota Gerardo (Final)",
          "tipo": "Logro",
          "entrada": 0.0,
          "salida": 275000.0,
          "hecho": False,
      },
  ]

# CÁLCULO DINÁMICO DE SALDOS SEGÚN LO QUE ESTÉ CHULEADO ("HECHO")
saldo_acumulado = 0.0
tabla_calculada = []

for mov in st.session_state.movimientos:
  # El saldo solo descuenta o suma si el movimiento ya fue ejecutado/marcado como hecho
  if mov["hecho"]:
    saldo_acumulado += mov["entrada"] - mov["salida"]

  tabla_calculada.append({
      "id": mov["id"],
      "Fecha": mov["fecha"],
      "Concepto": mov["concepto"],
      "Tipo": mov["tipo"],
      "Entrada": mov["entrada"],
      "Salida": mov["salida"],
      "Saldo Restante": saldo_acumulado,
      "Hecho": mov["hecho"],
  })

# MÉTRICA SUPERIOR RÁPIDA
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
  st.markdown(
      f"""
        <div class="card-resumen">
            <h5 style="color:#6A1B9A; margin:0;">💰 Saldo Actual en Caja</h5>
            <h3 style="color:#4A148C; margin:5px 0 0 0;">{formato_COP(saldo_acumulado)}</h3>
        </div>
    """,
      unsafe_allow_html=True,
  )
with col_m2:
  st.markdown(
      """
        <div class="card-resumen">
            <h5 style="color:#7B1FA2; margin:0;">🛡️ Prima de Diciembre</h5>
            <h3 style="color:#8E24AA; margin:5px 0 0 0;">100% Blindada</h3>
        </div>
    """,
      unsafe_allow_html=True,
  )
with col_m3:
  st.markdown(
      """
        <div class="card-resumen">
            <h5 style="color:#AD1457; margin:0;">✨ Estado General</h5>
            <h3 style="color:#D81B60; margin:5px 0 0 0;">Todo en Orden</h3>
        </div>
    """,
      unsafe_allow_html=True,
  )

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    "<h4 style='color: #4A148C; font-weight: 800;'>📋 Tabla Maestra Interactiva"
    " (Marca 'Hecho' a medida que ejecutes cada movimiento)</h4>",
    unsafe_allow_html=True,
)

# RENDERIZAR TABLA INTERACTIVA FILA POR FILA
for i, item in enumerate(tabla_calculada):
  cols = st.columns([1.2, 3.2, 1.3, 1.3, 1.5, 1.0])

  with cols[0]:
    st.markdown(f"**{item['Fecha']}**")
  with cols[1]:
    st.markdown(f"{item['Concepto']}")
  with cols[2]:
    entrada_txt = (
        formato_COP(item["Entrada"]) if item["Entrada"] > 0 else "-"
    )
    st.markdown(
        f"<span style='color: #2E7D32; font-weight:700;'>{entrada_txt}</span>",
        unsafe_allow_html=True,
    )
  with cols[3]:
    salida_txt = formato_COP(item["Salida"]) if item["Salida"] > 0 else "-"
    st.markdown(
        f"<span style='color: #C2185B; font-weight:700;'>{salida_txt}</span>",
        unsafe_allow_html=True,
    )
  with cols[4]:
    st.markdown(
        f"<span style='color: #6A1B9A; font-weight:900;'>"
        f"{formato_COP(item['Saldo Restante'])}</span>",
        unsafe_allow_html=True,
    )
  with cols[5]:
    nuevo_estado = st.checkbox(
        "Hecho", value=item["Hecho"], key=f"check_{item['id']}"
    )
    if nuevo_estado != item["Hecho"]:
      st.session_state.movimientos[i]["hecho"] = nuevo_estado
      st.rerun()

  st.markdown(
      "<hr style='border: 0.5px solid #E1BEE7; margin: 4px 0;'>",
      unsafe_allow_html=True,
  )
