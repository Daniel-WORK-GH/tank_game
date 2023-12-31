import socket
import sys
import consts
from .server import get_current_ip

class Client:
    def __init__(self):           
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  
        self.serverAddr: tuple[str, int]
        # self.socket.bind(("0.0.0.0", consts.CLIENT_PORT))
        self.socket.settimeout(1)


    def connect(self, addr:str, port:int):
        self.serverAddr = (addr, port)
        

    def send(self, data):
        try:
            self.socket.sendto(str.encode(data, 'utf-8'), self.serverAddr)
        except socket.timeout as e:
            print(e)


    def recv(self) -> str:
        try:
            msg, addrr = self.socket.recvfrom(consts.BUFFER_SIZE)
            return msg.decode('utf-8')
        except socket.timeout:
            exit()
        except Exception as e:
            if e.args[0] == 10054:
                exit()
            print(e.args[0])