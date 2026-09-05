import streamlit as st
from database import (
    init_db,
    numero_disponible,
    guardar_participante,
    validar_token,
    usar_token
)
from boleto import generar_boleto
from pathlib import Path
import base64


# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="Rifa en Apoyo al señor Oswaldo Martinez",
    page_icon="🎟️"
)


# ==========================================
# ESTILO
# ==========================================

st.markdown(
    """
    <style>
    h1, h2, h3, p, label {
        color: white !important;
        text-shadow: 2px 2px 4px black;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# BASE DE DATOS
# ==========================================

init_db()


# ==========================================
# FONDO
# ==========================================

def poner_fondo(imagen):

    with open(imagen, "rb") as archivo:
        datos = base64.b64encode(
            archivo.read()
        ).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image:
            url("data:image/jpeg;base64,{datos}");

            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


poner_fondo("logo.jpg")


# ==========================================
# OBTENER TOKEN DE LA URL
# ==========================================

params = st.query_params

token = params.get("token")


# ==========================================
# VALIDACIÓN DEL TOKEN
# ==========================================

if not token:

    st.error(
        "❌ No se encontró un token válido."
    )

    st.stop()


if not validar_token(token):

    st.error(
        "❌ Este enlace ya fue utilizado "
        "o no es válido."
    )

    st.stop()


# ==========================================
# PÁGINA PRINCIPAL
# ==========================================

st.title(
    "🎟️ Rifa en Apoyo al Señor Oswaldo Martinez"
)

st.write(
    "Selecciona un número disponible."
)


# ==========================================
# NÚMEROS
# ==========================================

for inicio in range(0, 100, 10):

    cols = st.columns(10)

    for i, col in enumerate(cols):

        numero = inicio + i
        texto = f"{numero:02d}"

        with col:

            if numero_disponible(numero):

                if st.button(
                    texto,
                    key=f"num_{numero}",
                    use_container_width=True
                ):

                    st.session_state["numero"] = numero

                    st.rerun()

            else:

                st.button(
                    texto,
                    key=f"ocupado_{numero}",
                    disabled=True,
                    use_container_width=True
                )


st.divider()


numero = st.session_state.get("numero")


# ==========================================
# REGISTRO
# ==========================================

if numero is not None:

    st.subheader(
        f"Número seleccionado: {numero:02d}"
    )

    with st.form("registro"):

        nombre = st.text_input(
            "Nombre completo *"
        )

        telefono = st.text_input(
            "Número de teléfono *"
        )

        correo = st.text_input(
            "Correo electrónico *"
        )

        emergencia = st.text_input(
            "Número de emergencia *"
        )

        enviar = st.form_submit_button(
            "🎟️ Registrar y generar boleto"
        )


    # ======================================
    # PROCESAR REGISTRO
    # ======================================

    if enviar:

        campos = [
            nombre,
            telefono,
            correo,
            emergencia
        ]


        # ------------------------------
        # VALIDAR CAMPOS
        # ------------------------------

        if not all(
            campo.strip()
            for campo in campos
        ):

            st.error(
                "Completa todos los campos."
            )


        # ------------------------------
        # COMPROBAR NÚMERO
        # ------------------------------

        elif not numero_disponible(numero):

            st.error(
                "Ese número ya fue ocupado. "
                "Selecciona otro."
            )

            st.session_state.pop(
                "numero",
                None
            )

            st.rerun()


        else:

            # --------------------------
            # GUARDAR PARTICIPANTE
            # --------------------------

            guardar_participante(
                numero,
                nombre.strip(),
                telefono.strip(),
                correo.strip(),
                emergencia.strip()
            )


            # --------------------------
            # MARCAR TOKEN COMO USADO
            # --------------------------

            token_usado = usar_token(token)


            if not token_usado:

                st.error(
                    "Este enlace ya fue utilizado."
                )

                st.stop()


            # --------------------------
            # GENERAR BOLETO
            # --------------------------

            pdf = generar_boleto(
                f"{numero:02d}",
                nombre.strip()
            )


            # --------------------------
            # RESULTADO
            # --------------------------

            st.success(
                "¡Registro realizado correctamente!"
            )


            st.download_button(
                "📄 Descargar boleto PDF",

                data=Path(pdf).read_bytes(),

                file_name=f"boleto_{numero:02d}.pdf",

                mime="application/pdf"
            )


            st.info(
                "Gracias a tu apoyo una persona "
                "tiene una segunda oportunidad."
            )


else:

    st.info(
        "Selecciona un número para comenzar."
    )