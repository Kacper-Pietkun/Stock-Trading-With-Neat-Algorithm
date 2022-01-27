import pandas as pd
import pickle
import os
import neat
import constants
from bookmaker import Bookmaker


def simulate_stock_market(best_genome, config, data, macd, signal, start_index, current_capital):
    net = neat.nn.FeedForwardNetwork.create(best_genome, config)
    bookmaker = Bookmaker(current_capital)
    last_index = len(data.index)
    for i in range(start_index + 1, last_index):
        decision = net.activate((macd[i], signal[i]))  # decision can be a real number form 0 to 1

        # if there is a missing data cell, then substitute it with the latest stock value
        index = i
        while pd.isnull(data[index]):
            index -= 1
        if decision[0] > 0.9:
            bookmaker.buy_all_stocks(data[index])
        elif decision[0] < 0.1:
            bookmaker.sell_all_stocks(data[index])

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
    config_path = os.path.join(constants.ROOT_DIR, constants.PATH_NEAT_CONF)
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    # load best genome
    best_genome_path = os.path.join(constants.ROOT_DIR, constants.PATH_NEAT_BEST_GENOME)
    best_genome = None
    try:
        with open(best_genome_path, 'rb') as fp:
            best_genome = pickle.load(fp)
    except FileNotFoundError:
        print('You need to train a network first')
        return

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
            result_capital = simulate_stock_market(best_genome, config, data_set, macd, signal, 35, start_capital)
            print('{}: we have earned {}'.format(file_name, result_capital - start_capital))


if __name__ == '__main__':
    main()
