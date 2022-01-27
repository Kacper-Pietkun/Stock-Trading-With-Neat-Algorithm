import pandas as pd
import pickle
import os
import constants
from bookmaker import Bookmaker


def simulate_stock_market(data, macd, signal, start_index, current_capital):
    bookmaker = Bookmaker(current_capital)
    last_index = len(data.index)

    last_macd_value = macd[start_index]
    last_signal_value = signal[start_index]

    # start from start_index + 1, because we treat start_index as a point of reference
    for i in range(start_index + 1, last_index):
        # if MACD crosses SIGNAL from top, then sell stocks
        if last_macd_value > last_signal_value and signal[i] > macd[i]:
            bookmaker.sell_all_stocks(data[i])
        # else if MACD crosses SIGNAL from bottom, then buy stocks
        elif last_macd_value < last_signal_value and signal[i] < macd[i]:
            bookmaker.buy_all_stocks(data[i])

        last_macd_value = macd[i]
        last_signal_value = signal[i]

    # On the last day we sell all of our stocks
    bookmaker.sell_all_stocks(data[last_index - 1])
    return bookmaker.capital


def load_macd(path):
    with open(path + '_macd', 'rb') as fp:
        macd = pickle.load(fp)
    with open(path + '_signal', 'rb') as fp:
        signal = pickle.load(fp)
    return macd, signal


def main():
    test_data_path = os.path.join(constants.ROOT_DIR, constants.PATH_CALCULATED_MACD_TEST)
    stock_data_path = os.path.join(constants.ROOT_DIR, constants.PATH_STOCK_DATA)
    for _, _, file_names in os.walk(stock_data_path):
        for file_name in file_names:
            full_load_path_stock_data = os.path.join(stock_data_path, file_name)
            data = pd.read_csv(full_load_path_stock_data)
            data_set = data[constants.CSV_OPEN_COLUMN]

            full_load_path_test_data = os.path.join(test_data_path, file_name)
            try:
                macd, signal = load_macd(full_load_path_test_data)
            except FileNotFoundError:
                continue
            start_capital = constants.STARTING_CAPITAL
            result_capital = simulate_stock_market(data_set, macd, signal, 35, start_capital)
            print('{}: we have earned {}'.format(file_name, result_capital - start_capital))


if __name__ == '__main__':
    main()
