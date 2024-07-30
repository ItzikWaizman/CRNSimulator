import numpy as np
import matplotlib as plt

def generate_access_pattern(lambda_rates, num_slots):
    num_channels = len(lambda_rates)
    access_pattern = np.empty((num_channels, num_slots), dtype='<U6')
    
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

def plot_estimated_pattern(self):
    if self.estimated_pattern is None:
        raise ValueError("Estimated pattern has not been generated yet.")
    
    num_channels, num_slots = self.estimated_pattern.shape
    
    for channel in range(num_channels):
        time_slots = self.estimated_pattern[channel]
        
        plt.figure(figsize=(12, 4))
        plt.stem(time_slots == 'active', use_line_collection=True)
        plt.title(f'Secondary User Estimated Channel Access Time Slots (Channel {channel + 1})')
        plt.xlabel('Time Slot')
        plt.ylabel('Active (1) / Idle (0)')
        plt.show()