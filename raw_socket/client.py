import socket
import threading as th
import sys
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from gui import baseGui

serverIP = '127.0.0.1'
serverPORT = 20001
buffSize = 1024

if len(sys.argv) > 1:
    userName = sys.argv[1]
else:
    userName = input("enter username: ")

def handle_disconnect(TCP_socket):

    print("Disconnecting")
    TCP_socket.close()

def listen(TCP_socket,ClientGUI):
    while True:
        try:
            data = TCP_socket.recv(buffSize)
        except OSError:
            return
        if not data:
            return
        msg=data.decode()
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
        global TCPSocket
        msg=self.entryTxt.get()
        msg = f"C:{msg}"
        if not msg:
            #there is no text in entry box no need to do anything
            return
        bytestosend = str.encode(msg)
        TCPSocket.sendall(bytestosend)
        self.entryTxt.set("")


app = ttk.App(title="Client", theme="bootstrap-dark", size=(700, 750))
clientFrame=Client(app)

TCPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
TCPSocket.connect((serverIP,serverPORT))
print(TCPSocket)

msg = f"U:{userName}"
bytestosend = msg.encode()
TCPSocket.sendall(bytestosend)

t = th.Thread(target=listen, args=(TCPSocket,clientFrame,))
t.start()
app.mainloop()
t.join()
