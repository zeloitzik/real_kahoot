import socket
import select
from inputimeout import inputimeout 


class PlayerClient:
    def __init__(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port

    def connect(self):
        self.socket.connect((self.ip, self.port))
        name = input("Enter your name: ")
        self.socket.send(f"{name} <PLR>".encode())

    def play(self):
        """Use `select` to wait for either user input or a message from the server."""
        while True:
            readable, _, _ = select.select([self.socket], [self.socket], [])
            for source in readable:
                if source == self.socket:  
                    message = self.socket.recv(1024).decode()
                    if(message != "Game has ended"):
                        print(message) 
                        try:
                            answer = str(inputimeout(prompt="Enter your answer: ", timeout=5))
                            self.socket.send(answer.encode())
                        except Exception:
                            print("Your time is over!")
                            self.socket.send("".encode())
                        output = self.socket.recv(1024).decode()
                        print(output)
                    else:
                        print(message)

if __name__ == "__main__":
    player = PlayerClient("127.0.0.1", 12345)
    player.connect()
    player.play()
