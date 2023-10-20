import socket
import threading
import consts
from datetime import datetime
from mapobjects.player import Player
from . import converter


def get_current_hostname() -> str:
    return socket.gethostname()


def get_current_ip() -> str:
    hostname = get_current_hostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


class Server:
    def __init__(self, addr, port):
        self.addr = addr
        self.port = port

        self.printwt('Creating socket...', True)
        self.printwt('Socket created', True)
        # bind server to the address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        self.printwt(f'Binding server to {self.addr}:{self.port}...', True)
        self.printwt(f'Server binded to {self.addr}:{self.port}', True)
        self.sock.bind((addr, port))

        self.players:dict[str, Player] = {}


    def printwt(self, msg, forceprint = False):
        if consts.SERVER_DEBUG_MSGS or forceprint:
            current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f'[{current_date_time}] {msg}')


    def update_on_request(self, data):
        player = converter.json_to_player(data)

        if player != None:
            self.players[player.name] = player


    def handle_request(self, data, client_address):
        data = data.decode('utf-8')

        forceprint = False
        if consts.SERVER_OTHERS_DEBUG_MSGS:
            forceprint = client_address[0] != "127.0.0.1"

        self.printwt(f'[ REQUEST from {client_address} ]: {data}', forceprint)

        self.update_on_request(data)

        resp = converter.player_list_to_json(self.players.values())
        self.printwt(f'[ RESPONSE to {client_address} ]', forceprint)
        self.sock.sendto(resp.encode('utf-8'), client_address)


    def wait_for_client(self):
        try:
            data, client_address = self.sock.recvfrom(1024)
            self.handle_request(data, client_address)
        except OSError as err:
            self.printwt(err)


    def shutdown_server(self):
        self.printwt('Shutting down server...')
        self.sock.close()


class ThreadServer:
    def __init__(self, addr, port) -> None:
        self.server = Server(addr, port)
        self.thread = threading.Thread(target = self.server_loop)
        self.thread.daemon = True
        self.isrunning = False


    def server_loop(self):
        if self.isrunning == False: return

        try:
            while True and self.isrunning: 
                self.server.wait_for_client()   
        except KeyboardInterrupt:
            self.server.shutdown_server()

        if not self.isrunning:
            self.server.shutdown_server()


    def start(self):
        self.isrunning = True
        self.thread.start()


    def stop(self):
        self.isrunning = False    
        self.server.shutdown_server()