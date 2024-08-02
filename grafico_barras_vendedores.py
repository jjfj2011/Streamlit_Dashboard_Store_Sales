import pandas as pd
import plotly.express as px

def crear_grafico(df):

    revenue_vendedores = df.groupby('nombre_vendedor').agg(
        monto_total_vendedores = ('valor_total','sum')
    ).sort_values(by='monto_total_vendedores', ascending=False).reset_index()

    # Formatear valores en dólares
    revenue_vendedores['ventas'] = revenue_vendedores['monto_total_vendedores'].apply(lambda x: f'${x:,.0f}')

    fig = px.bar(revenue_vendedores.head(3),
                 x = 'nombre_vendedor',
                 y = 'monto_total_vendedores',
                 text = 'monto_total_vendedores',
                 hover_data = {'ventas':True, 'monto_total_vendedores':False}
                 )
    
    fig.update_layout(yaxis_title='Ventas ($)', xaxis_title='Vendedor', showlegend=False)
    fig.update_traces(
        texttemplate='<b>%{text:.3s}</b>'#,
        #textangle=90,  # Girar el texto dentro de las barras 90 grados
        )
    
    return fig
