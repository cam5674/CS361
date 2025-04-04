import zmq

# zmq context and socket are initialized globally
path = "storage.json"
context = zmq.Context()
print("Client C attempting to connect to server...")

socket = context.socket(zmq.REQ)

socket.connect("tcp://localhost:5554")

print(f"Sending a request...")

# example: info = {'username': "cam9999", 'stock': "vti"}


def delete_stock(user_info):
    """
    # example: info = {'username': "cam9999", 'stock': "vti"}
    :param user_info:
    :return:
    """

    socket.send_json(user_info)
    reply = socket.recv_string()
    print(reply)

    return reply


