"""
Alinet Telecom Manager - Módulo de base de datos (Supabase).

Conexión vía supabase-py usando credenciales en st.secrets:

    # .streamlit/secrets.toml
    [supabase]
    url = "https://TU-PROYECTO.supabase.co"
    key = "TU-ANON-KEY"

Uso:
    from database import get_clientes, insert_cliente, update_estado_cliente
"""

from __future__ import annotations

import streamlit as st
from supabase import Client, create_client

TABLA = "clientes"


@st.cache_resource
def get_supabase() -> Client:
    """Crea (una sola vez) el cliente de Supabase a partir de st.secrets."""
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)


def get_clientes() -> list[dict]:
    """Retorna todos los clientes ordenados por nombre."""
    supabase = get_supabase()
    response = (
        supabase.table(TABLA)
        .select("*")
        .order("nombre_completo")
        .execute()
    )
    return response.data or []


def insert_cliente(datos: dict) -> dict:
    """Inserta un nuevo cliente. `datos` debe incluir los campos obligatorios."""
    supabase = get_supabase()
    response = supabase.table(TABLA).insert(datos).execute()
    return response.data[0] if response.data else {}


def update_estado_cliente(cliente_id: str, nuevo_estado: str) -> dict:
    """Cambia el estado de un cliente (Activo / Suspendido / Retirado)."""
    if nuevo_estado not in ("Activo", "Suspendido", "Retirado"):
        raise ValueError(f"Estado no válido: {nuevo_estado}")
    supabase = get_supabase()
    response = (
        supabase.table(TABLA)
        .update({"estado": nuevo_estado})
        .eq("id", cliente_id)
        .execute()
    )
    return response.data[0] if response.data else {}


def delete_cliente(cliente_id: str) -> None:
    """Elimina un cliente por su ID."""
    supabase = get_supabase()
    supabase.table(TABLA).delete().eq("id", cliente_id).execute()
