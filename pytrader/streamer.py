from binance.client import Client
from binance import BinanceSocketManager
import uuid
from pytrader import sql_handler

from pytrader.candle import Candle
from pytrader import validate
from pytrader import conditions

class Streamer:
    def __init__(self, pair, timeframe, log, file_name, config):
        """
        Stream candle data for a given symbol
        """
        log.info(f"Setting up market data streamer")

        self.pair = pair
        self.timeframe = timeframe
        self.log = log
        self.file_name = file_name
        self.config = config
        self.open_condition = conditions.trade_open_condition
        self.close_condition = conditions.trade_close_condition

        self.run = True
        self.trade_open = False
        
        self.stream_id = uuid.uuid4()
        self.log.info(f"Stream ID {self.stream_id}")

        self.log.info(f"Creating database client")
        self.db = sql_handler.SqlController(
            config['database']['credentials']['driver'],
            config['database']['credentials']['server'],
            config['database']['credentials']['database'],
            config['database']['credentials']['username'],
            config['database']['credentials']['password'],
            pair,
            timeframe,
            file_name,
            log
        )

        self.log.info("Creating Binance API client")
        self.client = Client()

        try:
            self.log.info("Validating provided pair and timeframe values")
            self.validate = validate.Validater(self.pair, self.timeframe)

        except ValueError as e:
            self.log.error("Validation failed")
            raise e

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
                self.candle = Candle(result, self.db, self.stream_id)
                
                if not self.trade_open and self.candle.close_flag:
                    if self.open_condition(self.candle):
                        self.trade_id = uuid.uuid4()
                        self.db.db_write_open_trade(self.candle, self.trade_id)
                        self.trade_open = True

                elif self.trade_open and self.candle.close_flag:
                    if self.close_condition(self.candle):
                        self.db.db_write_close_trade(self.candle, self.trade_id)
                        self.trade_open = False
                        self.trade_id = None                

                self.log.info(self.candle.to_dict())

    def end_stream(self):
        """
        Finish streaming and logging candle data
        """
        self.log.info(f"Ending market data stream")
        if self.trade_open:
            self.candle.on_error()
            self.db.db_write_close_trade(self.candle, self.trade_id)
            self.trade_open = False
            self.trade_id = None   

        self.db.db_write_end_stream(self.stream_id)
        self.db.close_cursor()
        self.run = False