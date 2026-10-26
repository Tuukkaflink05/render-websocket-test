import socket
import threading as th
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from gui import baseGui

serverIP = '127.0.0.1'
serverPORT = 20001
buffSize = 1024


class clientInfo:

    def __init__(self, conn):
        self._conn = conn
        self._username="NOTSET"

    def set_userName(self,usrnm):
        self._username=usrnm

def handle_client(conn, addr, GUIFrame):
    print("thread started")
    GUIFrame._add_table(addr)

    while True:
        try:
            data=conn.recv(buffSize)
        except OSError:
            handle_disconnect(addr, GUIFrame)
            return
        if not data:
            handle_disconnect(addr, GUIFrame)
            return
        else:
            msg=data.decode()
            conf,_,text = msg.partition(':')
            if (conf == 'C'):
                with client_lock:
                    txttosend=f"{client_list[addr]._username}: {text}"
                broadcast(addr,txttosend, GUIFrame)
            elif (conf == 'U') :
                with client_lock:
                    client_list[addr].set_userName(text)
                GUIFrame._update_table_name(addr,text)
            else:
                print("WARNING! handle_client: configuration prefix forgor from msg WARNING!! ")


def broadcast(senderaddr, msg, GUIFrame):
    global client_list
    print(msg)
    GUIFrame.add_text(msg)

    with client_lock:
        for addr in client_list.keys():
            if addr != senderaddr:
                pass
            client_list[addr]._conn.sendall(msg.encode())


def handle_disconnect(addr, GUIFrame):
    with client_lock:
        msg=f"{client_list[addr]._username} disconnected"
        client_list[addr]._conn.close()
        client_list.pop(addr)
    GUIFrame._delete_table_row(addr)
    broadcast(addr, msg, GUIFrame)

class serverGui(baseGui):

    def __init__(self, master):
        super().__init__(master)
        ttk.Label(self, text="SERVER", font="-size 16 -weight bold").pack()

        self._build_table()
        self._build_status()

    def _build_table(self):
        self.table=ttk.Tableview(
            self,
            coldata=["UserName", "IPaddress", "Port"],
            rowdata=[],
            iid_field="Port",
            searchable=False,
            bootstyle="primary",
            height=8
        )
        self.table.pack(fill=BOTH, expand=YES, pady=(16, 8))

    def _add_table(self,addr):
        with client_lock:
            username=client_list[addr]._username
        ipadr,port=addr

        self.table.insert_row(values=[username, ipadr,port])
        self._update_status()
        #print(self.table.get_row(iid=str(addr[1])))

    def _update_table_name(self,addr,name):
        ipadr,port=addr
        #print(self.table.get_row(iid=str(addr[1])))
        self.table.delete_row(iid=(str(addr[1])))
        self.table.insert_row(values=[name,ipadr,port])

        #print(self.table.get_row(iid=str(addr[1])))

    def _delete_table_row(self,addr):
        self.table.delete_row(iid=(str(addr[1])))
        self._update_status()

    def _update_status(self):
        with client_lock:
            count = len(client_list)
        self.status.configure(text=f"{count} users")


app = ttk.App(title="Server", theme="bootstrap-dark", size=(700, 750))
serverFrame=serverGui(app)

def run_server():
    while True:
        conn,addr=TCPSocket.accept()
        with client_lock:
            if not addr in client_list.keys():
                client_list[addr]=clientInfo(conn)
                thread = th.Thread(target=handle_client, args=(conn,addr,serverFrame,))
                thread.start()



TCPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
TCPSocket.bind((serverIP, serverPORT))
TCPSocket.listen()

print('TCP server up an listening')

client_list = {}
client_lock = th.Lock()

server_thread = th.Thread(target=run_server, daemon=True)
server_thread.start()
app.mainloop()