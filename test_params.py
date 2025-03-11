import zmq
import json
import time

# zmq context and socket are initialized globally
path =  "storage.json"
context = zmq.Context()
print("Client A attempting to connect to server...")

socket = context.socket(zmq.REQ)

socket.connect("tcp://localhost:5555")

print(f"Sending a request...")


def get_news(username=None):
        with open(path, "r") as file:
                data = json.load(file)

        favorite_stocks = None
        if username:
                for entry in data:
                        if username in entry:
                                favorite_stocks = entry["fav"]
                                break
        else:
                while True:
                        username = input("Enter Username: ")
                        for entry in data:
                                if username in entry:
                                        favorite_stocks = entry["fav"]
                                        break

                        if favorite_stocks is None:
                                username = input("Username entered invalid please enter a valid username: ")
                                continue
                        break

        socket.send_json(favorite_stocks)

        news_list = socket.recv_json()
        with open("stock_news.json", "w") as outfile:
                json.dump(news_list, outfile, indent=4)

        return news_list


