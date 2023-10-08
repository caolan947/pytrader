from datetime import datetime
import pandas as pd
from binance.client import Client
from binance import BinanceSocketManager
import asyncio
from pytrader import logger

class Streamer:
    def __init__(self):
        PAIR = 'BTCUSDT'
        TIMEFRAME = Client.KLINE_INTERVAL_1MINUTE

        self.log = logger.config_logger()
        self.run = True

        self.log.info("Creating Binance API client")
        self.client = Client()
        self.log.info("Initialising BinanceSocketManager")
        self.bm = BinanceSocketManager(self.client)
        self.log.info(f"Connecting to websocket for {PAIR} kline for {TIMEFRAME} interval")
        self.ks = self.bm.kline_socket(PAIR, interval=TIMEFRAME)

    async def start_stream(self):
        self.log.info(f"Beginning market data stream")

        async with self.ks as kscm:
            while self.run:
                result = await kscm.recv()

                # Load dataframe
                df = pd.DataFrame(result['k'], index=[0])

                # Transform data
                df = df.rename(columns={'t': 'Open_time', 'o': 'Open', 'h': 'High', 'l': 'Low', 'c': 'Close', 'T': 'Close_time', 'x': 'Close_flag'})
                df['Stream_time'] = datetime.fromtimestamp(result['E'] / 1e3)
                df['Open_time'] = pd.to_datetime(df['Open_time'], unit='ms')
                df['Open'] = pd.to_numeric(df['Open'])
                df['High'] = pd.to_numeric(df['High'])
                df['Low'] = pd.to_numeric(df['Low'])
                df['Close'] = pd.to_numeric(df['Close'])
                df['Close_time'] = pd.to_datetime(df['Close_time'], unit='ms')

                # Drop unused columns
                columns = ['s', 'i', 'f', 'L', 'v', 'n', 'q','V', 'Q', 'B']
                df.drop(columns, axis = 1, inplace = True)

                # Extract first row
                df_item = df.iloc[0]
       
                print(df_item)
                self.log.info(df_item.to_dict())

    def end_stream(self):
        self.run = False
        self.log.info(f"Ending market data stream")
