from socket import *
import select

class my_server:
    def __init__(self, port):
        self.port = port
        self.server_socket = socket()
        self.server_socket.bind(('', self.port))
        self.server_socket.listen(5)
        self.admin = None
        self.players = {}
        self.points = {}
        self.question = None
        self.isOver = False
        self.inputs = [self.server_socket]

    def server_listen(self):
        while True:
            rlist, wlist, _ = select.select(self.inputs, [], [])
            for sock in rlist:
                if sock == self.server_socket:
                    client, addr = self.server_socket.accept()
                    print(f"New connection")
                    self.inputs.append(client)
                else:
                    try:
                        self.handle_client(sock)
                    except (ConnectionResetError, BrokenPipeError, OSError):
                        print(f"Removing disconnected client {self.players.get(sock, 'Unknown')}")
                        if sock in self.players:
                            del self.players[sock]
                        self.inputs.remove(sock)
                        sock.close()

        self.server_socket.close()

    def handle_client(self, client):
        try:
            message = client.recv(1024).decode()
            print(message)
            if message.endswith("<STA>"):
                if self.admin is None:
                    self.admin = client
                    client.send("New admin registered".encode())
            elif message.endswith("<PLR>"):
                player_name = message[:-5]
                self.players[client] = player_name
                self.points[client] = 0
                print(f"Player {player_name} added")
            elif message.endswith("<QST>") and client == self.admin:
                self.question = message
                self.brodcast_question()
            elif message.endswith("<END>") and client == self.admin:
                for player in self.players:
                    player.send("Game has ended".encode())
            elif client in self.players:
                
                if message is not None: 
                    print(message) 
                    self.handle_answer(client, message)  
                else:
                    print("Received empty message.")
            else:
                client.send("Invalid Input. Start the game".encode())
        except:
            print(f"Client {self.players[client]} forcibly closed the connection")
            self.inputs.remove(client)
            client.close()

    def brodcast_question(self):
        self.answer_order = []
        self.question = self.question.split(",")
        question_gui = f"{self.question[0]}\n{self.question[1]}  {self.question[2]}\n{self.question[3]}  {self.question[4]}"
        
        for player in self.players:
            player.send(f"Question: {question_gui}".encode())

    def handle_answer(self, client, answer):
        self.answer_order = []
        print(self.question)
        correct_answer = self.question[-2]
        print(f"Correct answer: {correct_answer}, answer: {answer}")
        print(correct_answer)
        if answer.strip().lower() == correct_answer.strip().lower():
            if len(self.answer_order) == 0:
                self.points[client] += 10
                self.answer_order.append(1)
            elif len(self.answer_order) == 1:
                self.points[client] += 5
                self.answer_order.append(1)
            elif len(self.answer_order) == 2:
                self.points[client] += 3
                self.answer_order.append(1)
        client.send(f"Your points: {self.points[client]}\n".encode())

    def end_game(self):
        self.isOver = True           
        for i in self.players:
            i.close()

def main():
    server = my_server(12345)
    server.server_listen()

main()
