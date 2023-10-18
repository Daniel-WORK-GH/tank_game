import socket
import consts

class Client:
    def __init__(self):           
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)  
        self.serverAddr: tuple[str, int]


    def connect(self, addr:str, port:int):
        self.serverAddr = (addr, port)


    def send(self, data):
        self.socket.settimeout(0.01)
        
        try:
            self.socket.sendto(str.encode(data, 'utf-8'), self.serverAddr)
        except socket.timeout as e:
            print(e)



    def recv(self) -> str:
        msg, addrr = self.socket.recvfrom(consts.BUFFER_SIZE)
        return msg.decode('utf-8')