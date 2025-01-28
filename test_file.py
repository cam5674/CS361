import sys

import requests


key = "f908849cbe14794c8cdce604c8fd547d098d2af1"
headers = {
    'Content-Type': 'application/json'
}
response = requests.get(
    f"https://api.tiingo.com/iex/?tickers=apple&token={key}",
    headers=headers)
data = response.json()
print(data)
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


def menu():
    print("Welcome!\n")
    while True:
        stock = str(input("Look up stock or click 1 to exit: "))

        if stock == 1:
            print("Thank you for stopping by!")
            break
        else:
            data = get_data(stock)
            print(data)
            print(data[0]['last'])


menu()
