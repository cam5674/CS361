class Profile:

    def __init__(self, username, email=None, verf=None):
        self._fav_stocks = []
        self._news = []
        self._verf = verf
        self._email = email
        self._subreddits = []
        self._username = username

    def get_name(self):
        return self._username

    def get_email(self):
        return self._email

    def get_verf(self):
        return self._verf

    def get_fav_stocks(self):
        return self._fav_stocks

    def get_news(self):
        return self._news

    def get_subreddits(self):
        return self._subreddits

    def set_fav_stocks(self, stock):

        self._fav_stocks.append(stock)

    def set_news(self, headline):
        self._news.append(headline)

    def set_subreddits(self, subreddit):
        self._subreddits.append(subreddit)

    def print_fav_stocks(self):
        for i in self._fav_stocks:
            print(i)
