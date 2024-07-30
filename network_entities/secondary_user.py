import matplotlib as plt
import numpy as np
from netowrk_entities_utils import *

class SecondaryUser:
    def __init__(self, network, protocol, post_request_db, user_id, user_channels, network_channels, rate, user_elp_id, elp_rotations, elp_order = 3):
        self.network = network
        self.user_id = user_id
        self.user_elp_id = user_elp_id 
        self.user_channels = user_channels
        self.network_channels = network_channels
        self.num_user_channels = len(user_channels)
        self.num_network_channels = len(network_channels)
        self.rate = rate
        self.elp_order = elp_order
        self.elp_rotations = elp_rotations
        self.num_sub_columns = self.num_user_channelsl
        self.num_frames_in_sub_column = 2 * (self.elp_order + 1)
        self.num_slots_in_frame = 2 * self.num_network_channels
        self.post_request_db = post_request_db
        self.protocol = protocol
        self.channel_usage_probabilities = None

    def calculate_pu_usage_probabilities(self):
        i=0
        for channel in self.user_channels:
            combined_lambda = sum(pu.lambda_rates[channel.channel_id - 1] for pu in self.network.primary_users)
            self.pu_usage_probabilities[i] = 1 - np.exp(-combined_lambda)
            i+=1

    def calculate_channel_usage_probabilities(self):
        pu_usage_probabilities = self.calculate_pu_usage_probabilities()
        denominator = sum(1 - pu_usage_probabilities[j] for j in range(self.num_user_channels))
        channel_usage_probabilities =  [(1 - pu_usage_probabilities[i]) / denominator for i in range(self.num_user_channels)]
        return channel_usage_probabilities

    def post_cycle_requests(self):
        hopping_matrix = self.gen_protocol_matrix(self.protocol)
        hooping_sequence = self.derive_hopping_sequence(hopping_matrix)

    def gen_frame_matrix(self):
        user_elp_id = [int(x) for x in self.user_elp_id]
        nt = 2

        # Initialize the hopping matrix
        frame_matrix = []

        # The first column is built by repeating the 4-frame pattern TTRR
        first_column = ['T', 'T', 'R', 'R'] * (self.num_sub_columns * 2 * (self.elp_order + 1) // 4)
        frame_matrix.append(first_column)

        # For each y from 1 to l (number of sub-columns)
        for _ in range(len(self.user_elp_id)):
            column = []
            pattern_pi = np.random.choice(self.elp_rotations)

            for z in range(self.num_sub_columns):
                sub_column = []

                min_bound = min(user_elp_id[z] % (self.elp_order + 1), (user_elp_id[z] + nt) % (self.elp_order + 1))
                max_bound = max(user_elp_id[z] % (self.elp_order + 1), (user_elp_id[z] + nt) % (self.elp_order + 1))

                for w in range(self.num_frames_in_sub_column):
                    if min_bound <= pattern_pi[w] <= max_bound:
                        sub_column.append('T')
                    else:
                        sub_column.append('R')

                column.append(sub_column)

            frame_matrix.append(column)
        return frame_matrix

    def gen_laa_hopping_matrix(self):
        frame_matrix = self.gen_frame_matrix()
        hopping_matrix = []
        network_channel_ids = [ch.channel_id for ch in self.network_channels]
        user_channel_ids = [ch.channel_id for ch in self.user_channels]
        iterator = 0
        # Process the rest of the columns
        for column in frame_matrix:
            new_column = []
            for sub_column in column:
                for frame in sub_column:
                    if frame == 'T':
                        # T frame: Take 2 permutations of the network channels
                        slots = np.random.permutation(network_channel_ids).tolist() + np.random.permutation(network_channel_ids).tolist()
                        # Replace channels not in user channels
                        slots = [np.random.choice(user_channel_ids) if ch not in user_channel_ids else ch for ch in slots]
                        slots = [(np.random.choice(user_channel_ids), 'T') if ch not in user_channel_ids else (ch, 'T') for ch in slots]
                        new_column.extend(slots)
                    else:
                        # R frame: Randomly choose a channel from user channels and assign to the whole sub-column
                        chosen_channel = user_channel_ids[iterator]
                        slots = [(chosen_channel, 'R')] * self.num_slots_in_frame
                        new_column.extend(slots)
                iterator += 1
                iterator = iterator % len(user_channel_ids)
            
            hopping_matrix.append(new_column)
        
        return hopping_matrix

    def gen_olaa_t_hopping_matrix(self):
        frame_matrix = self.gen_frame_matrix()
        hopping_matrix = []
        network_channel_ids = [ch.channel_id for ch in self.network_channels]
        user_channel_ids = [ch.channel_id for ch in self.user_channels]
        max_prob_channel_id = self.user_channels[np.argmax(self.channel_usage_probabilities)].channel_id
        iterator = 0

        for column in frame_matrix:
            new_column = []
            for sub_column in column:
                for frame in sub_column:
                    if frame == 'T':
                        # T frame: Default slots
                        default_slots = np.random.permutation(network_channel_ids).tolist() + np.random.permutation(network_channel_ids).tolist()
                        default_slots = [(np.random.choice(user_channel_ids), 'T') if ch not in user_channel_ids else (ch, 'T') for ch in default_slots]
                        
                        # T frame: Adjustment slots
                        adjustment_slots = [(max_prob_channel_id, 'T')] * len(default_slots)

                        # Alternate between default and adjustment slots
                        slots = [None] * (2 * len(default_slots))
                        slots[::2] = default_slots
                        slots[1::2] = adjustment_slots
                        
                        new_column.extend(slots)
                    else:
                        # R frame: Assign a channel from user channels in a round-robin manner
                        chosen_channel = user_channel_ids[iterator]
                        slots = [(chosen_channel, 'R')] * (2 * self.num_slots_in_frame)
                        new_column.extend(slots)
                iterator += 1
                iterator = iterator % len(user_channel_ids)
            
            hopping_matrix.append(new_column)
        
        return hopping_matrix

    def gen_olaa_r_frame_matrix(self):
        user_elp_id = [int(x) for x in self.user_elp_id]
        nt = 2

        # Initialize the hopping matrix
        frame_matrix = []

        # The first column is built by repeating the 4-frame pattern TTRR
        first_column = ['T', 'T', 'R', 'R'] * (self.num_sub_columns * 2 * (self.elp_order + 1) // 4)
        frame_matrix.append(first_column)

        # For each y from 1 to l (number of sub-columns)
        for _ in range(len(self.user_elp_id)):
            column = []
            pattern_pi = np.random.choice(self.elp_rotations)

            for z in range(2*self.num_sub_columns):
                sub_column = []

                min_bound = min(user_elp_id[z] % (self.elp_order + 1), (user_elp_id[z] + nt) % (self.elp_order + 1))
                max_bound = max(user_elp_id[z] % (self.elp_order + 1), (user_elp_id[z] + nt) % (self.elp_order + 1))

                for w in range(self.num_frames_in_sub_column):
                    if min_bound <= pattern_pi[w] <= max_bound:
                        sub_column.append('T')
                    else:
                        sub_column.append('R')

                column.append(sub_column)

            frame_matrix.append(column)
        return frame_matrix

    def gen_olaa_r_hopping_matrix(self):
        frame_matrix = self.gen_olaa_r_frame_matrix()
        hopping_matrix = []
        network_channel_ids = [ch.channel_id for ch in self.network_channels]
        user_channel_ids = [ch.channel_id for ch in self.user_channels]
        max_prob_channel_id = self.user_channels[np.argmax(self.channel_usage_probabilities)].channel_id
        iterator = 0

        for column in frame_matrix:
            new_column = []
            for sub_column in column:
                j = 0
                for frame in sub_column:
                    if frame == 'T':
                        # T frame: Take 2 permutations of the network channels
                        slots = np.random.permutation(network_channel_ids).tolist() + np.random.permutation(network_channel_ids).tolist()
                        # Replace channels not in user channels
                        slots = [np.random.choice(user_channel_ids) if ch not in user_channel_ids else ch for ch in slots]
                        slots = [(np.random.choice(user_channel_ids), 'T') if ch not in user_channel_ids else (ch, 'T') for ch in slots]
                        new_column.extend(slots)
                    else:
                        # default sub_column
                        if (j%2 == 0):
                            chosen_channel = user_channel_ids[iterator]
                            slots = [(chosen_channel, 'R')] * self.num_slots_in_frame
                            new_column.extend(slots)
                        
                        # adjustment sub_column
                        else:
                            slots = [(max_prob_channel_id, 'R')] * self.num_slots_in_frame
                            new_column.extend(slots)
                j += 1
                iterator += 1
                iterator = iterator % len(user_channel_ids)
            
            hopping_matrix.append(new_column)
        
        return hopping_matrix

    def gen_hopping_matrix(self):
        if self.protocol == 'LAA':
            return self.gen_laa_hopping_matrix()
        elif self.protocol == 'OLAA_T':
            return self.gen_olaa_t_hopping_matrix()
        elif self.protocol == 'OLAA_R':
            return self.gen_olaa_r_hopping_matrix()
        else:
            raise ValueError(f"Unsupported protocol: {self.protocol}")
    
    def gen_hopping_sequence(self, hopping_matrix):
        hopping_matrix = self.gen_hopping_matrix()
        hopping_sequence = []

        # Iterate over each row and column of the hopping matrix
        for row in range(len(hopping_matrix[0])):
            for col in range(len(hopping_matrix)):
                hopping_sequence.append(hopping_matrix[col][row])
        
        return hopping_sequence

    def post_requests_to_network(self):
        hopping_sequence = self.gen_hopping_sequence()
        time_slot = 0
        for channel_id, mode in hopping_sequence:
            request = {
                'user_id': self.user_id,
                'channel': channel_id,
                'mode': mode,
                'rate': self.rate if mode == 'T' else 0  # Use the user's rate for 'T' mode, 0 for 'R' mode
            }
            self.post_request_db[channel_id-1][time_slot].append(request)
            time_slot += 1