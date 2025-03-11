import json

import zmq


# server
context = zmq.Context()
socket = context.socket(zmq.REP)

socket.bind("tcp://*:5554")


def replace_stock(user_info):

    name = user_info['username']
    stock = user_info['stock']

    with open("storage.json", "r") as f:
        data = json.load(f)
        try:
            for info in data:
                for key,values in info.items():
                    if key == name:
                        info["fav"].remove(stock)
        except ValueError:
            return False

        with open("storage.json", "w") as file:
            json.dump(data, file, indent=4)

    return True


while True:
    data = socket.recv_json()
    print("Received Request...")
    if replace_stock(data):
        socket.send_string("Deleted stock")
    else:
        socket.send_string("Stock not in favorites!")



