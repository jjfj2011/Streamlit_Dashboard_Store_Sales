import pandas as pd
import streamlit as st
import plotly.express as px
from store_sales_interactive_dashboard import cargar_data, preprocesamiento
import grafico_barras_vendedores as graf1
import grafico_barras_estados as graf2
import grafico_barras_productos as graf3
import grafico_lineas as graf4

def filtro_detalle():
    #st.set_page_config(layout='wide')
    st.title('Detalle Store Sales :shopping_trolley:')

    def formata_numero(valor, prefijo=''):
        for unidad in ['', 'k']:
            if valor < 1000:
                return f'{prefijo} {valor:.2f} {unidad}'
            valor /= 1000
        return f'{prefijo} {valor:.2f} M'

    # Panel lateral
    # st.sidebar.image('logo.png')
    st.sidebar.title('Filtros Detalle')

    # Cargar los datos
    df_itens_pedidos, df_pedidos, df_productos, df_vendedores, df_siglas_br = cargar_data()

    # Realizar el preprocesamiento
    df_final = preprocesamiento(df_itens_pedidos, df_pedidos, df_productos, df_vendedores, df_siglas_br)

    # Filtrando datos
    vendedor = sorted(list(df_final['nombre_vendedor'].unique()))
    # vendedor.insert(0,'Todos')
    vendedores = st.sidebar.multiselect('Vendedor',vendedor)
    estados = sorted(list(df_final['state_name'].unique()))
    ciudades = st.sidebar.multiselect('Estados', estados)
    productos = sorted(list(df_final['tipo_producto'].unique()))
    # productos.insert(0, 'Todos')
    producto = st.sidebar.multiselect('Productos', productos)
    años = st.sidebar.checkbox('Todo el periodo', value=True)

    # Validamos si están seleccionados los filtros
    if vendedores:
        df_final = df_final[df_final['nombre_vendedor'].isin(vendedores)]

    if ciudades:
        df_final = df_final[df_final['state_name'].isin(ciudades)]

    if producto:
        df_final = df_final[df_final['tipo_producto'].isin(producto)]

    # Inicializar variacion
    variacion = 100
    variacion_cantidad = 100
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

    ###############################################################################################################################################################
    # Mostramos las columnas
    col1, col2 = st.columns(2)
    with col1:
        st.metric('**Total de Revenue**', formata_numero(df_final['valor_total'].sum()), f'{variacion:,.2f}%')
    with col2:
        st.metric('**Total de Ventas**', formata_numero(df_final['cantidad'].sum()), f'{variacion_cantidad:,.2f}%')
    ###############################################################################################################################################################

    ###############################################################################################################################################################
    # Llamamos a los gráficos
    graf_barras_vendedores = graf1.crear_grafico(df_final)
    graf_barras_estados = graf2.crear_grafico(df_final)
    graf_barras_productos = graf3.crear_grafico(df_final)
    graf_lineas = graf4.crear_grafico(df_final)
    ###############################################################################################################################################################

    # Top 3 Vendedores
    if vendedores:
        df_final_vendedores = df_final.groupby('nombre_vendedor').agg(monto_total=('valor_total', 'sum')).sort_values(by='monto_total', ascending=False).head(3)
    else:
        df_final_vendedores = df_final.groupby('nombre_vendedor').agg(monto_total=('valor_total', 'sum')).sort_values(by='monto_total', ascending=False).head(3)

    df_final_vendedores['monto_total'] = df_final_vendedores['monto_total'].apply(lambda x: f"${x:,.2f}")
    df_final_vendedores = df_final_vendedores.rename(columns={'monto_total': 'Ventas ($)'})
    df_final_vendedores.index.name = 'Vendedor'

    # Top 3 Estados
    if ciudades:
        df_final_estados = df_final.groupby('state_name').agg(monto_total=('valor_total','sum')).sort_values(by='monto_total', ascending=False).head(3)
    else:
        df_final_estados = df_final.groupby('state_name').agg(monto_total=('valor_total','sum')).sort_values(by='monto_total', ascending=False).head(3)

    df_final_estados['monto_total'] = df_final_estados['monto_total'].apply(lambda x: f"${x:,.2f}")
    df_final_estados = df_final_estados.rename(columns={'monto_total':'Ventas ($)'})
    df_final_estados.index.name = 'Estado'

    # Top 3 Productos
    if producto:
        df_final_producto = df_final.groupby('tipo_producto').agg(monto_total=('valor_total','sum')).sort_values(by='monto_total', ascending=False).head(3)
    else:
        df_final_producto = df_final.groupby('tipo_producto').agg(monto_total=('valor_total','sum')).sort_values(by='monto_total', ascending=False).head(3)

    df_final_producto['monto_total'] = df_final_producto['monto_total'].apply(lambda x: f"${x:,.2f}")
    df_final_producto = df_final_producto.rename(columns={'monto_total':'Ventas ($)'})
    df_final_producto.index.name='Producto'

    # Creamos un nuevo Dataframe Año vs Meses
    # Agrupar por año y mes y sumar 'valor_total'
    df_grouped = df_final.groupby([df_final['fecha_compra'].dt.year.rename('año'), 
                                df_final['fecha_compra'].dt.month.rename('mes')])['valor_total'].sum().reset_index()
    # Pivotar el DataFrame
    df_pivot = df_grouped.pivot(index='mes', columns='año', values='valor_total')
    # Rellenar valores NaN con 0
    df_pivot = df_pivot.fillna(0)
    # Creamos un diccionario de mapeo para los nombres de los meses
    month_mapping = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
        7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    # Aplicamos el mapeo a los índices del DataFrame
    df_pivot.index = df_pivot.index.map(month_mapping)


    ###############################################################################################################################################################
    # Mostramos las columnas
    st.markdown("### Información Top de Ventas ($)")
    col1, col2, col3 = st.columns(3)
    with col1:
        # st.markdown("### Vendedores - Ventas ($)")
        st.dataframe(df_final_vendedores, use_container_width=True)
        #st.plotly_chart(graf_barras_vendedores, use_container_width=True)
    with col2:
        st.dataframe(df_final_estados, use_container_width=True)
        #st.plotly_chart(graf_barras_estados, use_container_width=True)
    with col3:
        st.dataframe(df_final_producto, use_container_width=True)

    # st.markdown("### Gráficos sobre las Ventas ($)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(graf_barras_vendedores, use_container_width=True)
    with col2:
        st.plotly_chart(graf_barras_estados, use_container_width=True)
    with col3:
        st.plotly_chart(graf_barras_productos, use_container_width=True)
    ###############################################################################################################################################################

    st.plotly_chart(graf_lineas, use_container_width=True)
    col1, col2, col3 = st.columns([0.2, 1, 0.2])
    #with col1:
    with col2:
        st.dataframe(df_pivot, use_container_width=True)
    #with col3:
