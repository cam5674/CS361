import zmq

# zmq context and socket are initialized globally
path = "storage.json"
context = zmq.Context()
print("Client attempting to connect to server...")

socket = context.socket(zmq.REQ)

socket.connect("tcp://localhost:5558")

print(f"Sending a request...")

info = {'username': "cam9999", 'stock': "vti"}

#TODO: Add edit email service
def delete_stock(user_info):

    socket.send_json(user_info)
    reply = socket.recv_string()

    print(reply)
    return reply


