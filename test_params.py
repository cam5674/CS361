import zmq
import json


path =  "C:\\Users\camer\\Python_crash_course\\CS361\\storage.json"
context = zmq.Context()
print("Client attempting to connect to server...")

socket = context.socket(zmq.REQ)

socket.connect("tcp://localhost:5555")

print(f"Sending a request...")

with open(path, "r") as file:
        data = json.load(file)

favorite_stocks = None

while True:
        # will need to be a function
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
print(news_list)
with open("stock_news.json", "w") as outfile:
        json.dump(news_list, outfile, indent=4)

print("news articles saved to stock_news.json")


