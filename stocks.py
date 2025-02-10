import json

from rich.text import Text
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


def check_username(name: str):
    """
    Returns True if username is in the file. The dictionary of the profile is returned
    as well. Returns False if the username is not in the file and 0 for the
    dictionary.
    Checks if username is in storage file.
    :param name:
    :return: A bool depending on if the username is in the json file or not.

    """

    with open("storage.json", "r") as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            return False
        for dict in data:
            for key in dict.items():
                if key[0] == name:
                    f.close()
                    return True, dict
        else:
            f.close()
            return False, 0


def create_profile():
    """
    Creates a new profile.

    :return: New profile class object profilec
    """
    while True:
        name = str(input("Enter a username: "))
        # bool value[0]
        if check_username(name)[0]:
            print("Username is taken. Please enter another username.")
            continue
        break
    # Profile example:  {"cam5674": [], "fav": ["vti","goog"]
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
    """
    console = Console()
    text = Text("Welcome!")
    text.stylize("bold magenta",0,8)
    console.print(text)
    """
    print("Welcome!\n")
    while True:
        response = str(input("Enter 1 to sign in or 2 to create a profile. Creating a profile will let you save your favorite stocks: "))

        if response == "1":
            # check for valid username
            while True:
                name = input(str("Please enter your username: "))
                bool, dict = check_username(name)
                if bool:
                    # valid, return dict
                    return dict
                # ask again
                else:
                    break
        elif response == "2":
            # Can you replace the dictionary with the class object?
            # save class object in profile
            profile = create_profile()
            # save profile info in dictionary
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


def menu(profile = None):
    stock_list = []

    while True:
        stock = str(input("Look up stock or enter 1 to exit: "))

        if stock == "1":
            print("Thank you for stopping by!")
            break
        else:
            stock_data = get_data(stock)
            # news = get_news(stock)
            stock_list.append(stock_data)
            table = pretty_print(stock_list)
            # to get the color to work I had to click on emulate terminal in
            # the output console
            console = Console(color_system="windows")
            console.print(table)
            response = str(input(f"Would you like to add {stock} to your favorites? y/n "))
            if response == "y":
                # profile['fav'].append(stock)
                # I don't think you need a try block here to check if the file is empty
                with open("storage.json", "r") as f:
                    # get value
                    data = json.load(f)
                    for dict in data:
                        for key in dict.keys():
                            if key == list(profile)[0]:
                                # add to value
                                dict["fav"].append(stock)
                # write to file
                with open("storage.json", "w") as file:
                    json.dump(data, file, indent=4)
                    print(f"Your favorites has been updated with {stock}! ")
                    file.close()

            elif response == "n":
                continue

            # To be implemented
            # print('\n\n\n')
            # add news later(commented out news above)
            #print(news[0]['title'])
            #print(news[0]['link'])


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
        menu(new_profile)
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
        print("\n\n")
        menu()


if __name__ == "__main__":
    main()


