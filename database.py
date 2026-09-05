import streamlit as st
from supabase import create_client, Client


# ==========================================
# CONEXIÓN CON SUPABASE
# ==========================================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# ==========================================
# INICIALIZAR
# ==========================================

def init_db():
    # Las tablas ya existen en Supabase
    pass


# ==========================================
# NÚMEROS
# ==========================================

def numero_disponible(numero):

    respuesta = (
        supabase
        .table("participantes")
        .select("id")
        .eq("numero", numero)
        .execute()
    )

    return len(respuesta.data) == 0


def guardar_participante(
    numero,
    nombre,
    telefono,
    correo,
    emergencia
):

    datos = {
        "numero": numero,
        "nombre": nombre,
        "telefono": telefono,
        "correo": correo,
        "emergencia": emergencia
    }

    respuesta = (
        supabase
        .table("participantes")
        .insert(datos)
        .execute()
    )

    return respuesta.data


# ==========================================
# TOKENS
# ==========================================

def validar_token(token):

    respuesta = (
        supabase
        .table("tokens")
        .select("*")
        .eq("token", token)
        .eq("usado", False)
        .execute()
    )

    if respuesta.data:
        return True

    return False


def usar_token(token):

    respuesta = (
        supabase
        .table("tokens")
        .update({"usado": True})
        .eq("token", token)
        .eq("usado", False)
        .execute()
    )

    return bool(respuesta.data)