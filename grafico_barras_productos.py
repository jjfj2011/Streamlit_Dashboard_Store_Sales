import pandas as pd
import plotly.express as px

def crear_grafico(df):

    revenue_productos = df.groupby('tipo_producto').agg(
        monto_total_productos = ('valor_total','sum')
    ).sort_values(by='monto_total_productos', ascending=False).reset_index()

    # Formatear valores en dólares
    revenue_productos['ventas'] = revenue_productos['monto_total_productos'].apply(lambda x: f'${x:,.0f}')

    fig = px.bar(revenue_productos.head(3),
                 x = 'tipo_producto',
                 y = 'monto_total_productos',
                 text = 'monto_total_productos',
                 hover_data = {'monto_total_productos':False, 'ventas':True}
                 )
    
    fig.update_layout(yaxis_title='Ventas ($)', xaxis_title='Producto', showlegend=False)
    fig.update_traces(
        texttemplate='<b>%{text:.3s}</b>'#,
        #textangle=90,  # Girar el texto dentro de las barras 90 grados
        )
    
    return fig
