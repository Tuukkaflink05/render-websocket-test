#!/usr/bin/env python

import asyncio

from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosedOK
from websockets import *

class clientInfo:

    def __init__(self, websocket):
        self._websocket = websocket
        self._username="NOTSET"

    def set_userName(self,usrnm):
        self._username=usrnm

async def handler(websocket):
    port = websocket.remote_address[2]
    print("user connected from port ", port)
    connections.append(websocket)
    client_list[port] = clientInfo(websocket)
    while True:
            message = await websocket.recv()

            conf,_,text = message.partition(':')
            if (conf == 'C'):
                txttosend=f"{client_list[port]._username}: {text}"
                broadcast(connections,txttosend)
            elif (conf == 'U') :
                client_list[port].set_userName(text)

            else:
                print("WARNING! handle_client: configuration prefix forgor from msg WARNING!! ")


client_list = {}
connections = []

async def main():
    server = await serve(handler, "", 8001)
    await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())