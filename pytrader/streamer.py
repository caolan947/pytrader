from datetime import datetime
import pandas as pd
from binance.client import Client
from binance import BinanceSocketManager
import logger

class Streamer:
    def __init__(self):
        """
        Stream candle data for a given symbol
        """

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
        """
        Begin streaming and logging candle data
        """
        self.log.info(f"Beginning market data stream")
        async with self.ks as kscm:
            while self.run:
                result = await kscm.recv()

                c = Candle(result)
                self.log.info(c.to_dict())

    def end_stream(self):
        """
        Finish streaming and logging candle data
        """
        self.log.info(f"Ending market data stream")
        self.run = False

class Candle():
    """
    An object representing a chart candle.
    """
    def __init__(self, message):
        """
        Args:
            message (`dict`): Uncleansed message received from websocket
        """

        df = pd.DataFrame(message['k'], index=[0])

        df = df.rename(columns={'t': 'Open_time', 'o': 'Open', 'h': 'High', 'l': 'Low', 'c': 'Close', 'T': 'Close_time', 'x': 'Close_flag'})
        df['Stream_time'] = datetime.fromtimestamp(message['E'] / 1e3)
        df['Open_time'] = pd.to_datetime(df['Open_time'], unit='ms')
        df['Open'] = pd.to_numeric(df['Open'])
        df['High'] = pd.to_numeric(df['High'])
        df['Low'] = pd.to_numeric(df['Low'])
        df['Close'] = pd.to_numeric(df['Close'])
        df['Close_time'] = pd.to_datetime(df['Close_time'], unit='ms')

        df = df.iloc[0]

        self.open = df['Open']
        self.close = df['Close']
        self.high = df['High']
        self.low = df['Low']
        self.open_time = df['Open_time']
        self.close_time = df['Close_time']
        self.close_flag = df['Close_flag']

    def to_dict(self):
        """
        Return `Candle` object as a `dict`

        Returns:
            `dict`: `dict` containing the attributes of the `Candle` class 
        """
        return vars(self)