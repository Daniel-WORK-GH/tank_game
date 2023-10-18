import socket
import sys
import consts
from server import get_current_ip

class Client:
    def __init__(self):           
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  
        self.serverAddr: tuple[str, int]
        self.socket.bind(("", consts.SERVER_PORT + 1))
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
        except Exception as e:
            print(e)