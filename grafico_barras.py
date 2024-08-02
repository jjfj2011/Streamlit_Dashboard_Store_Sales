import pandas as pd
import plotly.express as px

def crear_grafico(df):

    revenue_productos = df.groupby('tipo_producto').agg({
        'valor_total':'sum'
    }).sort_values(by='valor_total', ascending=False).reset_index()

    # Formatear valores en dólares
    revenue_productos['ventas'] = revenue_productos['valor_total'].apply(lambda x: f'${x:,.0f}')

    fig = px.bar(revenue_productos.head(10),
                 x = 'tipo_producto',
                 y = 'valor_total',
                 text = 'valor_total',
                 title = 'Top Ventas por Producto ($)',
                 hover_data={'ventas':True, 'valor_total':False}
                 )
    
    fig.update_layout(yaxis_title='Ventas ($)', xaxis_title='Tipo de producto', showlegend=False, xaxis_tickangle=45)
    fig.update_traces(
        texttemplate='<b>%{text:.3s}</b>',
        textangle=90,  # Girar el texto dentro de las barras 90 grados
        )
    
    return fig
