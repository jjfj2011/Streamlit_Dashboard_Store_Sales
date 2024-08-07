import pandas as pd
import plotly.express as px

def crear_grafico(df):

    # Convertir fecha_compra a datetime si no lo está
    df['fecha_compra'] = pd.to_datetime(df['fecha_compra'])

    revenues_monthly = df.set_index('fecha_compra').groupby(pd.Grouper(freq='ME'))['valor_total'].sum().reset_index()
    revenues_monthly['Year'] = revenues_monthly['fecha_compra'].dt.year
    revenues_monthly['Month'] = revenues_monthly['fecha_compra'].dt.month_name()

    # Crear un diccionario para mapear los nombres de los meses a su orden
    month_order = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }

    # Ordenar los datos usando el diccionario
    revenues_monthly['Month'] = pd.Categorical(revenues_monthly['Month'], categories=month_order.keys(), ordered=True)
    revenues_monthly = revenues_monthly.sort_values(by=['Year', 'Month'])

    # Obtener el orden único de los años
    year_order = sorted(revenues_monthly['Year'].unique())

    fig = px.line(
        revenues_monthly,
        x = 'Month',
        y = 'valor_total',
        markers = True,
        range_y = (0, revenues_monthly.max()),
        color = 'Year',
        line_dash = 'Year',
        title = 'Ventas mensuales',
        category_orders={'Month': list(month_order.keys()), 'Year': year_order}  # Ordenar la leyenda por Year y Month
    )
    fig.update_layout(yaxis_title='Ventas ($)', xaxis_tickangle=90, template='plotly_dark')

    return fig
