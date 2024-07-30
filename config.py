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

        self.params['channels'] = [
            {'channel_id': 1, 'capacity': 1},
            {'channel_id': 2, 'capacity': 1},
            {'channel_id': 3, 'capacity': 1},
        ]

        self.params['primary_users'] = [
            {'primary_user_id': 0, 'lambda_rates' : [0.001, 0.8, 0.002]}
        ]

        self.params['secondary_users'] = [
            {'user_id': 0, 'user_channels': [1, 2], 'rate': 0.3, 'elp_id': "01"},
            {'user_id': 1, 'user_channels': [1, 3], 'rate': 0.2, 'elp_id': "13"},
            {'user_id': 2, 'user_channels': [2, 3], 'rate': 0.1, 'elp_id': "21"},
        ]

        self.params['attackers'] = [
            {'channel_id': 2, 'interference_probability': 0.7}
        ]

        self.params['protocol'] = protocol

        """ LAA Protocol Parameters """
        self.params['elp_id_length'] = 2
        self.params['elp_order'] = 3
        self.params['num_channels'] = len(self.params['channels'])
        self.params['num_sub_col'] = 4 if self.params['protocol'] == 'OLAA_R' else 2
        self.params['num_cols'] = self.params['elp_id_length'] + 1
        self.params['num_frames_per_sub_col'] = 2 * (self.params['elp_order'] + 1)
        self.params['num_slots_per_frame'] = 4 * self.params['num_channels'] if self.params['protocol'] == 'OLAA_T' else 2 * self.params['num_channels']
        self.params['num_slots_per_cycle'] = self.params['num_cols'] * self.params['num_sub_col'] * self.params['num_frames_per_sub_col'] * self.params['num_slots_per_frame']
        self.params['num_cycles'] = 4 if self.params['protocol'] == 'LAA' else 2
        self.params['elp_sequence'] = ['0', '0', '3', '1', '2', '1', '2', '3']
        
    def load_params_from_file(self, config_path):
        with open(config_path, 'r') as file:
            self.params = json.load(file)

    def save_params_to_file(self, config_path):
        with open(config_path, 'w') as file:
            json.dump(self.params, file, indent=4)
