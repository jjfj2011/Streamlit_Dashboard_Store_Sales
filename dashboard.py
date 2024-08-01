import pandas as pd
import streamlit as st
import plotly.express as px
from store_sales_interactive_dashboard import cargar_data, preprocesamiento
import grafico_mapa as graf1
import grafico_lineas as graf2
import grafico_barras as graf3
import grafico_pizza as graf4
# import grafico_barras_vendedores as graf5

def mostrar_resumen_general():
    # st.set_page_config(layout='wide')

    st.title('Dashboard Store Sales :shopping_trolley:')

    def formata_numero(valor, prefijo=''):
        for unidad in ['', 'k']:
            if valor < 1000:
                return f'{prefijo} {valor:.2f} {unidad}'
            valor /= 1000
        return f'{prefijo} {valor:.2f} M'

    # Panel lateral
    # st.sidebar.image('logo.png')
    st.sidebar.title('Filtros')

    # Cargar los datos
    df_itens_pedidos, df_pedidos, df_productos, df_vendedores, df_siglas_br = cargar_data()

    # Realizar el preprocesamiento
    df_final = preprocesamiento(df_itens_pedidos, df_pedidos, df_productos, df_vendedores, df_siglas_br)

    # Filtrando datos
    estados = sorted(list(df_final['state_name'].unique()))
    ciudades = st.sidebar.multiselect('Estados', estados)
    productos = sorted(list(df_final['tipo_producto'].unique()))
    productos.insert(0, 'Todos')
    producto = st.sidebar.selectbox('Productos', productos)
    años = st.sidebar.checkbox('Todo el periodo', value=True)

    if ciudades:
        df_final = df_final[df_final['state_name'].isin(ciudades)]
    if producto != 'Todos':
        df_final = df_final[df_final['tipo_producto'] == producto]
    if not años:
        año = st.sidebar.slider('Año', df_final['fecha_compra'].dt.year.min(), df_final['fecha_compra'].dt.year.max())
        df_final_año_actual = df_final[df_final['fecha_compra'].dt.year == año]
        if año > df_final['fecha_compra'].dt.year.min():
            df_final_año_anterior = df_final[df_final['fecha_compra'].dt.year == (año - 1)]
            variacion = ((df_final_año_actual['valor_total'].sum() - df_final_año_anterior['valor_total'].sum()) / df_final_año_anterior['valor_total'].sum()) * 100
            variacion_cantidad = ((df_final_año_actual['cantidad'].sum() - df_final_año_anterior['cantidad'].sum()) / df_final_año_anterior['cantidad'].sum()) * 100
        else:
            variacion = 0
            variacion_cantidad = 0
        df_final = df_final[df_final['fecha_compra'].dt.year == año]
    else:
        variacion = 100
        variacion_cantidad = 100

    # Llamar a los gráficos
    graf_mapa = graf1.crear_grafico(df_final)
    graf_lineas = graf2.crear_grafico(df_final)
    graf_barras = graf3.crear_grafico(df_final)
    graf_pizza = graf4.crear_grafico(df_final)
    # graf_barras_vendedores = graf5.crear_grafico(df_final)

    col1, col2 = st.columns(2)
    with col1:
        st.metric('**Valor Total**', formata_numero(df_final['valor_total'].sum()), f'{variacion:,.2f}%')
        st.plotly_chart(graf_mapa, use_container_width=True)
        st.plotly_chart(graf_barras, use_container_width=True)
    with col2:
        st.metric('Cantidad total', formata_numero(df_final['cantidad'].sum()), f'{variacion_cantidad:,.2f}%')
        st.plotly_chart(graf_lineas, use_container_width=True)
        st.plotly_chart(graf_pizza, use_container_width=True)

    
