from datetime import datetime
import pandas as pd
from binance.client import Client
from binance import BinanceSocketManager
import asyncio
import logging
import logging.config


logging.config.dictConfig({'version': 1, 'disable_existing_loggers': True,})

PAIR = 'BTCUSDT'
TIMEFRAME = Client.KLINE_INTERVAL_1MINUTE

client = Client()
bm = BinanceSocketManager(client)
ks = bm.kline_socket(PAIR, interval=TIMEFRAME)


def fetch_historic_klines():
    pd.set_option('display.max_rows', None)
    df = pd.DataFrame(
        client.get_historical_klines(
            PAIR,
            TIMEFRAME,
            "1 day ago UTC"))

    return df

def transform_klines(kline_df):
    transformed_df = pd.DataFrame()
    transformed_df['Open_time'] = pd.to_datetime(kline_df[0], unit='ms')
    transformed_df['Close_time'] = pd.to_datetime(kline_df[6], unit='ms')
    transformed_df['Open'] = pd.to_numeric(kline_df[1])
    transformed_df['High'] = pd.to_numeric(kline_df[2])
    transformed_df['Low'] = pd.to_numeric(kline_df[3])
    transformed_df['Close'] = pd.to_numeric(kline_df[4])

    return transformed_df

def fetch_historical_as_records(data):
    data = transform_klines(data)

    return data.to_dict('records')

def transform_stream_to_record(result):
    stream_time = result['E']
    data = result['k']

    df = pd.DataFrame(data, index=[0])
    df['Stream_time'] = datetime.fromtimestamp(stream_time / 1e3)
    df = df.rename(columns={'t': 'Open_time', 'o': 'Open', 'h': 'High', 'l': 'Low', 'c': 'Close', 'T': 'Close_time', 'x': 'Close_flag'})
    df['Open_time'] = pd.to_datetime(df['Open_time'], unit='ms')
    df['Open'] = pd.to_numeric(df['Open'])
    df['High'] = pd.to_numeric(df['High'])
    df['Low'] = pd.to_numeric(df['Low'])
    df['Close'] = pd.to_numeric(df['Close'])
    df['Close_time'] = pd.to_datetime(df['Close_time'], unit='ms')

    first_column = df.pop('Stream_time')
    columns = ['s', 'i', 'f', 'L', 'v', 'n', 'q','V', 'Q', 'B']
    df.drop(columns, axis = 1, inplace = True)
    
    df.insert(0, 'Stream_time', first_column)
    df_item = df.iloc[0]

    return df_item.to_dict()

def pop_dict_list(dict_list, new_dict, pops):
    
    [new_dict.pop(key) for key in pops]
       
    dict_list.append(new_dict)

    return dict_list

def fetch_list_without_index(list, index):
    del list[index]

    return list

def result_to_record(result):
    if result:
        streamed_kline = transform_stream_to_record(result)
        return streamed_kline

def remove_open_candle(streamed_kline, historical_records):
    if streamed_kline['Open_time'] == historical_records[-1]['Open_time']:
        historical_records = fetch_list_without_index(historical_records, -1)

    return historical_records

async def stream():

    historical_df = fetch_historic_klines()
    historical_df = transform_klines(historical_df)

    historical_records = historical_df.to_dict('records')

  
    async with ks as kscm:
        while True:
            result = await kscm.recv()

            ### Check if not a candle close
            if result and result['k']['x'] is False:

                streamed_kline = result_to_record(result)

            elif result and result['k']['x'] is True:
                streamed_kline = result_to_record(result)

                historical_records = remove_open_candle(streamed_kline, historical_records)

                historical_records = fetch_list_without_index(historical_records, 0)
                historical_records = pop_dict_list(historical_records, streamed_kline, ['Stream_time', 'Close_flag'])

            
            print(result)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(stream())