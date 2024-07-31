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
class IntelligentAttacker(Attacker):
    def __init__(self, interference_probability):
        super().__init__(channel_id=None, interference_probability=interference_probability)
        self.state = 'listening'
        self.target_channels = []

    def set_attack_state(self, channel_id):
        if self.state == 'attacking':
            return
        # Listen for one cycle and determine the two most popular channels
        self.channel_id = channel_id
        self.state = 'attacking'

    def generate_interference_pattern(self, num_slots_per_cycle):
        if self.state == 'listening':
            return [0] * num_slots_per_cycle
        else:
            return np.random.choice([0, 1], size=num_slots_per_cycle, p=[1 - self.interference_probability, self.interference_probability])

