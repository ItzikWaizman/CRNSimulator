import argparse
import os
from config import Parameters
from simulator import Simulator

def main(params_folder=None):
    # Create an instance of Simulator using the parameters from the folder or default
    if params_folder:
        params_paths = {
            'LAA': os.path.join(params_folder, 'params_LAA.json'),
            'OLAA_T': os.path.join(params_folder, 'params_OLAA_T.json'),
            'OLAA_R': os.path.join(params_folder, 'params_OLAA_R.json')
        }
        simulator = Simulator(params_paths=params_paths, seed=10)
    else:
        simulator = Simulator(seed=10)

    simulator.run_simulation()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Network Simulator')
    parser.add_argument('--params_folder', type=str, help='Path to the folder containing the parameter JSON files for LAA, OLAA_T, and OLAA_R protocols')
    args = parser.parse_args()

    params_folder = args.params_folder if args.params_folder else None
    main(params_folder)