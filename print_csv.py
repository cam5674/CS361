import csv
import glob
import os
from rich.console import Console
from rich.table import Table

fp = "C:\\Users\\camer\\Desktop\\test_1\\*"


def pretty_print_csv(times: int):
    """
    Creates a stock table that prints out a user favorite stocks. Also, adds a
    row for every search the user makes.

    :param stock: A list of dictionaries. [ [{}], [{}] ]
    :return: Table to be printed

    """
    # get the latest file in the folder

    list_of_files = glob.glob(fp)
    latest_file = max(list_of_files, key=os.path.getctime)

    if times == 0:
        return None
    table = Table("Date", style="magenta")
    table.add_column("Close", justify="right", style="white")
    table.add_column("Volume", justify="right", style="white")
    table.add_column("Open", justify="right", style="white")
    table.add_column("High", justify="right", style="white")
    table.add_column("Low", justify="right", style="white")
    counter = 0
    try:
        with open(latest_file, "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if counter == times:
                    break
                table.add_row(row[0], row[1], row[2],row[3],row[4], row[5])
                counter += 1
    except FileNotFoundError:
        print("No such file exits")

    f.close()
    return table


def prompt_stock_history_table():
    while True:
        try:
            stock = int(input("How many past days would you like to view? "))
            print("\n")
            table = pretty_print_csv(stock)
            console = Console(color_system="windows")
            console.print(table)
            break
        except ValueError:
            print("Please enter a number")
            continue




