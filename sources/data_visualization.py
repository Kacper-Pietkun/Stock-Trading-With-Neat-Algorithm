import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import pickle
import constants


def load_macd(path):
    with open(path + '_macd', 'rb') as fp:
        macd = pickle.load(fp)
    with open(path + '_signal', 'rb') as fp:
        signal = pickle.load(fp)
    return macd, signal


def display_charts(data, macd, signal):
    fig, (ax_original, ax_macd) = plt.subplots(nrows=2, ncols=1)
    fig.set_size_inches(13, 8)

    rows_number = len(data.index)

    # Setting propperties of the main chart
    ax_original.set_title('Historical Data')
    ax_original.set_ylabel('Open Price', fontsize=18)
    ax_original.xaxis.set_ticks(np.linspace(1, rows_number, 10))
    ax_original.grid()
    for tick in ax_original.get_xticklabels():
        tick.set_fontsize(14)
        tick.set_rotation(12)

    for tick in ax_original.get_yticklabels():
        tick.set_fontsize(14)

    # plotting data on the chart
    ax_original.plot(data[constants.CSV_DATE_COLUMN], data[constants.CSV_OPEN_COLUMN])

    # Setting propperties of the MACD chart
    ax_macd.set_title('MACD')
    ax_macd.set_xlabel('Date', fontsize=18)
    ax_macd.set_ylabel('Value', fontsize=18)
    ax_macd.xaxis.set_ticks(np.linspace(1, rows_number, 10))
    ax_macd.grid()
    for tick in ax_macd.get_xticklabels():
        tick.set_fontsize(14)
        tick.set_rotation(12)

    for tick in ax_macd.get_yticklabels():
        tick.set_fontsize(14)

    zero_data_y = [0] * rows_number
    for i in range(0, rows_number):
        zero_data_y[i] = macd[i] - signal[i]
    np_zero_data_y = np.array(zero_data_y)

    # plotting data on the chart
    ax_macd.plot(data[constants.CSV_DATE_COLUMN], macd, color='b', label='MACD')
    ax_macd.plot(data[constants.CSV_DATE_COLUMN], signal, color='#990033', label='SIGNAL')
    ax_macd.bar(data[constants.CSV_DATE_COLUMN][np_zero_data_y > 0], np_zero_data_y[np_zero_data_y > 0], color='g')
    ax_macd.bar(data[constants.CSV_DATE_COLUMN][np_zero_data_y < 0], np_zero_data_y[np_zero_data_y < 0], color='#ff3300')

    plt.legend()

    fig.tight_layout(pad=4)
    # Updating main window
    plt.show()


def main():
    my_file_name = input('type name of the file: ')

    load_path_stock_data = os.path.join(constants.ROOT_DIR, constants.PATH_STOCK_DATA)
    load_path_calculated_macd_training = os.path.join(constants.ROOT_DIR, constants.PATH_CALCULATED_MACD_TRAINING)
    load_path_calculated_macd_test = os.path.join(constants.ROOT_DIR, constants.PATH_CALCULATED_MACD_TEST)

    full_load_path_data = os.path.join(load_path_stock_data, my_file_name)
    try:
        stock_data = pd.read_csv(full_load_path_data)
    except FileNotFoundError:
        print("File was not found")
        return

    full_load_path_macd_training = os.path.join(load_path_calculated_macd_training, my_file_name)
    full_load_path_macd_test = os.path.join(load_path_calculated_macd_test, my_file_name)
    try:
        macd, signal = load_macd(full_load_path_macd_training)
    except FileNotFoundError:
        try:
            macd, signal = load_macd(full_load_path_macd_test)
        except FileNotFoundError:
            print("File was not found")
            return

    display_charts(stock_data, macd, signal)


if __name__ == '__main__':
    main()
