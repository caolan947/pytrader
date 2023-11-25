from pytrader import streamer
import asyncio
import argparse
from pytrader import logger
import yaml

def main():
    print("START")

    log, file_name = logger.config_logger()

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-p", "--pair", help="Trading pair to stream")
    arg_parser.add_argument("-t", "--timeframe", help="Timeframe for candles data")
    args = arg_parser.parse_args()

    config = yaml.safe_load(open('config.yml'))

    try:
        print(f"Starting live market data stream for {args.pair} using a {args.timeframe} timeframe")

        s = streamer.Streamer(args.pair, args.timeframe, log, file_name, config)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(s.start_stream()).stream()

    except KeyboardInterrupt as e:
        print(f"Ending live market data stream for {args.pair} using a {args.timeframe} timeframe")
        s.end_stream()

    print(f"END")

if __name__ == "__main__":
    main()
