from pytrader import streamer
import asyncio
import argparse

def main(pair, timeframe):
    try:
        s = streamer.Streamer(pair, timeframe)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(s.start_stream()).stream()

    except KeyboardInterrupt as e:
        s.end_stream()

if __name__ == "__main__":

    argParser = argparse.ArgumentParser()
    argParser.add_argument("-p", "--pair", help="Trading pair to stream")
    argParser.add_argument("-t", "--timeframe", help="Timeframe for candles data")
    args = argParser.parse_args()

    print(f"START \nStarting live market data stream for {args.pair} using a {args.timeframe} timeframe")
    main(args.pair, args.timeframe)
    print(f"END \nEnding live market data stream for {args.pair} using a {args.timeframe} timeframe")
