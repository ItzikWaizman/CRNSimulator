import json

class Parameters:
    def __init__(self,  protocol='LAA', config_path=None):
        self.params = dict()

        if config_path:
            self.load_params_from_file(config_path)
        else:
            self.set_default_params(protocol)

    def set_default_params(self, protocol):
        """ Network Topology Parameters """

        # channels - Dictionary. Defines the channels in the network, including the channel id and the corresponding capacity.
        self.params['channels'] = [
            {'channel_id': 1, 'capacity': 1},
            {'channel_id': 2, 'capacity': 1},
            {'channel_id': 3, 'capacity': 1},
        ]

        # primary_users - Dictionary. Defines the primary users in the network, including the user id and lambda_rates (of the exponential distribution) for each channel.
        self.params['primary_users'] = [
            {'primary_user_id': 0, 'lambda_rates' : [0.01, 0.8, 0.02]}
        ]

        # secondary_users - Dictionary. Defines the secondary users in the netowrk, including user id, the channel set for each user, transmission rate ELP id.
        self.params['secondary_users'] = [
            {'user_id': 0, 'user_channels': [1, 2], 'rate': 0.3, 'elp_id': "01"},
            {'user_id': 1, 'user_channels': [1, 3], 'rate': 0.2, 'elp_id': "13"},
            {'user_id': 2, 'user_channels': [2, 3], 'rate': 0.1, 'elp_id': "21"},
        ]

        # attackers - Dictionary. Defines the attackers in the network, including the target channel and the probability of interference.
        self.params['attackers'] = [
            {'channel_id': 2, 'interference_probability': 0.7}
        ]

        # num_intelligent_attackers - Integer. Defines how many intelligent attackers will be used during the simulation.
        self.params['num_intelligent_attackers'] = 0
        
        # intelligent_attackers_inter_prob - Float. Indicates the interference probability of an intelligent attacker.
        self.params['intelligent_attackers_inter_prob'] = 0.9

        """ Network Topology Parameters """

        # protocol - String. Defines the protocol that will be used to generate a hopping sequence. The options are 'LAA', 'OLAA_T', 'OLAA_R'.
        self.params['protocol'] = protocol

        """ Protocol Parameters """
        # elp_id_length - Integer. Defines the length of Extended Langford's ID that will be assigned to each user.
        self.params['elp_id_length'] = 2

        # elp_order - Integer. Must be congruent to 0 or 3 modulo 4. Defines the order of ELP sequence that is used to generate hopping matrices.
        self.params['elp_order'] = 3

        # num_channels - Integer. indicates the number of channels in the network.
        self.params['num_channels'] = len(self.params['channels'])

        # num_sub_cols - Integer. Indicates the number of sub columns in each column. Vary according to the protocol (for 'OLAA_R' it is twice as the value of 'OLAA_T' and 'LAA').
        self.params['num_sub_col'] = 4 if self.params['protocol'] == 'OLAA_R' else 2

        # num_cols - Integer. Indicates the number of columns in the hooping matrix that will be generated during the simulation.
        self.params['num_cols'] = self.params['elp_id_length'] + 1

        # num_frames_per_sub_col - Integer. Indicates the number of frames in each sub column.
        self.params['num_frames_per_sub_col'] = 2 * (self.params['elp_order'] + 1)

        # num_slots_per_frame - Integer. Indicates the number of time slot in each frame. Vary according to the protocol (for 'OLAA_T' it is twice as the value of 'OLAA_R' and 'LAA').
        self.params['num_slots_per_frame'] = 4 * self.params['num_channels'] if self.params['protocol'] == 'OLAA_T' else 2 * self.params['num_channels']

        # num_slots_per_cycle - Integer. Indicates the number of time slots in one cycle (one sequence hopping).
        self.params['num_slots_per_cycle'] = self.params['num_cols'] * self.params['num_sub_col'] * self.params['num_frames_per_sub_col'] * self.params['num_slots_per_frame']

        # num cycles - Integers. Indicates the number of cycles that will be used to generate traffic in the network. 'LAA' num_cycles must be twice the value of 'OLAA_T' and 'OLAA_R'.
        self.params['num_cycles'] = 16 if self.params['protocol'] == 'LAA' else 8

        # elp_sequence - List of chars. An extended Langford's sequence that will be used to generate hopping matrices.
        self.params['elp_sequence'] = ['0', '0', '3', '1', '2', '1', '2', '3']
        
    def load_params_from_file(self, config_path):
        with open(config_path, 'r') as file:
            self.params = json.load(file)

    def save_params_to_file(self, config_path):
        with open(config_path, 'w') as file:
            json.dump(self.params, file, indent=4)
