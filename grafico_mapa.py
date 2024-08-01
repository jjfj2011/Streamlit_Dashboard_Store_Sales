import pandas as pd
import plotly.express as px

def crear_grafico(df):
    df_geo = pd.read_csv('https://raw.githubusercontent.com/jjfj2011/Dashboard_Store_Sales/main/latitude-longitude-cidades.csv', sep=';')

    # Renomblamos la columna 'uf' por 'ciudad'
    df_geo.rename(columns={'uf':'ciudad'}, inplace=True)

    # Agrupamos por la columna 'ciudad', y nos quedamos con los promedios de longitud y latitud
    df_geo_grouped = df_geo.groupby('ciudad').agg({
        'longitude': 'mean',
        'latitude': 'mean'
    }).reset_index()

    # Agrupamos df por 'ciudad' y sumando 'valor_total'
    df_grouped = df.groupby('ciudad').agg({
        'valor_total':'sum'
    }).reset_index()

    # Convertimos 'valor_total' a formato de moneda
    df_grouped['Ingresos'] = df_grouped['valor_total'].apply(lambda x: f"${x:,.2f}")

    df_mapa = df_grouped.merge(df_geo_grouped, on='ciudad', how='inner').sort_values(by='valor_total', ascending=True)

    graf_mapa = px.scatter_geo(df_mapa, 
                               lat = 'latitude', 
                               lon = 'longitude', 
                               scope = 'south america',
                               template = 'seaborn',
                               size = 'valor_total',
                               hover_name = 'ciudad',
                               hover_data = {'latitude':False, 'longitude':False, 'Ingresos': True, 'valor_total':False},
                               title = 'Ventas por Ciudades')
    

    return graf_mapa