import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class baseGui(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, padding=16)
        self.pack(fill=BOTH, expand=YES)
        self._build_text()


    def _build_text(self):
        self.text = ttk.Text(self, width=40, height=8,state="disabled")
        self.text.pack(fill="both", expand=True, padx=10, pady=10)




    def add_text(self, txt):
        self.text.configure(state="normal")
        self.text.insert("end", f"{txt} \n")
        self.text.configure(state="disabled")


    def _build_status(self):
        self.status = ttk.Label(self, text="0 users", bootstyle="secondary")
        self.status.pack(fill=X)

    def _update_status(self):
        pass