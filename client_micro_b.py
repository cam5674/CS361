import zmq
import json
import time

# zmq context and socket are initialized globally
path =  "storage.json"
context = zmq.Context()
print("Client attempting to connect to server...")

socket = context.socket(zmq.REQ)

socket.connect("tcp://localhost:5556")

print(f"Sending a request...")


# check to see if user clicked yes for email
# put in json {"email": john@gmail}
json_test = {"email": "john@gmail"}

json_string = json.dumps(json_test)

#TODO: Add sleep or time to wake up client and server
def send_email(email):

    socket.send_string(email)
    recv = socket.recv_string()
    print(f"Received confirmation {recv}")



def main():
    while True:
        with open("storage.json", "r") as f:
            data = json.load(f)
            for entry in data:
                if entry["email service"] == "1":

                    email_favs = {"email": entry["email"], "fav": entry["fav"] }
                    string_email_favs = json.dumps(email_favs)
                    print(email_favs)
                    send_email(string_email_favs)
                    print(f"Sending email{email_favs}")
                    #send_email(email)
        break




if __name__ == "__main__":
    main()


