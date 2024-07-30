import numpy as np

class Attacker:
    def __init__(self, channel_id, interference_probability):
        self.channel_id = channel_id
        self.interference_probability = interference_probability
        self.interference_slots = []

    def generate_interference_pattern(self, num_time_slots):
        self.interference_slots = np.random.choice(
            [0, 1], size=num_time_slots, p=[1 - self.interference_probability, self.interference_probability]
        )
        return self.interference_slots