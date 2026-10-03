#!/usr/bin/env python

import asyncio

from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosedOK
from websockets import *

from http import HTTPStatus
from pathlib import Path

class clientInfo:

    def __init__(self, websocket):
        self._websocket = websocket
        self._username="NOTSET"

    def set_userName(self,usrnm):
        self._username=usrnm

DASHBOARD_HTML = (Path(__file__).parent / "index.html").read_text(encoding="utf-8")

async def process_request(connection,request):
    if request.path == "/":
        response = connection.respond(HTTPStatus.OK, DASHBOARD_HTML)
        del response.headers["Content-Type"]
        response.headers["Content-Type"] = "text/html; charset=utf-8"
        return response
    return None


async def handler(websocket):

    print("user connected from port ")
    connections.append(websocket)
    client_list[websocket] = clientInfo(websocket)
    while True:
            message = await websocket.recv()

            conf,_,text = message.partition(':')
            if (conf == 'C'):
                txttosend=f"{client_list[websocket]._username}: {text}"
                broadcast(connections,txttosend)
            elif (conf == 'U') :
                client_list[websocket].set_userName(text)

            else:
                print("WARNING! handle_client: configuration prefix forgor from msg WARNING!! ")


client_list = {}
connections = []

async def main():
    server = await serve(handler, "0.0.0.0", 10000,process_request=process_request)
    await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())