"""
This program prints a text based menu in the console for the user to interact
with. All user information(favorite stocks/username) is saved in the
storage.json file. A user can search stocks, save/add stocks, and look up stock
history.

WARNING: For this program to work you need an api key from tiingo. The cred
file contains my personal key. If you would like to use this program you will
need to get a key from tiingo, create a module named cred and write your key in
the program, like this: key = "7777777777". Then you can import it to this module.

"""
from print_csv import prompt_stock_history_table
from download import prompt_stock_for_dl
import re
import json
from rich.console import Console
from rich.table import Table
import requests
import cred
from profile import Profile
from news import print_news_table
from client_micro_b import send_email
from client_micro_c import delete_stock

#TODO Check if error handling is correct for file empty error
#TODO write documentation for microservices


def get_data(stock: str):
    """
    Uses tiingo api to get the stock. Takes a string from the user, string
    needs to be an accurate ticker.

    Example of data:
3
    list with a dictionary:
    [{}]
    :param stock: ticker to be looked up.
    :return: JSON of data or an empty list if not a correct ticker
    """

    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.get(f"https://api.tiingo.com/iex/?tickers="
                            f"{stock}&token={cred.key}", headers=headers)
    data = response.json()
    return data


def pretty_print(stock):
    """
    Creates a stock table that prints out a user favorite stocks. Also, adds a
    row for every search the user makes.

    :param stock: A list of dictionaries. [ [{}], [{}] ]
    :return: Table to be printed
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
        table.add_row(stock_info[0]['ticker'], str(stock_info[0]['open']),
                      str(stock_info[0]['high']), str(stock_info[0]['low']),
                      str(stock_info[0]['tngoLast']), percentage_change,
                      str(stock_info[0]['volume']))

    return table


def reset_table():
    """
    Erases the current table
    """
    table = Table("Ticker", style="magenta")
    table.add_column("Last Price", justify="right", style="white")
    table.add_column("High", justify="right", style="white")
    table.add_column("Low", justify="right", style="white")
    table.add_column("Open", justify="right", style="white")
    table.add_column("Volume", justify="right", style="white")


def check_username(name: str):
    """
    Returns True if username is in the file. The dictionary of the profile is
    returned as well. Returns False if the username is not in the file and 0 for
    the dictionary. Checks if username is in storage file.
    :param name: String
    :return: A bool depending on if the username is in the json file or not.

    """
    # open file to check JSON for name
    with open("storage.json", "r") as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            return False
        for dic in data:
            for key in dic.items():
                if key[0] == name:
                    f.close()
                    # name was found
                    return True, dic
        else:
            f.close()
            # name is not in json file
            return False, 0


def create_profile():
    """
    Creates a new profile.
    Example of profile: {"cam5674": [], "fav": ["vti","goog"]

    :return: New profile class object profile
    """

    # prompt user for a username. Check if it is longer than 15 characters
    while True:
        name = str(input("Enter a username. A username needs to be less than 15 characters: ").replace(" ", ""))

        print(name)
        if len(name) >= 15:
            print("\n")
            print("Too long. Please enter a username that is less than 15 characters.")
            print("\n")
            continue
        # bool value[0], 0 = name is taken.
        elif len(name) < 1:
            print("\n")
            print("No characteres detected. Please enter a username that is less than 15 characters.")
            print("\n")
            continue
        elif name.isspace():
            print("\n")
            print("Empty spaces detected. Please enter a username that is less"
                  " than 15 characters and with no empty spaces. ")
            print("\n")
            continue
        try:
            if check_username(name)[0]:
                print("Username is taken. Please enter another username.")
                print("\n")
                continue
        except TypeError:
            break
        break

    # prompt user for email
    while True:
        email = str(input("Enter your email: "))

        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$", email):
            continue
        while True:
            try:
                response = str(input("Would you like email updates? Enter 1 for yes or 0 for no: "))
                break
            except TypeError:
                continue

        break
    # create instance to store information
    profile = Profile(name, email, response)
    print(email)
    send_email(profile.get_email())
    print("Sending a confirmation email...")

    return profile


def save_profile(profiles: dict):
    """
    Opens storage.json and adds a new profile to the json file.
    [{}]
    :param profiles: Dictionary that contains profile information
    :return:
    """
    with open("storage.json", "r+") as file:
        try:
            data = json.load(file)
        except json.decoder.JSONDecodeError:
            # store
            # If the file is empty, create an empty list
            data = []

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

    # introduce program
    stock_list = []
    print("\n\n")
    print("Welcome!\n")
    while True:
        response = str(input("Enter 1 to sign in \nEnter 2 to create a profile. Creating a profile will let you save your favorite stocks. "
                             "\nEnter 3 to continue without a profile\nEnter 4 for more information about the program\nEnter 5 to exit program\nPlease enter your response: "))
        print("\n")

        if response == "1":
            # check for valid username
            while True:
                name = input(str("Please enter your username: "))
                print("\n")
                if len(name) >= 15:
                    print("Too long. Please enter a username that is less than 15 characters.")
                    print("\n")
                    continue
                # check if the name is valid
                elif name == "1":
                    break
                valid, dic = check_username(name)
                if valid:
                    # valid, return dict
                    return dic
                # ask again
                else:
                    print("You did not enter the correct username. Please try again or enter 1 to quit: ")
                    print("\n")
                    continue
        elif response == "2":
            # save class object in profile
            profile = create_profile()
            print(profile)

            # save profile info in dictionary
            # profiles = {profile.get_name(): [], "email": profile.get_email(), "email service": profile.get_verf()}
            profiles = {profile.get_name(): [], "email": profile.get_email(), "email service": profile.get_verf()}
            #profiles[profile.get_name()] = []
            while True:
                ticker = str(input("Please enter a stock ticker you want to keep track of.\n"
                                   "The stock ticker needs to be a valid, for example: vti"
                                   "\nEnter 1 to continue or a stock ticker\n\nEnter your response:  "))
                print("\n")
                if ticker == "1":
                    break

                # check if stock tickers are correct and then add to fav list
                stocks = get_data(ticker)
                if not stocks:
                    print("Did not enter a correct stock ticker. Please try again.")
                    print("\n")
                    continue
                profile.set_fav_stocks(ticker)
                stock_list.append(stocks)

            # print out stock data. Adds a row to previous table
            table = pretty_print(stock_list)
            console = Console(color_system="windows")
            console.print(table)
            profiles['fav'] = profile.get_fav_stocks()
            save_profile(profiles)
            break
        elif response == "3":
            warning = input("WARNING: You will not be able to save your searches. Do you wish to continue? y/n\nEnter your response: ")
            if warning == "y":
                return response
            else:
                continue
        elif response == "4":
            print("This program allows you to look up the real-time prices of stocks. "
                  "\nIf you create a profile you can save and add stocks to your profile. "
                  "\nWhen you sign in with your profile name, a table with your favorite stocks are displayed. "
                  "\nTo create a profile you only need to enter '3' to select the create profile option. "
                  "\nYour username needs to be less than 15 characters.\n\n")
        elif response == "5":
            print("Thank you for stopping by!")
            return "5"
    return profile


def menu(profile=None):
    """
    Looks up a stock for a user. Will print out a table of the user's favorite
    stocks. If the user selects '3' or if the profile is a '3', then the program
    will treat the user as a guest.

    :param profile: If dictionary, profile is old and if '3', user is a guest.
    :return: A number, 0 or 1: 0 to end the program, 1 to continue the program
    """
    # Need to check username here for new profile edge case
    print(profile)
    stock_list = []
    while True:
        # look up stocks for user
        if profile == '3':
            stock = str(input("Look up stock or enter 1 to exit\nEnter 2 to go back to main menu\nEnter 3 to look up stock history\nEnter your response: "))
            print("\n")
        else:
            stock = str(input("Look up stock or enter 1 to exit\nEnter 2 to go back to main menu\nEnter 3 to look up stock history\nEnter 4 to edit your stocks\nEnter your response: "))
            print("\n")

        if stock == "1":
            print("Thank you for stopping by!")
            return "0"

        elif stock == "2":
            return "1"
        elif stock == "4":
            # check for the correct information(dictionary)
            if type(profile) is not dict:
                profile = check_username(profile)
                if type(profile) is tuple:
                    profile = profile[1]
                print(profile)

            while True:
                s = str(input("Enter 1 to see list of favorite stocks\nEnter 2 to return to previous menu or enter a stock to delete from your stock favorites:\nEnter 3 to see stock history: "))
                sl = []
                print("\n")
                # print out list of favorite stocks
                if s == "1":
                    print(f"profile before list:{profile}")
                    for ticker in profile['fav']:
                        print(f"{ticker}")
                        sl.append(ticker)
                    print("\n")
                elif s == "2":
                    break
                else:
                    # get info for stock deletion micro service
                    user_info = {'username': next(iter(profile)), 'stock': s}
                    reply = delete_stock(user_info)
                    if reply == "0":
                        print("Incorrect stock ticker")
                        print("\n")
                    else:
                        # turn reply into a dictionary
                        profile = eval(reply)
                        print(f"profile after initial deletion{profile}")
                        print(f"Deleted {s}")
                        print("\n")

            continue
        elif stock == "3":
            prompt_stock_for_dl()
            prompt_stock_history_table()
        else:
            # get stock data and append it to a list if stock ticker is correct
            stock_data = get_data(stock)
            if not stock_data:
                print("Did not enter a correct stock ticker. Please try again.")
                print("\n")
                continue
            else:
                stock_list.append(stock_data)
                # print out stock data. Adds a row to previous table
                table = pretty_print(stock_list)
                console = Console(color_system="windows")
                console.print(table)

                # no profile option
                if profile != "3":
                    response = str(input(f"Would you like to add {stock} to your favorites? y/n\nEnter your response: "))
                    print("\n")
                    if response == "y":
                        with open("storage.json", "r") as f:
                            # get value
                            data = json.load(f)
                            for dic in data:
                                print(f"dic: {dic}")
                                for key in dic.keys():
                                    if key == list(profile)[0]:
                                        # add to value and update profile
                                        dic["fav"].append(stock)
                                        profile = dic
                        # write to file
                        with open("storage.json", "w") as file:
                            json.dump(data, file, indent=4)
                            print(f"Your favorites has been updated with {stock}! ")
                            print("\n")
                            file.close()

                    elif response == "n":
                        continue


def main():
    """
    new_profile could be a dict, a boolean value, or class object.
    """
    while True:
        # get profile and check if empty file
        try:
            new_profile = check_cred()
        except TypeError:
            print("File is empty. No profiles exists. You need to create a profile before signing in.")
            continue

        # Continue without a profile
        if new_profile == "3":
            menu(new_profile)

        # exit program
        elif new_profile == "5":
            break

        # If new_profile is a dictionary, then it is an old profile
        elif isinstance(new_profile, dict):
            # get list of favorite stocks and put them in favs
            fav_stocks = []
            favs = new_profile['fav']
            for stock in favs:
                stock = get_data(stock)
                fav_stocks.append(stock)

            # print favorite stocks for user
            table = pretty_print(fav_stocks)
            console = Console(color_system="windows")
            console.print(table)
            print(print_news_table(next(iter(new_profile))))
            print("\n")

            # exit program
            if menu(new_profile) == "0":
                break

        # new profile
        else:
            # print out news articles
            name = new_profile.get_name()
            print_news_table(name)

            # exit program
            if menu(new_profile.get_name()) == "0":
                break


if __name__ == "__main__":
    main()
