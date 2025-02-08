from socket import *
import time

class admin_client:
    def __init__(self, ip, port):
        self.soc = socket()
        self.ip = ip    
        self.port = port

    def connect(self):
        self.soc.connect((self.ip, self.port))
        self.soc.send("Start the game <STA>".encode())
        print("Admin connected. Waiting for players...")

    def ask_questions(self):
        with open("question_answer.txt", "r") as file:
            questions = file.readlines()

        for question in questions:
            formatted_question = question.strip() + ",<QST>"
            self.soc.send(formatted_question.encode())
            print(f"Sent: {question.strip()}")
            time.sleep(5)
        self.soc.send("<END>".encode())    

if __name__ == "__main__":
    admin = admin_client("127.0.0.1", 12345)
    admin.connect()
    time.sleep(20)  # Give players time to join
    admin.ask_questions()
