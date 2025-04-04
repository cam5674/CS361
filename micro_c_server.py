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
                        profile = info
        except ValueError:
            return False

        with open("storage.json", "w") as file:
            json.dump(data, file, indent=4)

    print(profile)
    return True, profile


while True:
    data = socket.recv_json()
    print("Received Request...")
    check = replace_stock(data)
    if not check:
        print("False")
        socket.send_string("0")
    else:
        socket.send_json(check[1])



