import json
import websockets
import asyncio

subscribers = []

async def handler(ws):
    subscribers.append(ws)
    while True:
        message_from_client = await ws.recv()
        print(message_from_client)
        message_from_client = json.loads(message_from_client)
        if message_from_client["type"] == "send_msg":
            for sub in subscribers:
                await ws.send(json.dumps({"type": "recv_msg", "content":message_from_client["content"]}))   

async def main():
    async with websockets.serve(handler,"192.168.56.1",8001):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())



