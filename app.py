import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Tabla Maestra Finanzas Tatis Pro",
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
        font-size: 15px; /* Letras más grandes y legibles */
        color: #3E2723;
    }
    
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        max-width: 96% !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }
    
    .main {
        background: linear-gradient(135deg, #F3E5F5 0%, #E1BEE7 50%, #CE93D8 100%);
    }
    
    .header-container {
        text-align: center;
        background: linear-gradient(135deg, #7B1FA2 0%, #8E24AA 50%, #C2185B 100%);
        padding: 18px;
        border-radius: 16px;
        border: 2px solid #F3E5F5;
        box-shadow: 0 6px 20px rgba(123, 31, 162, 0.35);
        margin-bottom: 20px;
    }
    
    .header-title {
        font-weight: 900;
        font-size: 2.2rem;
        color: #FFFFFF;
        margin: 0;
    }

    .card-resumen {
        background-color: rgba(255, 255, 255, 0.96);
        padding: 18px;
        border-radius: 14px;
        border: 2px solid #BA68C8;
        text-align: center;
        box-shadow: 0 4px 12px rgba(123, 31, 162, 0.15);
    }
    
    .tabla-header {
        font-weight: 800;
        color: #4A148C;
        font-size: 16px;
        text-transform: uppercase;
        padding-bottom: 8px;
        border-bottom: 2.5px solid #BA68C8;
        margin-bottom: 12px;
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
        <p style="color: #F3E5F5; margin: 6px 0 0 0; font-weight: 700; font-size: 1.1rem;">Control milimétrico, entradas, salidas y saldo real al instante</p>
    </div>
""",
    unsafe_allow_html=True,
)

# INICIALIZAR MOVIMIENTOS EN SESSION STATE
if "movimientos" not in st.session_state:
  st.session_state.movimientos = [
      {
          "id": 1,
          "fecha": "Oct 28",
          "quincena": "Oct 30 (Cierre Mes)",
          "concepto": "Efectivo en mano actual",
          "tipo": "Disponible",
          "entrada": 100000.0,
          "salida": 0.0,
          "hecho": True,
      },
      {
          "id": 2,
          "fecha": "Oct 30",
          "quincena": "Oct 30 (Cierre Mes)",
          "concepto": "Entrada de efectivo Gerardo",
          "tipo": "Ingreso",
          "entrada": 900000.0,
          "salida": 0.0,
          "hecho": False,
      },
      {
          "id": 3,
          "fecha": "Oct 30",
          "quincena": "Oct 30 (Cierre Mes)",
          "concepto": "Entrada de efectivo Karen",
          "tipo": "Ingreso",
          "entrada": 880000.0,
          "salida": 0.0,
          "hecho": False,
      },
      {
          "id": 4,
          "fecha": "Oct 30",
          "quincena": "Oct 30 (Cierre Mes)",
          "concepto": "Pago neto a Cristian",
          "tipo": "Salida",
          "entrada": 0.0,
          "salida": 308000.0,
          "hecho": False,
      },
      {
          "id": 5,
          "fecha": "Oct 30",
          "quincena": "Oct 30 (Cierre Mes)",
          "concepto": "Saldo pendiente Nicolás (Base)",
          "tipo": "Salida",
          "entrada": 0.0,
          "salida": 60000.0,
          "hecho": False,
      },
      {
          "id": 6,
          "fecha": "Oct 30",
          "quincena": "Oct 30 (Cierre Mes)",
          "concepto": "Addi - Alkosto / Televisor (De Cristian)",
          "tipo": "Deuda",
          "entrada": 0.0,
          "salida": 286000.0,
          "hecho": False,
      },
      {
          "id": 7,
          "fecha": "Oct 30",
          "quincena": "Oct 30 (Cierre Mes)",
          "concepto": "Addi - Totto (Cuota 3 de 5 - Faltan 2)",
          "tipo": "Deuda",
          "entrada": 0.0,
          "salida": 68370.0,
          "hecho": False,
      },
      {
          "id": 8,
          "fecha": "Oct 30",
          "quincena": "Oct 30 (Cierre Mes)",
          "concepto": "Addi - Puntos Colombia (Cuota 8 de 9 - Faltan 2)",
          "tipo": "Deuda",
          "entrada": 0.0,
          "salida": 68370.0,
          "hecho": False,
      },
      {
          "id": 9,
          "fecha": "Oct 31",
          "quincena": "Oct 30 (Cierre Mes)",
          "concepto": "Salario quincenal (Est. aprox.)",
          "tipo": "Ingreso",
          "entrada": 1194000.0,
          "salida": 0.0,
          "hecho": False,
      },
      {
          "id": 10,
          "fecha": "Oct 31",
          "quincena": "Oct 30 (Cierre Mes)",
          "concepto": "Última cuota de Camilo (¡Liquidado!)",
          "tipo": "Logro",
          "entrada": 0.0,
          "salida": 373500.0,
          "hecho": False,
      },
      {
          "id": 11,
          "fecha": "Nov 3",
          "quincena": "Noviembre (Martes Nicolás)",
          "tipo": "Deuda",
          "entrada": 0.0,
          "salida": 360000.0,
          "hecho": False,
          "concepto": "1.ª Cuota Martes Nicolás",
      },
      {
          "id": 12,
          "fecha": "Nov 10",
          "quincena": "Noviembre (Martes Nicolás)",
          "tipo": "Deuda",
          "entrada": 0.0,
          "salida": 360000.0,
          "hecho": False,
          "concepto": "2.ª Cuota Martes Nicolás",
      },
      {
          "id": 13,
          "fecha": "Nov 10",
          "quincena": "Noviembre (Mitad/Gas)",
          "tipo": "Fuerte",
          "entrada": 0.0,
          "salida": 800000.0,
          "hecho": False,
          "concepto": "Factura del Gas (Completa)",
      },
      {
          "id": 14,
          "fecha": "Nov 10",
          "quincena": "Noviembre (Mitad/Gas)",
          "tipo": "Deuda",
          "entrada": 0.0,
          "salida": 160000.0,
          "hecho": False,
          "concepto": "Cuota Tarjeta de Crédito (TC)",
      },
      {
          "id": 15,
          "fecha": "Nov 15",
          "quincena": "Noviembre 15 (Quincena Fuerte)",
          "tipo": "Rescate",
          "entrada": 1500000.0,
          "salida": 0.0,
          "hecho": False,
          "concepto": "Desembolso Préstamo de Nómina (Moderline)",
      },
      {
          "id": 16,
          "fecha": "Nov 15",
          "quincena": "Noviembre 15 (Quincena Fuerte)",
          "tipo": "Ingreso",
          "entrada": 1194000.0,
          "salida": 0.0,
          "hecho": False,
          "concepto": "Salario Quincenal Regular",
      },
      {
          "id": 17,
          "fecha": "Nov 15",
          "quincena": "Noviembre 15 (Quincena Fuerte)",
          "tipo": "Logro",
          "entrada": 0.0,
          "salida": 1000000.0,
          "hecho": False,
          "concepto": "Pago total deuda Alexa (¡Paz y Salvo!)",
      },
      {
          "id": 18,
          "fecha": "Nov 15",
          "quincena": "Noviembre 15 (Quincena Fuerte)",
          "tipo": "Deuda",
          "entrada": 0.0,
          "salida": 39413.0,
          "hecho": False,
          "concepto": "Sistecredito - Vestido (Cuota final)",
      },
      {
          "id": 19,
          "fecha": "Nov 15",
          "quincena": "Noviembre 15 (Quincena Fuerte)",
          "tipo": "Deuda",
          "entrada": 0.0,
          "salida": 59599.0,
          "hecho": False,
          "concepto": "Sistecredito - Sudadera (Cuota final)",
      },
      {
          "id": 20,
          "fecha": "Nov 15",
          "quincena": "Noviembre 15 (Quincena Fuerte)",
          "tipo": "Deuda",
          "entrada": 0.0,
          "salida": 66051.0,
          "hecho": False,
          "concepto": "Sistecredito - Maleta Totto (Cuota final)",
      },
      {
          "id": 21,
          "fecha": "Nov 15",
          "quincena": "Noviembre 15 (Quincena Fuerte)",
          "tipo": "Reserva",
          "entrada": 0.0,
          "salida": 275000.0,
          "hecho": False,
          "concepto": "Separación 1.ª Cuota Gerardo (Se aparta desde el 15)",
      },
      {
          "id": 22,
          "fecha": "Nov 17",
          "quincena": "Noviembre (Martes Nicolás)",
          "tipo": "Deuda",
          "entrada": 0.0,
          "salida": 360000.0,
          "hecho": False,
          "concepto": "3.ª Cuota Martes Nicolás",
      },
      {
          "id": 23,
          "fecha": "Nov 24",
          "quincena": "Noviembre (Martes Nicolás)",
          "tipo": "Logro",
          "entrada": 0.0,
          "salida": 360000.0,
          "hecho": False,
          "concepto": "4.ª Cuota Martes Nicolás (Final)",
      },
      {
          "id": 24,
          "fecha": "Nov 25",
          "quincena": "Noviembre 30 (Fin de Mes)",
          "tipo": "Pagado",
          "entrada": 0.0,
          "salida": 0.0,
          "hecho": False,
          "concepto": "Pago de la 1.ª Cuota Gerardo (Con lo separado el 15)",
      },
      {
          "id": 25,
          "fecha": "Nov 30",
          "quincena": "Noviembre 30 (Fin de Mes)",
          "tipo": "Ingreso",
          "entrada": 1194000.0,
          "salida": 0.0,
          "hecho": False,
          "concepto": "Salario Quincenal Regular",
      },
      {
          "id": 26,
          "fecha": "Dic 10",
          "quincena": "Diciembre",
          "tipo": "Deuda",
          "entrada": 0.0,
          "salida": 275000.0,
          "hecho": False,
          "concepto": "2.ª Cuota Gerardo",
      },
      {
          "id": 27,
          "fecha": "Dic 15",
          "quincena": "Diciembre",
          "tipo": "Ingreso",
          "entrada": 1194000.0,
          "salida": 0.0,
          "hecho": False,
          "concepto": "Salario Quincenal Regular",
      },
      {
          "id": 28,
          "fecha": "Dic 15",
          "quincena": "Diciembre",
          "tipo": "Reserva",
          "entrada": 0.0,
          "salida": 275000.0,
          "hecho": False,
          "concepto": "Separación 3.ª Cuota Gerardo (Se aparta desde el 15)",
      },
      {
          "id": 29,
          "fecha": "Dic 25",
          "quincena": "Diciembre",
          "tipo": "Pagado",
          "entrada": 0.0,
          "salida": 0.0,
          "hecho": False,
          "concepto": "3.ª Cuota Gerardo (Con lo separado el 15)",
      },
      {
          "id": 30,
          "fecha": "Dic 30",
          "quincena": "Diciembre",
          "tipo": "Ingreso",
          "entrada": 1194000.0,
          "salida": 0.0,
          "hecho": False,
          "concepto": "Salario Quincenal Regular",
      },
      {
          "id": 31,
          "fecha": "Ene 10",
          "quincena": "Diciembre",
          "tipo": "Logro",
          "entrada": 0.0,
          "salida": 275000.0,
          "hecho": False,
          "concepto": "4.ª Cuota Gerardo (Final)",
      },
  ]

# CÁLCULO DINÁMICO DE SALDOS Y TOTALES DE ADDI / SISTECREDITO
saldo_acumulado = 0.0
tabla_calculada = []
total_addi_pendiente = 68370.0 + 68370.0 + 286000.0  # Totto + Puntos + Alkosto
total_sistecredito_pendiente = 39413.0 + 59599.0 + 66051.0  # Vestido + Sudadera + Maleta

for mov in st.session_state.movimientos:
  if mov["hecho"]:
    saldo_acumulado += mov["entrada"] - mov["salida"]

  tabla_calculada.append({
      "id": mov["id"],
      "Fecha": mov["fecha"],
      "Quincena": mov["quincena"],
      "Concepto": mov["concepto"],
      "Tipo": mov["tipo"],
      "Entrada": mov["entrada"],
      "Salida": mov["salida"],
      "Saldo Restante": saldo_acumulado,
      "Hecho": mov["hecho"],
  })

# -------------------------------------------------------------
# MÉTRICAS SUPERIORES (SALDO EN CAJA, ADDI Y SISTECREDITO)
# -------------------------------------------------------------
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
  st.markdown(
      f"""
        <div class="card-resumen">
            <h4 style="color:#6A1B9A; margin:0; font-size: 1.1rem;">💰 Saldo Actual en Caja</h4>
            <h2 style="color:#4A148C; margin:8px 0 0 0; font-size: 1.8rem; font-weight: 900;">{formato_COP(saldo_acumulado)}</h2>
        </div>
    """,
      unsafe_allow_html=True,
  )
with col_m2:
  st.markdown(
      f"""
        <div class="card-resumen">
            <h4 style="color:#7B1FA2; margin:0; font-size: 1.1rem;">💳 Total Pendiente Addi</h4>
            <h2 style="color:#8E24AA; margin:8px 0 0 0; font-size: 1.8rem; font-weight: 900;">{formato_COP(total_addi_pendiente)}</h2>
        </div>
    """,
      unsafe_allow_html=True,
  )
with col_m3:
  st.markdown(
      f"""
        <div class="card-resumen">
            <h4 style="color:#AD1457; margin:0; font-size: 1.1rem;">🛍️ Total Sistecredito</h4>
            <h2 style="color:#C2185B; margin:8px 0 0 0; font-size: 1.8rem; font-weight: 900;">{formato_COP(total_sistecredito_pendiente)}</h2>
        </div>
    """,
      unsafe_allow_html=True,
  )

st.markdown("<br>", unsafe_allow_html=True)

# FILTRO POR QUINCENA / BLOQUE
st.markdown(
    "<h4 style='color: #4A148C; font-weight: 800;'>🔍 Filtrar Vista por Bloque"
    " / Quincena</h4>",
    unsafe_allow_html=True,
)
opciones_quincenas = ["Todas las Fechas (Mes Completo)"] + list(
    pd.DataFrame(tabla_calculada)["Quincena"].unique()
)
filtro_quincena = st.selectbox("", opciones_quincenas, label_visibility="collapsed")

if filtro_quincena != "Todas las Fechas (Mes Completo)":
  tabla_filtrada = [
      item for item in tabla_calculada if item["Quincena"] == filtro_quincena
  ]
else:
  tabla_filtrada = tabla_calculada

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='color: #4A148C; font-weight: 900; margin-bottom: 15px;'>📋 Tabla"
    " Maestra Interactiva (Puedes editar los valores directamente)</h3>",
    unsafe_allow_html=True,
)

# ENCABEZADOS DE LA TABLA
h_cols = st.columns([1.1, 3.2, 1.4, 1.4, 1.5, 0.9])
with h_cols[0]:
  st.markdown("<div class='tabla-header'>Fecha</div>", unsafe_allow_html=True)
with h_cols[1]:
  st.markdown(
      "<div class='tabla-header'>Concepto del Movimiento</div>",
      unsafe_allow_html=True,
  )
with h_cols[2]:
  st.markdown("<div class='tabla-header'>Entrada</div>", unsafe_allow_html=True)
with h_cols[3]:
  st.markdown("<div class='tabla-header'>Salida</div>", unsafe_allow_html=True)
with h_cols[4]:
  st.markdown(
      "<div class='tabla-header'>Saldo Restante</div>", unsafe_allow_html=True,
  )
with h_cols[5]:
  st.markdown("<div class='tabla-header'>Acción</div>", unsafe_allow_html=True)

# RENDERIZAR FILAS CON EDICIÓN DE VALORES Y CHECKBOX AUTOMÁTICO
for item in tabla_filtrada:
  # Encontrar el índice real en st.session_state.movimientos
  real_idx = next(
      i
      for i, m in enumerate(st.session_state.movimientos)
      if m["id"] == item["id"]
  )

  cols = st.columns([1.1, 3.2, 1.4, 1.4, 1.5, 0.9])

  with cols[0]:
    st.markdown(
        f"<div style='padding: 10px 0; font-weight: 700; font-size: 15px;'>{item['Fecha']}</div>",
        unsafe_allow_html=True,
    )
  with cols[1]:
    st.markdown(
        f"<div style='padding: 10px 0; font-weight: 600; font-size: 15px;'>{item['Concepto']}</div>",
        unsafe_allow_html=True,
    )
  with cols[2]:
    # Permitir editar la entrada si es un valor editable
    nueva_entrada = st.number_input(
        f"Entrada_{item['id']}",
        value=float(item["Entrada"]),
        step=10000.0,
        label_visibility="collapsed",
        key=f"ent_{item['id']}",
    )
    if nueva_entrada != item["Entrada"]:
      st.session_state.movimientos[real_idx]["entrada"] = nueva_entrada
      st.rerun()

  with cols[3]:
    # Permitir editar la salida si es un valor editable
    nueva_salida = st.number_input(
        f"Salida_{item['id']}",
        value=float(item["Salida"]),
        step=10000.0,
        label_visibility="collapsed",
        key=f"sal_{item['id']}",
    )
    if nueva_salida != item["Salida"]:
      st.session_state.movimientos[real_idx]["salida"] = nueva_salida
      st.rerun()

  with cols[4]:
    st.markdown(
        f"<div style='padding: 10px 0; color: #6A1B9A; font-weight: 900; font-size: 16px;'>{formato_COP(item['Saldo Restante'])}</div>",
        unsafe_allow_html=True,
    )

  with cols[5]:
    nuevo_estado = st.checkbox(
        "Hecho", value=item["Hecho"], key=f"chk_{item['id']}"
    )
    if nuevo_estado != item["Hecho"]:
      st.session_state.movimientos[real_idx]["hecho"] = nuevo_estado
      st.rerun()

  st.markdown(
      "<hr style='border: 0.8px solid #D1C4E9; margin: 4px 0;'>",
      unsafe_allow_html=True,
  )
