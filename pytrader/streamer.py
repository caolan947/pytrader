from datetime import datetime
import pandas as pd
from binance.client import Client
from binance import BinanceSocketManager
import asyncio

PAIR = 'BTCUSDT'
TIMEFRAME = Client.KLINE_INTERVAL_1MINUTE

client = Client()
bm = BinanceSocketManager(client)
ks = bm.kline_socket(PAIR, interval=TIMEFRAME)

async def stream():
    async with ks as kscm:
        while True:
            result = await kscm.recv()

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
            streamed_kline = df_item.to_dict()              
            
            print(streamed_kline)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(stream())