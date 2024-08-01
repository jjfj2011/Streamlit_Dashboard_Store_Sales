import pandas as pd
import streamlit as st
import plotly.express as px


##**2.1 Cargando las bases de datos**
def cargar_data():
  df_itens_pedidos = pd.read_csv('https://raw.githubusercontent.com/ElProfeAlejo/Bootcamp_Databases/main/itens_pedidos.csv')
  # df_itens_pedidos.head()

  df_pedidos = pd.read_csv('https://raw.githubusercontent.com/ElProfeAlejo/Bootcamp_Databases/main/pedidos.csv')
  # df_pedidos.head()

  df_productos = pd.read_csv('https://raw.githubusercontent.com/ElProfeAlejo/Bootcamp_Databases/main/productos.csv')
  # df_productos.head()

  df_vendedores = pd.read_csv('https://raw.githubusercontent.com/ElProfeAlejo/Bootcamp_Databases/main/vendedores.csv')
  # df_vendedores.head()

  df_siglas_br = pd.read_csv('https://raw.githubusercontent.com/jjfj2011/Dashboard_Store_Sales/main/ISO-3166-2-BR.csv')
  # df_siglas_br = pd.read_csv('https://raw.githubusercontent.com/okfn-brasil/getlex/master/data/ISO-3166-2-BR.csv')
  # df_siglas_br.head()

  return df_itens_pedidos, df_pedidos, df_productos, df_vendedores, df_siglas_br


# **2.2 Tratamiento de Datos**"""
#@title
def preprocesamiento(df_itens_pedidos, df_pedidos, df_productos, df_vendedores, df_siglas_br):
  df_itens_pedidos['df_itens_pedidos_key'] = df_itens_pedidos['pedido_id'].astype(str) + df_itens_pedidos['producto_id'].astype(str)
  df_pedidos['df_pedidos_key'] = df_pedidos['pedido_id'].astype(str) + df_pedidos['producto_id'].astype(str)

  df_itens_pedidos = df_itens_pedidos.dropna(subset='df_itens_pedidos_key')
  df_pedidos = df_pedidos.dropna(subset='df_pedidos_key')
  df_productos = df_productos.dropna(subset='producto_id')
  df_vendedores = df_vendedores.dropna(subset='vendedor_id')

  df_itens_pedidos = df_itens_pedidos.dropna()
  df_pedidos = df_pedidos.dropna()
  df_productos = df_productos.dropna()
  df_vendedores = df_vendedores.dropna()

  df_itens_pedidos = df_itens_pedidos.drop_duplicates(subset='df_itens_pedidos_key')
  df_pedidos = df_pedidos.drop_duplicates(subset='df_pedidos_key')
  df_productos = df_productos.drop_duplicates(subset='producto_id')
  df_vendedores = df_vendedores.drop_duplicates(subset='vendedor_id')

  df_pedidos['fecha_compra'] = pd.to_datetime(df_pedidos['fecha_compra'], format='%Y-%m-%d', errors='coerce')
  df_productos['sku'] = df_productos['sku'].astype('int')

  df_itens_pedidos['ciudad'] = df_itens_pedidos['ciudad'].str.replace('BR-', '')
  df_itens_pedidos = pd.merge(df_itens_pedidos, df_siglas_br[['Subdivision', 'Name']], left_on='ciudad', right_on='Subdivision', how='left')
  df_itens_pedidos = df_itens_pedidos.drop(columns='Subdivision').rename(columns={'Name': 'state_name'})

  df_productos['tipo_producto'] = df_productos['producto'].str.split().str[0]

  df_itens_pedidos = df_itens_pedidos.drop(columns='df_itens_pedidos_key')
  df_pedidos = df_pedidos.drop(columns='df_pedidos_key')

  merged1 = pd.merge(df_itens_pedidos, df_pedidos, on=['producto_id', 'pedido_id'])
  merged2 = pd.merge(merged1, df_productos, on='producto_id')
  df_final = pd.merge(merged2, df_vendedores, on='vendedor_id')

  return df_final