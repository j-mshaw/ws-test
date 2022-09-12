import json
import websockets
import asyncio
import os
import signal

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
        elif message_from_client["type"] == "query":
            for s in subscribers:
                print(s)
            print()
        elif message_from_client["type"] == "clear":
            subscribers.clear()
async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    
    #when termination signal is recieved, the future is resolved and we move past await stop in the serve block
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    port = int(os.environ.get("PORT", "8001"))
    
    async with websockets.serve(handler,"",port):
        await stop

if __name__ == "__main__":
    asyncio.run(main())



