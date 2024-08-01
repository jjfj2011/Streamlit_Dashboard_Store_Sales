import streamlit as st
import pandas as pd
import plotly.express as px
import dashboard as dash
import detalle as detal


st.set_page_config(layout = 'wide')


def pagina_principal():
    st.markdown(
        """
        <style>
        .centered {
            display: flex;
            justify-content: center;
            align-items: flex-start;
            height: 100vh;
            text-align: center;
        }
        .content {
            margin-top: 50px;
        }
        </style>
        <div class="centered">
            <div class="content">
                <h1>Página Principal</h1>
                <p>Bienvenidos: Dashboard Store Sales!!</p>
                <p>Desplega el menú de la izquierda para navegar por cada vista</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.sidebar.image('logo.png')
st.sidebar.title("Dashboard Store Sales")
pagina = st.sidebar.selectbox("Selecciona una vista", ["Página principal", "Resumen General", "Detalle"])

if pagina == "Página principal":
    pagina_principal()
elif pagina == "Resumen General":
    dash.mostrar_resumen_general()  # Llama a la función del archivo dashboard.py
elif pagina == "Detalle":
    detal.filtro_detalle() # Llama a la función del archivo detalle.py