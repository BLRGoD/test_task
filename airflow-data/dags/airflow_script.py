import requests
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET
from clickhouse_driver import Client
import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    'owner' : 'airflow',
    'start_date' : datetime.datetime(2024,12,12)
}

dag = DAG(
    dag_id='Parse_Data',
    default_args=default_args,
    schedule_interval='@daily',
    description='Sobes Airflow Script',
    catchup=False,
    max_active_runs=1,
    tags=['MYJOB']
)

def req():
    url = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req=22/12/2024'
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp
    else:
        raise ConnectionError('request failed')
    
    
def get_data(currencies):

    resp = ET.fromstring(req().content)
    data = []
    for valute in resp.findall('.//Valute'):
        item = {
            'ID': valute.get('ID'),
            'NumCode': valute.find('NumCode').text,
            'CharCode': valute.find('CharCode').text,
            'Nominal': valute.find('Nominal').text,
            'Name': valute.find('Name').text,
            'Value': valute.find('Value').text
        }
        data.append(item)

    df = pd.DataFrame(data)
    df['Value'] = pd.to_numeric(df['Value'].str.replace(',','.'))

    USD_rate = df[df['CharCode'] == 'USD']['Value'].iloc[0]
    EUR_rate =df[df['CharCode'] == 'EUR']['Value'].iloc[0]
    df['X_to_USD'] = 0.0
    df['USD_to_X'] = 0.0
    df['X_to_EUR'] = 0.0
    df['EUR_to_X'] = 0.0

    df = df[df['CharCode'].isin(currencies)]

    for i, row in df.iterrows():
      val = row['Value'] 
      df.at[i, 'X_to_USD'] = float(val/USD_rate)
      df.at[i,'USD_to_X'] = float(USD_rate/val)
      df.at[i,'X_to_EUR'] = float(val/EUR_rate)
      df.at[i,'EUR_to_X'] = float(EUR_rate/val)


    df[['Value','X_to_USD','USD_to_X','X_to_EUR','EUR_to_X']] = df[['Value','X_to_USD','USD_to_X','X_to_EUR','EUR_to_X']].astype(np.float64)
    df[['ID','NumCode','CharCode','Name']] = df[['ID','NumCode','CharCode','Name']].astype(str)

    return df

  
def insert(currencies):
    client = Client('127.0.0.1', port=9000, user='airflow', password='airflow')
    
    df = get_data(currencies)
    client.execute("INSERT INTO default.ECB_table VALUES", df.to_dict('records'))

def main():
    fiat_currencies = ['JPY', 'BGN', 'CZK', 'DKK', 'GBP', 'HUF', 'PLN',
                   'RON', 'SEK', 'CHF', 'ISK', 'NOK', 'TRY', 'AUD',
                   'BRL', 'CAD', 'CNY', 'HKD', 'IDR', 'ILS', 'INR',
                   'KRW', 'MXN', 'MYR', 'NZD', 'PHP', 'SGD', 'THB', 'ZAR']
    
    insert(fiat_currencies)


task = PythonOperator(
    task_id='Parse_Data_task',
    python_callable=main,
    dag=dag
)

task
