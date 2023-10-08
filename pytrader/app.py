from streamer import Streamer
import asyncio

try:
    s = Streamer()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(s.start_stream()).stream()

except KeyboardInterrupt as e:
    s.end_stream()