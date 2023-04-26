# IMPORTAÇÕES 
import pandas as pd

# mostrar todas as colunas do pandas
pd.set_option('display.max_columns', None) 
# remoção da notação cientifica
pd.set_option('display.float_format', lambda x: '%.2f' % x) 

def read_data(path):
  # carregando dataset
  df = pd.read_csv(path)
  
  return df

def data_cleaning(data):
  # Convertendo a data
  data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')

  # Filtrando as linhas
  # removendo ids duplicados, mantendo apenas o último registro
  data = data.sort_values('date', ascending=False)
  data = data.drop_duplicates(subset='id', keep='first')
  # removendo casas com bedrooms = 0
  data = data.loc[~(data['bedrooms'] == 0), :]
  # removendo casas com bathrooms = 0
  data = data.loc[~(data['bathrooms'] == 0), :]
  # substituindo o bedrooms = 33 por 3
  data.loc[(data['bedrooms'] == 33), 'bedrooms'] = 3
  
  return data

def feature_engineering(data):
  # price_per_sqft_living
  data['price_per_sqft_living'] = data.apply(lambda x: x['price'] / x['sqft_living'], axis=1)
  # year
  data['year'] = data['date'].dt.year
  # month
  data['month'] = data['date'].dt.month
  # adicionando as estações do ano
  seasons_year = {1: 'winter', 2: 'winter', 3:'spring', 4:'spring', 5:'spring', 6:'summer', 7:'summer', 8:'summer', 9:'fall', 10:'fall', 11:'fall', 12:'winter'}
  data['seasons_year'] = data['month'].map(seasons_year)

  return data

def load_data(data):
  # Q1. Quais são os imóveis que a House Rocket deveria comprar e por qual preço?
  # calculando a mediana por zipcode  
  aux1_q1 = data[['zipcode', 'price_per_sqft_living']].groupby('zipcode').median().reset_index().rename(columns={'price_per_sqft_living': 'median_price_per_zipcode'})
  aux2_q1 = pd.merge(data, aux1_q1, how='left', on='zipcode')
  # calculando o valor total dos imóveis com a mediana do zipcode
  aux2_q1['median_total_price'] = aux2_q1.apply(lambda x: x['sqft_living'] * x['median_price_per_zipcode'], axis=1)
  aux2_q1['status'] = aux2_q1.apply(lambda x: 'Compra' if (x['price_per_sqft_living'] < x['median_price_per_zipcode']) & (x['condition'] > 3) else 'Não Compra', axis=1)
  data_q1 = aux2_q1[['id', 'zipcode', 'price', 'median_total_price', 'condition', 'status']]

  # Q2. Uma vez o imóvel comprado, qual o melhor momento para vendê-lo e por qual preço?
  # calculando a mediana por zipcode e seasons_year
  aux1_q2 = data[['zipcode', 'seasons_year', 'price_per_sqft_living']].groupby(['zipcode', 'seasons_year']).median().reset_index().rename(columns={'price_per_sqft_living': 'median_price_per_zipcode_season'})
  aux2_q2 = pd.merge(data, aux1_q2, on=['zipcode', 'seasons_year'])
  # calculando o valor total dos imóveis com a mediana do zipcode/seasons
  aux2_q2['median_total_price'] = aux2_q2.apply(lambda x: x['sqft_living'] * x['median_price_per_zipcode_season'], axis=1)
  # calculando o valor total de venda dos imóveis
  # para imóveis com preço de compra abaixo da mediana, utilizar fator de 1.3, caso contrário, de 1.1
  aux2_q2['sale_price'] = aux2_q2.apply(lambda x: x['price'] * 1.3 if x['price_per_sqft_living'] <= x['median_price_per_zipcode_season'] else x['price'] * 1.1, axis=1 )
  # calculando o lucro
  aux2_q2['profit'] = aux2_q2.apply(lambda x: x['sale_price'] - x['price'], axis=1)
  data_q2 = aux2_q2[['id', 'zipcode', 'seasons_year', 'price', 'median_total_price', 'sale_price', 'profit']]

  return data_q1, data_q2

def saving_data(data, path):
    data.to_csv(path, index=False)

    return None

if __name__ == '__main__':
  path = 'dataset/kc_house_data.csv'  
  df_raw = read_data(path)
  
  df1 = data_cleaning(df_raw)
  
  df2 = feature_engineering(df1)

  df_q1, df_q2 = load_data(df2)

  path1 = 'dataset/filtered_kc_house_data.csv'
  saving_data(df2, path1)

  path2 = 'dataset/df_q1.csv'
  saving_data(df_q1, path2)

  path3 = 'dataset/df_q2.csv'
  saving_data(df_q2, path3)