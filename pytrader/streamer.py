from binance.client import Client
from binance import BinanceSocketManager

from pytrader.candle import Candle
from pytrader import logger

class Streamer:
    def __init__(self):
        """
        Stream candle data for a given symbol
        """
        self.pair = 'BTCUSDT'
        self.timeframe = Client.KLINE_INTERVAL_1MINUTE        
        self.run = True

        self.log = logger.config_logger()

        self.log.info("Creating Binance API client")
        self.client = Client()

        self.log.info("Initialising BinanceSocketManager")
        self.bm = BinanceSocketManager(self.client)

        self.log.info(f"Connecting to websocket for {self.pair} kline for {self.timeframe} interval")
        self.ks = self.bm.kline_socket(self.pair, interval=self.timeframe)

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