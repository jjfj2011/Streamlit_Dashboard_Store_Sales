import pandas as pd
import plotly.express as px

def crear_grafico(df):
    revenue_estados = df.groupby('state_name').agg(
        total_ventas_estados = ('valor_total','sum')
    ).sort_values(by='total_ventas_estados', ascending=True).reset_index()

    # Formatear valores en dólares
    revenue_estados['ventas'] = revenue_estados['total_ventas_estados'].apply(lambda x: f'${x:,.0f}')

    fig = px.bar(revenue_estados.tail(3),
                 x='state_name',
                 # x='total_ventas_estados',
                 y='total_ventas_estados',
                 # y='state_name',
                 text = 'total_ventas_estados',
                 hover_data = {'ventas':True, 'total_ventas_estados':False}
                 )
    fig.update_layout(yaxis_title='Ventas ($)', xaxis_title='Estados', showlegend=False)
    fig.update_traces(texttemplate = '<b>%{text:.3s}</b>')

    return fig
