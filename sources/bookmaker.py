import math


class Bookmaker:

    def __init__(self, start_capital):
        self.capital = start_capital
        self.number_of_stocks = 0
        self.incomes_list = []
        self.expenses_list = []

    def buy_one_stock(self, stock_price):
        if self.capital > stock_price:
            self.capital = self.capital - stock_price
            self.expenses_list.append(stock_price)
            self.number_of_stocks += 1

    # buy all stocks that bookmaker can afford
    def buy_all_stocks(self, stock_price):
        how_many_stocks = math.floor(self.capital / stock_price)
        if how_many_stocks > 0:
            self.capital -= stock_price * how_many_stocks
            self.expenses_list.extend([stock_price] * how_many_stocks)
            self.number_of_stocks += how_many_stocks

    def sell_one_stock(self, stock_price):
        if self.number_of_stocks > 0:
            self.capital += stock_price
            self.incomes_list.append(stock_price)
            self.number_of_stocks -= 1

    def sell_all_stocks(self, stock_price):
        if self.number_of_stocks > 0:
            self.capital += stock_price * self.number_of_stocks
            self.incomes_list.extend([stock_price] * self.number_of_stocks)
            self.number_of_stocks = 0
