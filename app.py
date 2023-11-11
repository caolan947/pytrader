from pytrader import streamer
import asyncio
import argparse
from pytrader import logger

def main():
    print("START")

    log, file_name = logger.config_logger()

    argParser = argparse.ArgumentParser()
    argParser.add_argument("-p", "--pair", help="Trading pair to stream")
    argParser.add_argument("-t", "--timeframe", help="Timeframe for candles data")
    args = argParser.parse_args()

    try:
        print(f"Starting live market data stream for {args.pair} using a {args.timeframe} timeframe")

        s = streamer.Streamer(args.pair, args.timeframe, log, file_name)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(s.start_stream()).stream()

    except KeyboardInterrupt as e:
        print(f"Ending live market data stream for {args.pair} using a {args.timeframe} timeframe")
        s.end_stream()

    print(f"END")

if __name__ == "__main__":
    main()
