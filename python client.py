import threading
import socket
import tkinter as tk

address = None
nick = None

class connectedGUI(object):
    def __init__(self):
        global address, nick
        self.address = address
        self.nick = nick
        self.connect()
        self.interface()

    def connect(self):
        self.sock = socket.socket()
        self.sock.connect((self.address, 9339))
        self.sock.send(bytes(self.nick, 'UTF-8'))
        self.thread = threading.Thread(target=lambda: self.reception_handler())
        self.thread.start()

    def interface(self):
        self.window = tk.Tk(screenName="Multi-Plexing-Server Client")
        window = self.window
        window.protocol("WM_DELETE_WINDOW", self.close_func)

        messages = tk.Frame(window, bd=2, relief=tk.SUNKEN)
        textbar = tk.Frame(window, bd=2, relief=tk.SUNKEN)

        messages.grid(row=0, padx=5, pady=5)
        textbar.grid(row=1, padx=5, pady=5)

        messages_scroll = tk.Scrollbar(messages)
        messages_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.messages_body = tk.Text(messages)
        self.messages_body.pack()
        self.messages_body.config(yscrollcommand=messages_scroll.set)
        messages_scroll.config(command=self.messages_body.yview)
        self.textbar_message = tk.Entry(textbar, width=74)
        self.textbar_message.grid(row=0, column=0)
        textbar_send = tk.Button(textbar, text="Send", command=self.send)
        textbar_send.grid(row=0, column=1)

        window.mainloop()

    def send(self):
        text = self.textbar_message.get()
        try:
            self.sock.send(bytes(text, "UTF-8"))
            self.textbar_message.delete(0, len(text))
        except:
            pass

    def reception_handler(self):
        while True:
            name = self.sock.recv(32)
            message = self.sock.recv(1024)
            self.messages_body.insert(tk.END, str(name, 'UTF-8')+": "+str(message, 'UTF-8')+"\n")

    def close_func(self):
        self.sock.close()
        quit(code=0)

class setupGUI(object):
    def __init__(self):
        self.setup()
    
    def setup_button_handler(self):
        global address, nick
        address = self.address_entry.get()
        nick = self.nick_entry.get()
        self.window.destroy()
        connectedGUI()
    
    def setup(self):
        self.window = tk.Tk(screenName="MPS Client Connect")
        window = self.window
        window.protocol("WM_DELETE_WINDOW", self.close_func)
        
        intro = tk.Frame(window, bd=2, relief=tk.SUNKEN)
        address = tk.Frame(window, bd=2, relief=tk.SUNKEN)
        nick = tk.Frame(window, bd=2, relief=tk.SUNKEN)
        connect = tk.Frame(window, bd=2, relief=tk.SUNKEN)

        intro.grid(row=0,padx=5,pady=5)
        address.grid(row=1,padx=5,pady=5)
        nick.grid(row=2,padx=5,pady=5)
        connect.grid(row=3,padx=5,pady=5)
    
        intro_label = tk.Label(intro, text="Please enter a server address and nickname.").grid(row=0,column=0)
        address_label = tk.Label(address, text="Server Address : ").grid(row=0,column=0)
        self.address_entry = tk.Entry(address)
        self.address_entry.grid(row=0,column=1)
        nick_label = tk.Label(nick, text="Nickname : ").grid(row=0,column=0)
        self.nick_entry = tk.Entry(nick)
        self.nick_entry.grid(row=0,column=1)
        connect_button = tk.Button(connect, text="Connect", command=self.setup_button_handler).grid(row=0,column=0)

    def close_func(self):
        quit(code=0)
#runs the setupGUI to get info from user
setupGUI()




