import pandas as pd
import os
import pickle
import numpy as np
import constants


# Calculate exponential moving average
def EMA(data_set, n, index):
    if index - n < 0:
        return 0
    numerator = 0
    denominator = 0
    alpha = 2 / (n + 1)
    for i in range(0, n + 1):
        if index - i < 0:
            break
        numerator = numerator + pow(1 - alpha, i) * data_set[index - i]
        denominator = denominator + pow(1 - alpha, i)
    return numerator / denominator


def calculate_macd_and_signal(data, rows_number):
    # Calculating MACD for every row of stock information
    macd = [0] * rows_number
    data_set = data[constants.CSV_OPEN_COLUMN]

    for i in range(35, rows_number):
        macd[i] = EMA(data_set, 12, i) - EMA(data_set, 26, i)

    # Calculating SIGNAL
    signal = [0] * rows_number
    for i in range(35, rows_number):
        signal[i] = EMA(macd, 9, i)

    return macd, signal


def calculate_and_save(load_path, save_path_training, save_path_test):
    np.random.seed(42)
    progress = 0
    for _, _, file_names in os.walk(load_path):
        for file_name in file_names:

            full_load_path = os.path.join(load_path, file_name)
            full_save_path_test = os.path.join(save_path_test, file_name)
            full_save_path_training = os.path.join(save_path_training, file_name)

            data = pd.read_csv(full_load_path)
            rows_number = len(data.index)

            macd, signal = calculate_macd_and_signal(data, rows_number)

            # Save training and test data to different folders
            if np.random.randint(low=0, high=10) < 9:
                save_path = full_save_path_training
            else:
                save_path = full_save_path_test

            # saving macd to a file
            with open(save_path + '_macd', 'wb') as fp:
                pickle.dump(macd, fp)

            # saving signal to a file
            with open(save_path + '_signal', 'wb') as fp:
                pickle.dump(signal, fp)

            progress += 1
            print("progress {}%".format(progress / len(file_names) * 100))


def main():
    load_path = os.path.join(constants.ROOT_DIR, constants.PATH_STOCK_DATA)
    save_path_test = os.path.join(constants.ROOT_DIR, constants.PATH_CALCULATED_MACD_TEST)
    save_path_train = os.path.join(constants.ROOT_DIR, constants.PATH_CALCULATED_MACD_TRAINING)
    calculate_and_save(load_path, save_path_train, save_path_test)


if __name__ == '__main__':
    main()
