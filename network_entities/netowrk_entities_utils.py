import numpy as np

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

def get_elp_rotations(elp_sequence, elp_order):
    rotations = [elp_sequence[i:] + elp_sequence[:i] for i in range(2 * (elp_order + 1))]
    return rotations