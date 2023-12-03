import requests
import pandas as pd

class Validater:
    def __init__(self, pair, timeframe):

        self._valid_timeframes = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']
        
        r = requests.get("https://api3.binance.com/api/v3/ticker/price")
        df = pd.DataFrame(r.json())
        df.drop(df[~df.symbol.str.contains('USDT')].index, inplace=True)#
        
        self._valid_pairs = df.symbol.to_list()
        self.pair = pair
        self.timeframe = timeframe
    
    @property
    def pair(self):
        return self._pair
    
    @property
    def timeframe(self):
        return self._timeframe
    
    @pair.setter
    def pair(self, pair):
        if not pair in self._valid_pairs: 
            raise ValueError(f"Validating provided trading pair. {pair} is an invalid pair. Ensure the provided pair is a valid USDT pair from the following list: {self._valid_pairs}")
        self._pair = pair

    @pair.setter
    def timeframe(self, timeframe):
        if not timeframe in self._valid_timeframes: 
            raise ValueError(f"Validating provided trading timeframe. {timeframe} is an invalid timeframe. Ensure the provided timeframe is selected from the following list: {self._valid_timeframes}")
        self._timeframe = timeframe