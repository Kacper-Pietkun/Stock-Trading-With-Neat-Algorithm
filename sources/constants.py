from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent

PATH_STOCK_DATA = 'stock_data'
PATH_CALCULATED_MACD_TEST = 'test_calculated_macd_signal'
PATH_CALCULATED_MACD_TRAINING = 'training_calculated_macd_signal'
PATH_NEAT_BEST_GENOME = 'neat_genomes/best_genome'
PATH_NEAT_CONF = 'resources/config-feedforward'

STARTING_CAPITAL = 1000

CSV_OPEN_COLUMN = 'open'
CSV_DATE_COLUMN = 'date'
