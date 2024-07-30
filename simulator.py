import random
import numpy as np
import matplotlib.pyplot as plt
from config import Parameters
from network_entities.cognitive_radio_network import CognitiveRadioNetwork

class Simulator:
    def __init__(self, seed=None):
        self.seed = seed
        if seed is not None:
            self.set_seed(seed)
        self.params_LAA = Parameters(protocol='LAA').params
        self.params_OLAA_T = Parameters(protocol='OLAA_T').params
        self.params_OLAA_R = Parameters(protocol='OLAA_R').params
        self.networks = self.create_networks()

    def set_seed(self, seed):
        random.seed(seed)
        np.random.seed(seed)

    def create_networks(self):
        networks = []
        params_list = [self.params_LAA, self.params_OLAA_T, self.params_OLAA_R]
        for params in params_list:
            networks.append(CognitiveRadioNetwork(params))
        return networks

    def run_simulation(self):
        results = []
        for network in self.networks:
            network.execute_traffic()
            results.append(network.calculate_statistics())
        self.print_simulation_details(results)
        self.plot_statistics(results)

    def print_simulation_details(self, statistics):
        for protocol, stats in zip(['LAA', 'OLAA_T', 'OLAA_R'], statistics):
            print(f"Protocol: {protocol}")
            print(f"Throughput: {stats['throughput']} MB")
            print(f"Max Rendezvous Slot: {stats['max_rendezvous_slot']}")
            print(f"Average Time to Rendezvous: {stats['avg_time_to_rendezvous']}\n")

    def plot_statistics(self, statistics):
        labels = ['LAA', 'OLAA_T', 'OLAA_R']
        
        # Throughput plot
        throughput_values = [stat['throughput'] for stat in statistics]
        plt.figure(figsize=(10, 6))
        plt.bar(labels, throughput_values, color=['#4CAF50', '#FFC107', '#2196F3'])
        plt.xlabel('Protocol')
        plt.ylabel('Throughput (MB)')
        plt.title('Throughput Comparison')
        plt.show()

        # Max Rendezvous Slot plot
        max_rendezvous_values = [stat['max_rendezvous_slot'] for stat in statistics]
        plt.figure(figsize=(10, 6))
        plt.bar(labels, max_rendezvous_values, color=['#4CAF50', '#FFC107', '#2196F3'])
        plt.xlabel('Protocol')
        plt.ylabel('Max Rendezvous Slot')
        plt.title('Max Rendezvous Slot Comparison')
        plt.show()

        # Average Time to Rendezvous plot
        avg_time_rendezvous_values = [stat['avg_time_to_rendezvous'] for stat in statistics]
        plt.figure(figsize=(10, 6))
        plt.bar(labels, avg_time_rendezvous_values, color=['#4CAF50', '#FFC107', '#2196F3'])
        plt.xlabel('Protocol')
        plt.ylabel('Average Time to Rendezvous')
        plt.title('Average Time to Rendezvous Comparison')
        plt.show()

# Main execution
if __name__ == '__main__':
    # Run simulation
    simulator = Simulator(seed=42)
    simulator.run_simulation()
