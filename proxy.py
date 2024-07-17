#
#
#    Created By Sam Stockstrom for Fun
#    Project Started on June 25th 2024
#        Based on Terraria 1.4.4.9
#
#

import socket
import select
import traceback
import packet as p

class Proxy:
    def __init__(self, listen_ip: str, listen_port: int, server_ip: str, server_port: int, printout=True, print_packet=False, print_unknown=False):
        """A proxy server for Terraria 1.4.4.9

        Args:
            listen_ip (str): The ip you want to host the proxy on (127.0.0.1)
            listen_port (int): The port you want the proxy to listen on (2222)
            server_ip (str): The ip of the real server
            server_port (int): The port of the real server (7777)
            printout (bool, optional): _description_. Defaults to True.
            print_unknown (bool, optional): _description_. Defaults to False.
        """
        self.listen_ip = listen_ip
        self.listen_port = listen_port
        self.SERVER_IP = server_ip
        self.SERVER_PORT = server_port
        self.PRINTOUT = printout
        self.PRINT_PACKET = print_packet
        self.PRINT_UNKNOWN = print_unknown
        self.BUFF_SIZE = 4096  # TCP Buffer Size

    def process_packet(self, source: socket.socket, destination: socket.socket, packet: bytes):
        """Process Client and Server Packets"""
            
        if (self.PRINTOUT):
                    
            info = p.Packet(packet)
            
            if '- Unknown' in info.payload.description:
                if self.PRINT_UNKNOWN:
                    if self.PRINT_PACKET:
                        print("Packet:")
                        print(packet)
                    print("Payload information:")
                    print(vars(info.payload))
            else:
                if self.PRINT_PACKET:
                    print("Packet:")
                    print(packet)
                print("Payload information:")
                print(vars(info.payload))
                
        destination.send(packet)
        return packet
    
    def run_proxy(self):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((self.listen_ip, self.listen_port))
        listener.listen(1)

        while True:
            print("[-] Listening for client...")
            client_sock, addr = listener.accept()
            print("[+] Client Connected:", addr)

            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.connect((self.SERVER_IP, self.SERVER_PORT))

            sockets = [client_sock, server_sock]
            wait_for_client = False
            
            try:
                while True:
                    readable, _, _ = select.select(sockets, [], [])
                    
                    for sock in readable:
                        if sock == client_sock:
                            data = client_sock.recv(self.BUFF_SIZE)
                            
                            if not data:
                                raise Exception("Client disconnected")
                            
                            self.process_packet(client_sock, server_sock, data)
                            wait_for_client = False
                            
                        elif sock == server_sock and not wait_for_client:
                            data = server_sock.recv(self.BUFF_SIZE)
                            
                            if p.Packet(data).id == '025':
                                readable.remove(server_sock)
                                
                            if not data:
                                raise Exception("Server disconnected")
                            
                            response = self.process_packet(server_sock, client_sock, data)
                            
                            if response == b'\x03\x00%':
                                wait_for_client = True
                                print("Received Password Request. Waiting for next client packet before reading from server.")
                            
            except Exception as e:
                if "Client disconnected" not in str(e):
                    exc_obj = e
            finally:
                try:
                    tb_str = ''.join(traceback.format_exception(None, exc_obj, exc_obj.__traceback__))
                    print(tb_str)
                except:
                    pass  # no errors to report
                
                print("[+] Closing connections")
                client_sock.close()
                server_sock.close()

if __name__ == "__main__":
    proxy = Proxy('127.0.0.1', 2222, '127.0.0.1', 7777, print_packet=True)
    proxy.run_proxy()