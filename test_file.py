import sys

from rich.console import Console
from rich.table import Table
import requests


key = "f908849cbe14794c8cdce604c8fd547d098d2af1"


def get_data(stock: str):
    """
    list with a dictionary:
    [{}]
    :param stock:
    :return:
    """
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.get(f"https://api.tiingo.com/iex/?tickers={stock}&token={key}",headers=headers)
    data = response.json()

    return data


def pretty_print(stock):
    """

    :param stock: [ [{}], [{}] ]
    :return:
    """
    table = Table("Ticker", style="magenta")
    table.add_column("Last Price", justify="right", style="green")
    for x in range(0, len(stock)):
        # unpack
        stock_info = stock[x]
        # Get the dictionary in the list and print out a row
        table.add_row(stock_info[0]['ticker'], str(stock_info[0]['last']))

    return table


def reset_table():
    table = Table("Ticker", style="magenta")
    table.add_column("Last Price", justify="right", style="green")


def menu():
    print("Welcome!\n")
    stock_list = []
    while True:
        stock = str(input("Look up stock or click 1 to exit: "))

        if stock == "1":
            print("Thank you for stopping by!")
            break
        else:
            stock = get_data(stock)
            stock_list.append(stock)
            table = pretty_print(stock_list)
            console = Console(color_system="windows")
            console.print(table)




menu()
