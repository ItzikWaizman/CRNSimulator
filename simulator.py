from config import Parameters
from network_entities.cognitive_radio_network import CognitiveRadioNetwork
import matplotlib.pyplot as plt

class Simulator:
    def __init__(self, params):
        self.params = params
        self.network = CognitiveRadioNetwork(params)

    def run_simulation(self):
        self.network.execute_traffic()

    def print_simulation_details(self):
        statistics = self.network.calculate_statistics()
        print(f"Throughput: {statistics['throughput']} MB")
        print(f"Max Rendezvous Slot: {statistics['max_rendezvous_slot']}")
        print(f"Average Time to Rendezvous: {statistics['avg_time_to_rendezvous']}")

    def post_simulation(self):
        statistics = self.network.calculate_statistics()
        self.plot_statistics(statistics)

    def plot_statistics(self, statistics):
        labels = ['LAA', 'OLAA_T', 'OLAA_R']
        protocols = ['LAA']

        # Throughput plot
        throughput_values = [statistics['throughput']]
        plt.figure(figsize=(10, 6))
        plt.bar(labels[:len(throughput_values)], throughput_values, color=['#4CAF50'])
        plt.xlabel('Protocol')
        plt.ylabel('Throughput (MB)')
        plt.title('Throughput Comparison')
        plt.show()

        # Max Rendezvous Slot plot
        max_rendezvous_values = [statistics['max_rendezvous_slot']]
        plt.figure(figsize=(10, 6))
        plt.bar(labels[:len(max_rendezvous_values)], max_rendezvous_values, color=['#FFC107'])
        plt.xlabel('Protocol')
        plt.ylabel('Max Rendezvous Slot')
        plt.title('Max Rendezvous Slot Comparison')
        plt.show()

        # Average Time to Rendezvous plot
        avg_time_rendezvous_values = [statistics['avg_time_to_rendezvous']]
        plt.figure(figsize=(10, 6))
        plt.bar(labels[:len(avg_time_rendezvous_values)], avg_time_rendezvous_values, color=['#2196F3'])
        plt.xlabel('Protocol')
        plt.ylabel('Average Time to Rendezvous')
        plt.title('Average Time to Rendezvous Comparison')
        plt.show()
