from rich.console import Console
from rich.table import Table
from test_params import get_news
import test_params

# Do I need to set up zmq



def print_table():
    """
    Creates a news table that prints out links for users.

    :param stock: A list of dictionaries. [ [{}], [{}] ]
    :return: Table to be printed
    """
    news = get_news()
    table = Table("Ticker", style="magenta", expand=True)
    table.add_column("Title", justify="right", style="white", )
    table.add_column("Date", justify="right", style="white",)
    table.add_column("Source", justify="right", style="white")
    table.add_column("Link", justify="right", style="white")

    for key, values in news.items():
        for value in values:
            table.add_row(key,value['title'], value['date'], value['source'], value['url'])

    console = Console(color_system="windows", width=180)
    console.print(table)


print_table()