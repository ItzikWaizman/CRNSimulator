import matplotlib.pyplot as plt
from netowrk_entities_utils import *

class PrimaryUser:
    def __init__(self, lambda_rates):
        self.lambda_rates = lambda_rates  # List of lambda rates for each channel
        self.access_pattern = None  # Field to store the access pattern
    
    def generate_access_pattern(self, num_slots):
        self.access_pattern = generate_access_pattern(self.lambda_rates, num_slots)
        return self.access_pattern
    
    def plot_access_pattern(self):
        if self.access_pattern is None:
            raise ValueError("Access pattern has not been generated yet.")
        
        num_channels, num_slots = self.access_pattern.shape
        
        for channel in range(num_channels):
            time_slots = self.access_pattern[channel]
            
            plt.figure(figsize=(12, 4))
            plt.stem(time_slots == 'active', use_line_collection=True)
            plt.title(f'User Channel Access Time Slots (Channel {channel + 1})')
            plt.xlabel('Time Slot')
            plt.ylabel('Active (1) / Idle (0)')
            plt.show()