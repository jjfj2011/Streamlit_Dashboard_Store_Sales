import pandas as pd
import plotly.express as px

def crear_grafico(df):

    vendedores = df.groupby('nombre_vendedor').agg(
        total_ventas = ('cantidad','sum')
    ).sort_values(by='total_ventas', ascending=False).reset_index()

    colors = ['#0077b6', '#1A4D83', '#063970', '#2f567D', '#4B6A92']
    fig = px.pie(
        vendedores.head(5),
        values = 'total_ventas',
        names = 'nombre_vendedor',
        title = 'Ventas por vendedores',
        color_discrete_sequence = colors
    )
    fig.update_layout(showlegend=False)
    fig.update_traces(textposition='inside', textinfo='percent+label', insidetextfont=dict(size=14), insidetextorientation='horizontal')

    return fig