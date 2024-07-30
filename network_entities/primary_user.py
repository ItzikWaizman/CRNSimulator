import numpy as np
import matplotlib.pyplot as plt

def generate_access_pattern(lambda_rates, num_slots):
    num_channels = len(lambda_rates)
    access_pattern = np.empty((num_channels, num_slots), dtype='<U6')  # '<U6' specifies a Unicode string of up to 6 characters
    
    for channel in range(num_channels):
        lambda_rate = lambda_rates[channel]
        p = 1 - np.exp(-lambda_rate)
        idle_slots = np.random.geometric(p, size=num_slots)
        access_slots = np.cumsum(idle_slots)
        access_slots = access_slots[access_slots < num_slots]
        
        time_slots = np.array(['idle'] * num_slots, dtype='<U6')
        time_slots[access_slots] = 'active'
        access_pattern[channel] = time_slots
    
    return access_pattern

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
            plt.stem(time_slots == 'active')
            plt.title(f'User Channel Access Time Slots (Channel {channel + 1})')
            plt.xlabel('Time Slot')
            plt.ylabel('Active (1) / Idle (0)')
            plt.show()
