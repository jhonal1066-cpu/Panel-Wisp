"""
Alinet Telecom Manager - Interfaz de gestión de clientes (Streamlit).

Ejecutar con:
    streamlit run clientes_ui.py
"""

import pandas as pd
import streamlit as st

from database import get_clientes, insert_cliente, update_estado_cliente

PLANES = ["3Mbps", "5Mbps", "10Mbps", "20Mbps", "50Mbps"]
ESTADOS = ["Activo", "Suspendido", "Retirado"]

st.set_page_config(page_title="Alinet Telecom - Clientes", page_icon="📡", layout="wide")
st.title("📡 Alinet Telecom Manager — Suscriptores")

tab_directorio, tab_nuevo = st.tabs(["📋 Directorio", "➕ Nuevo Registro"])

# ---------------------------------------------------------------
# Pestaña 1: Directorio
# ---------------------------------------------------------------
with tab_directorio:
    st.subheader("Directorio de clientes")

    if st.button("🔄 Actualizar lista"):
        st.rerun()

    try:
        clientes = get_clientes()
    except Exception as e:
        st.error(f"No se pudo cargar la lista de clientes: {e}")
        clientes = []

    if not clientes:
        st.info("Aún no hay clientes registrados.")
    else:
        df = pd.DataFrame(clientes)
        columnas = [
            "nombre_completo", "cedula_identidad", "telefono", "direccion",
            "ip_asignada", "mac_cpe", "plan_contratado", "estado",
            "fecha_instalacion",
        ]
        df = df[[c for c in columnas if c in df.columns]]
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Cambio rápido de estado (útil para suspensión por falta de pago)
        st.divider()
        st.subheader("Cambiar estado de un cliente")
        opciones = {f"{c['nombre_completo']} ({c['cedula_identidad']})": c["id"] for c in clientes}
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            seleccion = st.selectbox("Cliente", list(opciones.keys()))
        with col2:
            nuevo_estado = st.selectbox("Nuevo estado", ESTADOS)
        with col3:
            st.write("")  # alineación vertical
            st.write("")
            if st.button("Aplicar", type="primary"):
                try:
                    update_estado_cliente(opciones[seleccion], nuevo_estado)
                    st.success(f"Estado actualizado a «{nuevo_estado}».")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al actualizar: {e}")

# ---------------------------------------------------------------
# Pestaña 2: Nuevo Registro
# ---------------------------------------------------------------
with tab_nuevo:
    st.subheader("Registrar nuevo suscriptor")

    with st.form("form_nuevo_cliente", clear_on_submit=True):
        st.markdown("**Datos personales**")
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre completo *")
            cedula = st.text_input("Cédula de identidad *")
        with col2:
            telefono = st.text_input("Teléfono *")
            direccion = st.text_area("Dirección *", height=68)

        st.markdown("**Datos técnicos**")
        col3, col4 = st.columns(2)
        with col3:
            ip = st.text_input("IP asignada *", placeholder="Ej: 10.10.5.23")
            mac = st.text_input("MAC del CPE *", placeholder="Ej: AA:BB:CC:11:22:33")
        with col4:
            plan = st.selectbox("Plan contratado *", PLANES)
            fecha = st.date_input("Fecha de instalación")

        guardar = st.form_submit_button("💾 Guardar cliente", type="primary")

    if guardar:
        if not all([nombre.strip(), cedula.strip(), telefono.strip(),
                    direccion.strip(), ip.strip(), mac.strip()]):
            st.warning("Completa todos los campos obligatorios (*).")
        else:
            datos = {
                "nombre_completo": nombre.strip(),
                "cedula_identidad": cedula.strip(),
                "direccion": direccion.strip(),
                "telefono": telefono.strip(),
                "ip_asignada": ip.strip(),
                "mac_cpe": mac.strip(),
                "plan_contratado": plan,
                "estado": "Activo",
                "fecha_instalacion": str(fecha),
            }
            try:
                insert_cliente(datos)
                st.success(f"✅ Cliente «{nombre}» registrado correctamente.")
            except Exception as e:
                st.error(f"No se pudo guardar el cliente: {e}")
