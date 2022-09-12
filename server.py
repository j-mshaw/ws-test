from email import message
import json
import websockets
import asyncio
import os
import signal

rooms = {}
where_is = {}

def remove_ws_from_rooms(ws):
    for r in rooms:
        if ws in rooms[r]:
            rooms[r].remove(ws)
    where_is[ws] = None


async def handler(ws):
    while True:
        message_from_client = await ws.recv()
        print(message_from_client)
        message_from_client = json.loads(message_from_client)
        if message_from_client["type"] == "send_msg":
            room_subs = rooms[where_is[ws]]
            for sub in room_subs:
                await sub.send(json.dumps({"type": "recv_msg", "content":message_from_client["content"]}))   
        
        elif message_from_client["type"] == "query":
            for r in rooms:
                print(r)
                for s in rooms[r]:
                    print("\t" + str(s))
            print()
        elif message_from_client["type"] == "clear":
            for r in rooms:
                rooms[r].clear()
        elif message_from_client["type"] == "join_req":
            if not rooms[message_from_client["name"]]["password"] == message_from_client["password"]:
                await ws.send(json.dumps({"type":"create_resp", "content":"failed to joined room with name {}".format(message_from_client["name"])}))
            else:
                remove_ws_from_rooms(ws)
                rooms[message_from_client["name"]].append(ws)
                where_is[ws] = message_from_client["name"]
                await ws.send(json.dumps({"type":"create_resp", "content":"successfully joined room with name {}".format(message_from_client["name"])}))

        elif message_from_client["type"] == "create_req":
            if message_from_client["name"] not in list(rooms.keys()):
                remove_ws_from_rooms(ws)
                rooms[message_from_client["name"]] = {
                    "subs": [ws],
                    "password": message_from_client["password"]
                }#[ws]
                where_is[ws] = message_from_client["name"]
                await ws.send(json.dumps({"type":"create_resp", "content":"successfully created and joined room with name {}".format(message_from_client["name"])}))
        
        elif message_from_client["type"] == "leave_req":
            remove_ws_from_rooms(ws)

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



