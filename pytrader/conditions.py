def trade_open_condition(candle):
    if candle.close <= 50000:
        return True
    else:
        return False
    
def trade_close_condition(candle):
    if candle.close >= 100:
        return True
    else:
        return False