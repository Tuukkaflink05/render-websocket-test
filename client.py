import threading as th
import sys
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from websockets.sync.client import connect

from raw_socket.gui import baseGui

uri = "ws://localhost:10000/chat"
#uri = "wss://websockets-echo-t90c.onrender.com/chat"

if len(sys.argv) > 1:
    userName = sys.argv[1]
else:
    userName = input("enter username: ")

def handle_disconnect(TCP_socket):

    print("Disconnecting")
    TCP_socket.close()

def listen(websocket,ClientGUI):
    while True:
        msg = websocket.recv()
        ClientGUI.add_text(msg)
        print(msg)


class Client(baseGui):

    def __init__(self, master):
        super().__init__(master)
        ttk.Label(self, text="CLIENT", font="-size 16 -weight bold").pack()

        self.entryTxt=ttk.StringVar()
        #self._build_status()
        self._build_entry()


    def _update_status(self):
      pass

    def _build_entry(self):
        self.entry=ttk.Entry(self,textvariable=self.entryTxt)
        self.entry.pack(fill="x",padx=20, pady=10)
        self.entry.bind("<Return>", self.returnpressed)

        sendBtn=ttk.Button(self.entry,icon="arrow-right-short",command=self.send_chat, padding=10, icon_only="true", cursor="hand2")
        sendBtn.pack(side="right")
        sendBtn.bind("<Return>", self.returnpressed)


    def returnpressed(self,event):
        self.send_chat()


    def send_chat(self):
        global websocket
        msg=self.entryTxt.get()
        if not msg:
            #there is no text in entry box no need to do anything
            return
        message = f"C:{msg}"

        websocket.send(message)
        self.entryTxt.set("")


app = ttk.App(title="Client", theme="bootstrap-dark", size=(700, 750))
clientFrame=Client(app)

with connect(uri) as websocket:

    msg = f"U:{userName}"
    websocket.send(msg)

    t = th.Thread(target=listen, args=(websocket,clientFrame,), daemon=True)
    t.start()

    app.mainloop()

t.join()

