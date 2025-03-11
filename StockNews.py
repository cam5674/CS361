import zmq

import feedparser

context = zmq.Context()
socket = context.socket(zmq.REP)

socket.bind("tcp://*:5555")


def fetch_news(ticker):
    url = f"https://news.google.com/rss/search?q={ticker}+stock&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(url)

    articles = []
    for entry in feed.entries[:1]:  # Get the 5 most recent articles
        articles.append({
            "title": entry.title,
            "url": entry.link,
            "source": entry.source.title if "source" in entry else "Unknown",
            "date": entry.published if "published" in entry else "No date available"
        })

    return articles
# username = None


while True:
    favorite_stocks = socket.recv_json()
    print(favorite_stocks)

    print(f"Received request of latest news for stocks: {favorite_stocks}")

    if len(favorite_stocks) > 0:
        news_data = {}
        for ticker in favorite_stocks:
            news_data[ticker] = fetch_news(ticker)

        socket.send_json(news_data)



