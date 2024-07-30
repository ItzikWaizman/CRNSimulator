import argparse
import os
from config import Parameters
from simulator import Simulator

def main(config_path=None):
    # Create an instance of Simulator using the parameters
    simulator = Simulator(seed=10)
    simulator.run_simulation()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Network Simulator')
    parser.add_argument('--config', type=str, help='Path to the config file')
    args = parser.parse_args()

    config_path = args.config if args.config else None
    main(config_path)