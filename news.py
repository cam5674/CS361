from rich.console import Console
from rich.table import Table
from test_params import get_news
import pyshorteners
# Do I need to set up zmq


def print_news_table(username=None):
    """
    Creates a news table that prints out links for users.

    :param stock: A list of dictionaries. [ [{}], [{}] ]
    :return: Table to be printed
    """
    #TODO: edit tinyurl so it is more readable
    #TODO:
    if username:
        news = get_news(username)
    else:
        news = get_news()
    table = Table("Ticker", style="magenta", expand=True)
    table.add_column("Title", justify="right", style="white", )
    table.add_column("Date", justify="right", style="white",)
    table.add_column("Source", justify="right", style="white")
    table.add_column("Link", justify="right", style="white")

    for key, values in news.items():
        for value in values:
            s = pyshorteners.Shortener()
            lurl = value['url']
            short = s.tinyurl.short(lurl)
            table.add_row(key,value['title'], value['date'], value['source'], short)

    console = Console(color_system="windows", width=150)
    console.print(table)


