import zmq
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from stocks import  get_data
load_dotenv()

email_me = os.getenv('email')
password = os.getenv('password')

context = zmq.Context()
socket = context.socket(zmq.REP)

socket.bind("tcp://*:5556")

# TODO: Add headers and cells to table
# TODO: Add recv after send_update

def send_confirmation(user_email):
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

    email = user_info['email']
    """
    Uses api to get all stocks
    print(email)
    fav_stocks = []
    favs = user_info['fav']
    for stock in favs:
        stock = get_data(stock)
        fav_stocks.append(stock)
    print(fav_stocks)
    """
    me = email_me


    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Stock Updates(ENTER DATE HERE)'
    msg['From'] = me
    msg['To'] = email

    # body of message
    html = """  
       <html>
       <style> table, th, td {border:1px solid black;}
       </style>
           <head></head>
           <body>
               <p>Hi!<br>
                   This is an email confirmation to confirm that you selected to receive daily updates for your stock favorites.<br>
               </p>
               <table style="width:100%">
               <tr>
                    <th style="border: 1px solid black;">Company</th>
                    <th style="border: 1px solid black;">Contact</th>
                    <th style="border: 1px solid black;">Country</th>
                </tr>
               <tr>
                    <td style="border: 1px solid black;">Alfreds Futterkiste</td>
                    <td style="border: 1px solid black;">Maria Anders</td>
                    <td style="border: 1px solid black;">Germany</td>
                </tr>
                <tr>
                    <td style="border: 1px solid black;">Centro comercial Moctezuma</td>
                    <td style="border: 1px solid black;">Francisco Chang</td>
                    <td style="border: 1px solid black;">Mexico</td>
                    </tr>
                </table>
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
    socket.send_string(f"Sent email to{email}")
    s.quit()


while True:
    email = socket.recv_string()
    print(f"received {email}")
    try:
        data = json.loads(email)
        print(data)
        print("Received JSON:")
        send_update(data)
    except json.JSONDecodeError:
        print(email)
        print("Received string")
        send_confirmation(email)


