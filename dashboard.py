import folium
import geopandas
import numpy     as np
import pandas    as pd
import streamlit as st

import plotly.express as px

from datetime         import datetime
from folium.plugins   import MarkerCluster
from streamlit_folium import folium_static

st.set_page_config(layout='wide')

@st.cache(allow_output_mutation=True)
def get_data(path):
  data = pd.read_csv(path)
  return data

@st.cache(allow_output_mutation=True)
def get_geofile(url):
  geofile = geopandas.read_file(url)
  return geofile

def set_feature(data):
  # alterando tipo dos dados
  data['date'] = pd.to_datetime(data['date'])
  # criando coluna preço por área quadrada
  data['price_per_sqft_living'] = data['price'] / data['sqft_living']
  return data

def overview_data(data):
  st.title('HOUSE ROCKET - DASHBOARD')
  st.sidebar.title('Visão Geral dos Dados')
  st.title('Visão Geral dos Dados')
  f_features = st.sidebar.multiselect('Selecione as Colunas', data.columns)
  f_zipcode = st.sidebar.multiselect('Selecione os zipcodes', data['zipcode'].sort_values().unique(), key='multiselect1')

  df = data.loc[data['zipcode'].isin(f_zipcode), :].copy() if f_zipcode else data.copy() 
  df = df.loc[:, f_features] if f_features else df

  st.dataframe(df)

  c1, c2 = st.columns((1, 1))
  df = data.loc[data['zipcode'].isin(f_zipcode), :].copy() if f_zipcode else data.copy()

  # médias
  df1 = df[['id', 'zipcode']].groupby('zipcode').count().reset_index()
  df2 = df[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
  df3 = df[['sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()
  df4 = df[['price_per_sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()

  # merge
  m1 = pd.merge(df1, df2, on='zipcode', how='inner')
  m2 = pd.merge(m1, df3, on='zipcode', how='inner')
  df5 = pd.merge(m2, df4, on='zipcode', how='inner')
  df5.columns = ['zipcode', 'número de casas', 'média dos preços', 'média das áreas úteis', 'média dos preços por área quadrada']
  c1.subheader('Valores Médios')
  c1.dataframe(df5, height=400)

  # Estatística Descritiva
  num_attributes = df.select_dtypes(include=['int64', 'float64'])
  # métricas
  mean = pd.DataFrame(num_attributes.apply(np.mean))
  median = pd.DataFrame(num_attributes.apply(np.median))
  std = pd.DataFrame(num_attributes.apply(np.std))
  max_ = pd.DataFrame(num_attributes.apply(np.max))
  min_ = pd.DataFrame(num_attributes.apply(np.min))

  df6 = pd.concat([max_, min_, mean, median, std], axis=1).reset_index()
  df6.columns = ['atributos', 'máx', 'mín', 'média', 'mediana', 'desvio padrão']

  c2.subheader('Análise Descritiva')
  c2.dataframe(df6, height=400)
  
  return None

def portfolio_density(data, geofile):  
  st.title('Visão Geral da Região')

  st.subheader('Densidade do Portfólio')
  df = data.sample(10)

  # Mapa - Folium
  density_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()],
                          default_zoom_start=15)

  marker_cluster = MarkerCluster().add_to(density_map)

  for name, row in df.iterrows():  
    folium.Marker([row['lat'], row['long']],
                  popup='Preço ${0} em: {1}. Features: {2} sqft, {3} quartos, {4} banheiros, ano de construção: {5}'.format(row['price'], row['date'].strftime('%d-%m-%Y'), row['sqft_living'], row['bedrooms'], row['bathrooms'], row['yr_built'])
                  ).add_to(marker_cluster)

  folium_static(density_map)

  # Mapa dos preços por região
  st.subheader('Preço por Região')

  df = df[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
  df.columns = ['zipcode', 'avg_price']

  region_price_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()],
                                default_zoom_start=15)

  geofile = geofile[geofile['ZIP'].isin(df['zipcode'].tolist())]

  region_price_map.choropleth(data=df, geo_data=geofile, columns=['zipcode', 'avg_price'],
                              key_on='feature.properties.ZIP', fill_color='YlOrRd', fill_opacity=0.7,
                              line_opacity=0.2, legend_name='Média de preços')

  folium_static(region_price_map)

  return None

def commercial_distribution(data):
  st.sidebar.title('Atributos Comerciais')
  st.title('Atributos Comerciais')

  # -- média do preço por ano de construção
  st.subheader('Média do Preço x Ano de Construção')

  # filtros
  st.sidebar.subheader('Selecione o ano de construção máximo')
  min_year_built = int(data['yr_built'].min())
  max_year_built = int(data['yr_built'].max())

  f_yr_built = st.sidebar.slider('Ano de Construção', min_year_built, max_year_built, min_year_built)

  # gráfico
  df = data[data['yr_built'] <= f_yr_built]
  df = df[['yr_built', 'price']].groupby('yr_built').mean().reset_index()
  fig = px.line(df, x='yr_built', y='price')
  st.plotly_chart(fig, use_container_width=True)

  # -- média do preço por data
  st.subheader('Média do Preço x Data')

  # filtros
  st.sidebar.subheader('Selecione a data máxima')
  min_date = datetime.strptime(data['date'].min().strftime('%Y-%m-%d'), '%Y-%m-%d')
  max_date = datetime.strptime(data['date'].max().strftime('%Y-%m-%d'), '%Y-%m-%d')

  f_date = st.sidebar.slider('Data Máxima', min_date, max_date, min_date)

  # gráfico
  df = data[data['date'] <= f_date]
  df = df[['date', 'price']].groupby('date').mean().reset_index()
  fig = px.line(df, x='date', y='price')
  st.plotly_chart(fig, use_container_width=True)

  # -- histograma
  st.subheader('Distribuição do Preço')

  # filtros
  st.sidebar.subheader('Selecione o Preço Máximo')
  min_price = int(data['price'].min())
  max_price = int(data['price'].max())
  avg_price = int(data['price'].mean())

  f_price = st.sidebar.slider('Preço Máximo', min_price, max_price, avg_price)

  # gráfico
  df = data[data['price'] <= f_price]
  fig = px.histogram(df, x='price', nbins=50)
  st.plotly_chart(fig, use_container_width=True)

  return None

def attributes_distribution(data):
  st.sidebar.title('Atributos Físicos')
  st.title('Atributos Físicos')

  # filtros
  f_bedrooms = st.sidebar.selectbox('Número Máximo de Quartos', data['bedrooms'].sort_values().unique())
  f_bathrooms = st.sidebar.selectbox('Número Máximo de Banheiros', data['bathrooms'].sort_values().unique())

  c1, c2 = st.columns(2)

  # -- house per bedrooms
  c1.subheader('Casas x Qtde de Quartos')
  df = data[data['bedrooms'] <= f_bedrooms]
  fig = px.histogram(df, x='bedrooms', nbins=20)
  c1.plotly_chart(fig, use_container_width=True)

  # -- house per bathrooms
  c2.subheader('Casas x Qtde de Banheiros')
  df = data[data['bathrooms'] <= f_bathrooms]
  fig = px.histogram(df, x='bathrooms', nbins=20)
  c2.plotly_chart(fig, use_container_width=True)

  # filtros
  f_floors = st.sidebar.selectbox('Número Máximo de Andares', data['floors'].sort_values().unique())
  f_waterview = st.sidebar.checkbox('Com Vista pra Água')

  c1, c2 = st.columns(2)

  # -- house per floors
  c1.subheader('Casas x Qtde de Andares')
  df = data[data['floors'] <= f_floors]
  fig = px.histogram(df, x='floors', nbins=20)
  c1.plotly_chart(fig, use_container_width=True)

  # -- house per water view
  c2.subheader('Casas x Vista para Água')
  df = data[data['waterfront'] == 1] if f_waterview else data
  fig = px.histogram(df, x='waterfront', nbins=10)
  c2.plotly_chart(fig, use_container_width=True)

  return None

def business_issues(data_q1, data_q2):
  st.title('Questões de Negócio')
  # -- Questão 01.
  st.subheader('1. Quais são os imóveis que a House Rocket deveria comprar e por qual preço?')

  # filtro
  c1, c2, c3 = st.columns(3)
  f_zipcode_q1 = c1.multiselect('Zipcode', data_q1['zipcode'].sort_values().unique(), key='multiselect2')
  f_condition_q1 = c2.multiselect('Condição do Imóvel', data_q1['condition'].sort_values().unique())
  f_status_q1 = c3.multiselect('Status do Imóvel', data_q1['status'].sort_values().unique())

  # dataframe
  df = data_q1[data_q1['zipcode'].isin(f_zipcode_q1)] if f_zipcode_q1 else data_q1.copy()
  df = df[df['condition'].isin(f_condition_q1)] if f_condition_q1 else df
  df = df[df['status'].isin(f_status_q1)] if f_status_q1 else df

  # gráfico
  st.dataframe(df, use_container_width=True)

  # -- Questão 02.
  st.subheader('2. Uma vez que o imóvel seja comprado, qual o melhor momento para vendê-lo e por qual preço?')

  # filtro
  c1, c2, c3 = st.columns(3)
  f_zipcode_q2 = c1.multiselect('Zipcode', data_q2['zipcode'].sort_values().unique(), key='multiselect3')
  f_season_q2 = c2.multiselect('Estação do Ano', data_q2['seasons_year'].sort_values().unique())
  f_status_q2 = c3.checkbox('Apenas imóveis sugeridos para compra')
  f_price_q2 = c3.checkbox('Imóveis com valor de venda menor do que a mediana da região/estação')

  # dataframe
  df = data_q2[data_q2['id'].isin(list(data_q1[data_q1['status'] == 'Compra']['id']))] if f_status_q2 else data_q2.copy()
  df = df[df['sale_price'] < df['median_total_price']] if f_price_q2 else df
  df = df[df['zipcode'].isin(f_zipcode_q2)] if f_zipcode_q2 else df
  df = df[df['seasons_year'].isin(f_season_q2)] if f_season_q2 else df

  profit = '$ ' + '{:,.2f}'.format(df['profit'].sum())
  number_of_houses = str(df.shape[0]) + ' imóveis'

  # gráfico
  st.dataframe(df, use_container_width=True)
  st.write(f'Quantidade: {number_of_houses}')
  st.write(f'Lucro estimado com os imóveis selecionados: {profit}')

  return None

if __name__ == '__main__':
  # data extration
  # carregando os dados
  path = 'dataset/kc_house_data.csv'
  path_q1 = 'dataset/df_q1.csv'
  path_q2 = 'dataset/df_q2.csv'
  url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'

  data = get_data(path)
  data_q1 = get_data(path_q1)
  data_q2 = get_data(path_q2)
  geofile = get_geofile(url)
  
  # transformation
  data = set_feature(data)
  overview_data(data)
  portfolio_density(data, geofile)
  commercial_distribution(data)
  attributes_distribution(data)
  business_issues(data_q1, data_q2)
