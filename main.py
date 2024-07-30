import argparse
import os
from config import Parameters
from simulator import Simulator

def main(config_path=None):
    # Create an instance of Parameters
    Params = Parameters(config_path)
    
    # Create an instance of Simulator using the parameters
    simulator = Simulator(Params.params)

    simulator.run_simulation()

    simulator.print_simulation_details()
    
    simulator.post_simulation()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Network Simulator')
    parser.add_argument('--config', type=str, help='Path to the config file')
    args = parser.parse_args()

    config_path = args.config if args.config else None
    main(config_path)