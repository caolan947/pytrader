from streamer import Streamer
import asyncio

def main():
    try:
        s = Streamer()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(s.start_stream()).stream()

    except KeyboardInterrupt as e:
        s.end_stream()

if __name__ == "__main__":
    main()