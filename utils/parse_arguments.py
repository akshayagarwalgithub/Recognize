import argparse
def parse_training_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument("--reset_training", help="Delete all the past training model received", type=bool, default=False)
    args = parser.parse_args()

    return args