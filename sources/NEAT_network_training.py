import pandas as pd
import neat
import os
import pickle
import constants
import math
from bookmaker import Bookmaker

input = []
input_index = 0


def training(genomes, config):
    # We have x number of genomes. X is specified in the configuration file
    # for ever genome we will create one object of Bookmaker class, this object will simulate behaviour of the person
    # which buys and sells stocks
    # Also for each genome we create a neural network
    bookmakers = []
    nets = []
    ge = []
    # Creating individual data for every object in this generation
    for _, genome in genomes:
        bookmaker = Bookmaker(constants.STARTING_CAPITAL)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = 0
        bookmakers.append(bookmaker)
        nets.append(net)
        ge.append(genome)

    # getting data for this generation
    global input_index
    (macd, signal, data_set) = input[input_index]
    input_index = input_index + 1
    input_index = input_index % len(input)
    rows_number = len(data_set.index)

    # starting simulation, from 35 because we need to omit all of the zeroes that appears during calculating MACD
    for i in range(35, rows_number):
        for j in range(0, len(bookmakers)):
            decision = nets[j].activate((macd[i], signal[i]))  # decision can be a real number form 0 to 1

            # if there is a missing data cell, then substitute it with the latest stock value
            index = i
            while pd.isnull(data_set[index]):
                index -= 1
            if decision[0] > 0.9:
                bookmakers[j].buy_all_stocks(data_set[index])
            elif decision[0] < 0.1:
                bookmakers[j].sell_all_stocks(data_set[index])

            # Increase fitness when bookmaker sold stock with profit
            # Decrease fitness when bookmaker sold stock with loss
            if len(bookmakers[j].incomes_list) > 0:
                index = len(bookmakers[j].incomes_list) - 1
                difference = bookmakers[j].incomes_list[index] - bookmakers[j].expenses_list[index]
                if difference > 0:
                    ge[j].fitness += 5
                if difference <= 0:
                    ge[j].fitness -= 10

                ge[j].fitness = ge[j].fitness + difference
                bookmakers[j].incomes_list.pop()
                bookmakers[j].expenses_list.pop()

            # bookmaker is bankrupt, so delete it from further trading
            if bookmakers[j].capital == 0 and bookmakers[j].number_of_stocks == 0:
                ge[j].fitness -= 100
                nets.pop(bookmakers.index(bookmakers[j]))
                ge.pop(bookmakers.index(bookmakers[j]))
                bookmakers.pop(bookmakers.index(bookmakers[j]))


def load_input_for_training(stock_data_path, training_data_path):
    for _, _, file_names in os.walk(stock_data_path):
        for file_name in file_names:
            full_load_path_stock_data = os.path.join(stock_data_path, file_name)
            data = pd.read_csv(full_load_path_stock_data)
            data_set = data[constants.CSV_OPEN_COLUMN]

            full_load_path_training_data = os.path.join(training_data_path, file_name)
            try:
                macd, signal = load_macd(full_load_path_training_data)
            except FileNotFoundError:
                continue
            input.append((macd, signal, data_set))


def load_macd(path):
    with open(path + '_macd', 'rb') as fp:
        macd = pickle.load(fp)
    with open(path + '_signal', 'rb') as fp:
        signal = pickle.load(fp)
    return macd, signal


def run(config_path):
    # creating configuration basing on our configuration file
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    # creating population basing on our configuration
    population = neat.Population(config)

    # creating reporter that will print crucial data in the terminal
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    training_data_path = os.path.join(constants.ROOT_DIR, constants.PATH_CALCULATED_MACD_TRAINING)
    stock_data_path = os.path.join(constants.ROOT_DIR, constants.PATH_STOCK_DATA)

    # load data to global variable
    load_input_for_training(stock_data_path, training_data_path)

    # saving the best genome after completing the training
    # Running as much generations as there is files in training directory
    number_of_generations = len([name for name in os.listdir(training_data_path)])
    number_of_generations /= 2  # divide by 2, because of the fact that for each file there is macd and signal file
    winner = population.run(training, number_of_generations)

    # statistics of the best genome
    print('\nBest genome:\n{!s}'.format(winner))

    # save the best genome to a file
    save_path = os.path.join(constants.ROOT_DIR, constants.PATH_NEAT_BEST_GENOME)
    with open(save_path, 'wb') as fp:
        pickle.dump(winner, fp)


def main():
    config_path = os.path.join(constants.ROOT_DIR, constants.PATH_NEAT_CONF)
    run(config_path)


if __name__ == '__main__':
    main()
