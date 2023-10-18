import socket
import consts

class Client:
    def __init__(self):           
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  
        self.serverAddr: tuple[str, int]


    def connect(self, addr:str, port:int):
        self.serverAddr = (addr, port)


    def send(self, data):
        self.socket.sendto(str.encode(data, 'utf-8'), self.serverAddr)


    def recv(self) -> str:
        msg, addrr = self.socket.recvfrom(consts.BUFFER_SIZE)
        return msg.decode('utf-8')