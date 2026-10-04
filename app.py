#!/usr/bin/env python

import asyncio

from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed
from websockets import *

from http import HTTPStatus
from pathlib import Path

import json

class clientInfo:

    def __init__(self, websocket):
        self._websocket = websocket
        self._username="NOTSET"

    def set_userName(self,usrnm):
        self._username=usrnm

DASHBOARD_HTML = (Path(__file__).parent / "index.html").read_text(encoding="utf-8")
DASHBOARD_JS = (Path(__file__).parent / "index.js").read_text(encoding="utf-8")

admin_ws = None

def getAdminInfo():
    payload = json.dumps({
        "users":[
            {"name":info._username}
            for info in client_list.values()
        ],
    })
    return payload

async def notify_admin():
    if admin_ws == None:
        return

    await admin_ws.send(getAdminInfo())

async def process_request(connection,request):
    if request.path == "/admin":
        response = connection.respond(HTTPStatus.OK, DASHBOARD_HTML)
        del response.headers["Content-Type"]
        response.headers["Content-Type"] = "text/html; charset=utf-8"
        return response
    elif request.path == "/index.js":
        response = connection.respond(HTTPStatus.OK, DASHBOARD_JS)
        del response.headers["Content-Type"]
        response.headers["Content-Type"] = "text/javascript; charset=utf-8"
        return response
    return None


async def handler(websocket):
    client_list[websocket] = clientInfo(websocket)
    print("user connected")
    broadcast(client_list.keys(),"user connected")

    while True:
        try:
            message = await websocket.recv()

            conf,_,text = message.partition(':')
            if (conf == 'C'):
                txttosend=f"{client_list[websocket]._username}: {text}"
                print(txttosend)
                broadcast(client_list.keys(),txttosend)
            elif (conf == 'U') :
                client_list[websocket].set_userName(text)
                await notify_admin()
            elif (conf == 'A'):
                global admin_ws
                print(text)
                admin_ws = websocket
                await notify_admin()
                print(client_list[websocket]._username)

            else:
                print("WARNING! handle_client: configuration prefix forgor from msg WARNING!! ")

        except ConnectionClosed:
            info = client_list.pop(websocket,None)
            if websocket in connections:
                connections.remove(websocket)
            txttosend=f"{info._username} Disconnected"
            print(txttosend)
            broadcast(client_list.keys(),txttosend)
            await notify_admin()
            break

client_list = {}
connections = []

async def main():
    server = await serve(handler, "0.0.0.0", 10000,process_request=process_request)
    await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())