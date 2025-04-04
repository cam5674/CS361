import zmq
import json
from datetime import datetime, timedelta
import time


# zmq context and socket are initialized globally
path = "storage.json"
context = zmq.Context()
print("Client B attempting to connect to server...")

socket = context.socket(zmq.REQ)

socket.connect("tcp://localhost:5559")

print(f"Sending a request...")


# check to see if user clicked yes for email
# put in json {"email": john@gmail}
json_test = {"email": "john@gmail"}

json_string = json.dumps(json_test)


def send_email(email: str):
    """
    Sends email/emails to the server

    :param email: Email or emails to be sent to the server
    :return:
    """
    print(f"Sent{email}")
    socket.send_string(email)
    recv = socket.recv_string()
    print(f"Received confirmation {recv}")


def check_time():
    """
    Checks the current time and the time for the client to send the emails
    to the server.
    :return:
    """

    target_time = datetime.now().replace(hour=16, minute=19, second=0)

    while True:

        now = datetime.now()
        print(f"current time: {now}")
        print(f"target time: {target_time}")
        sleep_time = target_time - now

        # margin of error of 1 minute
        if sleep_time < timedelta(minutes=-1):
            target_time = target_time + timedelta(days=1)
            print("Add day")
        else:
            # if less than a minute remaining send email
            print("soon")
            print(sleep_time)
            if sleep_time < timedelta(minutes=1):
                return True
            else:
                sec = sleep_time.total_seconds()
                print(sec)
                time.sleep(sec)


def main():

    # loop through file and put json in a string to send emails and
    # favorite stocks to server
    while True:
        if check_time():
            with open("storage.json", "r") as f:
                data = json.load(f)
                for entry in data:
                    if entry["email service"] == "1":

                        email_favs = {"email": entry["email"], "fav": entry["fav"]}
                        string_email_favs = json.dumps(email_favs)
                        print(email_favs)
                        send_email(string_email_favs)
                        print(f"Sending email{email_favs}")
                        #send_email(email)
            break


if __name__ == "__main__":
    main()