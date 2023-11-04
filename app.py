from pytrader import streamer
import asyncio

def main():
    try:
        s = streamer.Streamer()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(s.start_stream()).stream()

    except KeyboardInterrupt as e:
        s.end_stream()

if __name__ == "__main__":
    print("START")
    main()
    print("END")