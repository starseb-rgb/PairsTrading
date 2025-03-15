import requests
import configparser
import asyncio
import websockets
import json
import ssl
import certifi

import pandas as pd

config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['ALPACA']['API_KEY']
API_SECRET = config['ALPACA']['SECRET_KEY']
ALPACA_WSS_URL = "wss://stream.data.alpaca.markets/v2/iex"

ssl_context = ssl.create_default_context(cafile=certifi.where())

async def connect():
    async with websockets.connect(ALPACA_WSS_URL, ssl=ssl_context) as ws:
        try:
            # Authenticate
            auth_msg = {
                "action": "auth",
                "key": API_KEY,
                "secret": API_SECRET
            }
            await ws.send(json.dumps(auth_msg))
            print("Authenticated!")

            # Subscribe to AAPL trades
            sub_msg = {
                "action": "subscribe",
                "trades": ["AAPL"]
            }
            await ws.send(json.dumps(sub_msg))
            print("Subscribed to AAPL trades")

            # Listen for messages
            while True:
                response = await ws.recv()
                print("Received:", response)

        except asyncio.CancelledError:
            print("Disconnecting gracefully...")
            await ws.close()

async def main():
    try:
        await connect()
    except KeyboardInterrupt:
        print("Interrupted! Closing WebSocket...")
    finally:
        print("WebSocket closed.")

# Run WebSocket connection
asyncio.run(main())