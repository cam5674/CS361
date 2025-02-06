import json

from rich.console import Console
from rich.table import Table
import requests
import yfinance as yf
import cred
from profile import Profile


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
    response = requests.get(f"https://api.tiingo.com/iex/?tickers={stock}&token={cred.key}",headers=headers)
    data = response.json()
    print(data)
    return data


def get_news(ticker: str):
    news = yf.Search(f"{ticker}", news_count=5).news
    print(news)
    if news == []:
        print("No news found")
    return news


def pretty_print(stock):
    """

    :param stock: [ [{}], [{}] ]
    :return:
    """

    table = Table("Ticker", style="magenta")
    table.add_column("Open", justify="right", style="white")
    table.add_column("High", justify="right", style="white")
    table.add_column("Low", justify="right", style="white")
    table.add_column("Last", justify="right", style="white")
    table.add_column("Percentage Change(1d)", justify="right", style="white")
    table.add_column("Volume", justify="right", style="white")

    for x in range(0, len(stock)):
        # unpack
        stock_info = stock[x]

        # check daily percentage change
        percentage_change = round(((stock_info[0]['tngoLast'] - stock_info[0]['open']) / stock_info[0]['tngoLast']) * 100, 2)

        # check if positive or negative
        if percentage_change >= 0:
            percentage_change = f'[green]{percentage_change}%[/green]'
        else:
            percentage_change = f'[red]{percentage_change}%[/red]'
        # Get the dictionary in the list and print out a row
        table.add_row(stock_info[0]['ticker'], str(stock_info[0]['open']),str(stock_info[0]['high']), str(stock_info[0]['low']),str(stock_info[0]['tngoLast']), percentage_change, str(stock_info[0]['volume']))

    return table


def reset_table():
    table = Table("Ticker", style="magenta")
    table.add_column("Last Price", justify="right", style="white")
    table.add_column("High", justify="right", style="white")
    table.add_column("Low", justify="right", style="white")
    table.add_column("Open", justify="right", style="white")
    table.add_column("Volume", justify="right", style="white")


def check_username(name:str):
    """
    Checks if username is in storage file.
    :param name:
    :return:
    """

    with open("storage.json", "r") as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            return False
        for dict in data:
            for key in dict.items():
                print(key)
                if key[0] == name:
                    f.close()
                    return True, dict
        else:
            f.close()
            return False


def create_profile():
    """
    Creates a new profile.

    :return: New profile class object profilec
    """
    while True:
        name = str(input("Enter a username: "))
        if check_username(name):
            print("Username is taken. Please enter another username.")
            continue
        break

    profile = Profile(name)

    return profile


def new_profile(profile):
    with open("storage.json", "a") as f:
        json.dump(profile, f, indent=5)


def save_profile(profiles: dict):
    """
    Opens storage.json and adds a new profile to the json file.
    [{}]
    :param profiles:
    :return:
    """
    with open("storage.json", "r+") as file:
        try:
            data = json.load(file)
        except json.decoder.JSONDecodeError:
            # store
            data = []  # If the file is empty, create an empty list

        data.append(profiles)

        # move file pointer to beginning of file
        file.seek(0)
        json.dump(data, file, indent=4)


def check_cred():
    """
    Checks for username and password. User can create a profile. User's favorite
    stocks are saved in their profile.

    :return: User's new profile
    """
    print("Welcome!\n")
    while True:
        response = str(input("Enter 1 to sign in or 2 to create a profile. Creating a profile will let you save your favorite stocks: "))

        if response == "1":
            name = input(str("Please enter your username: "))
            bool, dict = check_username(name)
            if bool:
                return dict

        elif response == "2":
            profile = create_profile()
            profiles = {}
            profiles[profile.get_name()] = []
            while True:
                ticker = str(input("Please enter a stock ticker you want to keep track of or enter 1 to exit: "))
                if ticker == "1":
                    break
                profile.set_fav_stocks(ticker)

            profiles['fav'] = profile.get_fav_stocks()
            save_profile(profiles)
            break

    return profile


def menu():
    stock_list = []

    while True:
        stock = str(input("Look up stock or enter 1 to exit: "))

        if stock == "1":
            print("Thank you for stopping by!")
            break
        else:
            stock = get_data(stock)
            news = get_news(stock)
            stock_list.append(stock)
            table = pretty_print(stock_list)
            # to get the color to work I had to click on Emulate terminal in
            # the output console
            console = Console(color_system="windows")
            console.print(table)
            # print news
            print('\n\n\n')

            print(news[0]['title'])
            print(news[0]['link'])


def main():
    """
    new_profile could be a dict, a boolean value, or class object.
    Does not work if the username does not exist
    """
    new_profile = check_cred()
    if isinstance(new_profile, dict):
        fav_stocks = []
        favs = new_profile['fav']
        for stock in favs:
            stock = get_data(stock)
            fav_stocks.append(stock)
        table = pretty_print(fav_stocks)
        console = Console(color_system="windows")
        console.print(table)
    # check if user created a profile and print out their favorite stocks
    # should this be a function? Print out favs for user?
    else:
        stocks = []
        for stock in new_profile.get_fav_stocks():
            stock = get_data(stock)
            stocks.append(stock)
        table = pretty_print(stocks)
        console = Console(color_system="windows")
        console.print(table)

    menu()


if __name__ == "__main__":
    main()


