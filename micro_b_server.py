import zmq
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from stocks import get_data
from datetime import datetime, timedelta
import time


load_dotenv()
email_me = os.getenv('email')
password = os.getenv('password')

# server
context = zmq.Context()
socket = context.socket(zmq.REP)

socket.bind("tcp://*:5557")


def send_confirmation(user_email):
    """
    Sends a confirmation email to a single user.
    :param user_email: email receiver
    :return:
    """

    me = email_me

    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Email confirmation'
    msg['From'] = me
    msg['To'] = user_email

    # body of message
    html = """  
    <html>
        <head></head>
        <body>
            <p>Hi!<br>
                This is an email confirmation to confirm that you selected to receive daily updates for your stock favorites.<br>
            </p>
        </body>
    </html>  
    """

    # Record the MIME types of both parts
    text = MIMEText(html, 'html')
    msg.attach(text)

    # send message
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(email_me, password)
    s.sendmail(me, email, msg.as_string())
    socket.send_string(f"Sent email to{user_email}")
    s.quit()


def send_update(user_info):
    """
    Sends a table to a single user or multiple users.
    :param user_info: JSON of emails and favorite stocks
    :return:
    """

    email = user_info['email']

    # Uses api to get all stock prices
    fav_stocks = []
    favs = user_info['fav']
    for stock in favs:
        stock = get_data(stock)
        fav_stocks.append(stock)

    # initialize array to store dynamic table rows
    rows = []

    for x in range(0, len(fav_stocks)):
        # unpack
        stock_info = fav_stocks[x]

        html_rows = f"""
            <tr>
                    <td style="border: 1px solid black;">{stock_info[0]['ticker']}</td>
                    <td style="border: 1px solid black;">${stock_info[0]['open']}</td>
                    <td style="border: 1px solid black;">${stock_info[0]['high']}</td>
                    <td style="border: 1px solid black;">${stock_info[0]['low']}</td>
                    <td style="border: 1px solid black;">${stock_info[0]['tngoLast']}</td>
                    <td style="border: 1px solid black;">{stock_info[0]['volume']}</td>
            </tr>
        
        """
        rows.append(html_rows)

    # join rows together to be used for html later
    rows = ' '.join(rows)
    me = email_me

    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Stock Updates'
    msg['From'] = me
    msg['To'] = email

    # body of message
    html = """  
       <html>
           <head></head>
           <body>
               <p>Hi!<br>
                   The bottom table displays your current holdings.<br>
               </p>
               <table style="width:100%; border-collapse: collapse;">
               <tr>
                    <th style="border: 1px solid black;">Ticker</th>
                    <th style="border: 1px solid black;">Open</th>
                    <th style="border: 1px solid black;">High</th>
                    <th style="border: 1px solid black;">Low</th>
                    <th style="border: 1px solid black;">Last</th>
                    <th style="border: 1px solid black;">Volume</th>
                </tr>
                {{placeholder}}
              
                </table>
           </body>
       </html>  
       """
    # add rows to html table
    html = html.replace("{{placeholder}}", rows)

    # Record the MIME types of both parts
    text = MIMEText(html, 'html')
    msg.attach(text)

    # send message
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(email_me, password)
    s.sendmail(me, email, msg.as_string())
    socket.send_string(f"Sent email to{email}")
    s.quit()


def check_time():

    target_time = datetime.now().replace(hour=16, minute=19, second=0)

    while True:

        now = datetime.now()
        print(f"current time{now}")
        print(f"target time{target_time}")
        sleep_time = target_time - now
        print(f"Sleep time{sleep_time}")
        print(type(sleep_time))
        if sleep_time < timedelta(minutes=-1):
            target_time = target_time + timedelta(days=1)
            print("Add day")
        else:
            print("soon")
            print(sleep_time)
            if sleep_time < timedelta(minutes=2):
                return True
            else:
                sec = sleep_time.total_seconds()
                print(sec)
                time.sleep(sec)


while True:

    # check if it is the time
    print("Ready to do work!")
    email = socket.recv_string()
    print(f"received {email}")

    # check request type(single email vs JSON of emails and favorite stocks
    try:
        data = json.loads(email)
        # check if it is the correct time to receive request from client
        if check_time():
            print(data)
            print("Received JSON:")
            send_update(data)
    except json.JSONDecodeError:
        print(email)
        print("Received string")
        send_confirmation(email)
