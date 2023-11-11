from binance.client import Client
from binance import BinanceSocketManager
import uuid
from pytrader.sql_handler import SqlController
import config

from pytrader.candle import Candle

class Streamer:
    def __init__(self, pair, timeframe, log, file_name):
        """
        Stream candle data for a given symbol
        """
        self.pair = pair
        self.timeframe = timeframe
        self.log = log
        self.file_name = file_name
        self.run = True
        
        self.log.info(f"Setting up market data streamer")

        self.stream_id = uuid.uuid4()
        self.log.info(f"Stream ID {self.stream_id}")#

        self.log.info(f"Creating database client")
        self.db = SqlController(
            config.creds['driver'],
            config.creds['server'],
            config.creds['database'],
            config.creds['username'],
            config.creds['password'],
            pair,
            timeframe,
            file_name,
            log
        )

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
        
        self.db.db_write_start_stream(self.stream_id)

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
        self.db.db_write_end_stream(self.stream_id)
        self.db.close_cursor()
        self.run = False

