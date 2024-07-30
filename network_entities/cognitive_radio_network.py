from network_entities.channel import Channel
from network_entities.primary_user import PrimaryUser
from network_entities.secondary_user import SecondaryUser
from network_entities.attacker import Attacker

class CognitiveRadioNetwork:
    def __init__(self, params):
        self.params = params
        self.protocol = params['protocol']
        self.num_time_slots_per_cycle = self.params['num_slots_per_cycle']
        self.num_cycles = self.params['num_cycles']
        self.elp_rotations = self.get_elp_rotations()
        self.channels = [Channel(ch['channel_id'], ch['capacity']) for ch in self.params['channels']]
        self.num_channels = len(self.channels)
        self.time_slot_requests = [[[] for _ in range(self.num_time_slots_per_cycle)] for _ in range(self.num_channels)]
        self.allocation_schedule = [[[] for _ in range(self.num_time_slots_per_cycle)] for _ in range(self.num_channels)]
        self.primary_users = [PrimaryUser(pu['lambda_rates']) for pu in self.params['primary_users']]

        self.secondary_users = [SecondaryUser(
            network=self,
            user_id=su['user_id'],
            user_elp_id=su['elp_id'],
            user_channels=[self.channels[i-1] for i in su['user_channels']],
            rate=su['rate'],
            network_channels = self.channels,
            elp_rotations=self.elp_rotations,
            protocol=params['protocol']
        ) for su in self.params['secondary_users']]

        self.attackers = [Attacker(att['channel_id'], att['interference_probability']) for att in self.params['attackers']]

 
        self.throughput = 0
        self.rendezvous_matrix = [[None for _ in range(len(self.secondary_users))] for _ in range(len(self.secondary_users))]
        self.total_slots = self.num_time_slots_per_cycle * self.num_cycles
        


        # DEBUG COUNTERS
        self.slot_trans =0
        self.inteference_times = 0
        self.no_tx_user = 0
        self.attacker_interfere = 0
        self.primary_user_interfere = 0
        self.channel_interfere = [0,0,0]

    def get_elp_rotations(self):
        elp_sequence = self.params['elp_sequence']
        elp_order = self.params['elp_order']
        rotations = [elp_sequence[i:] + elp_sequence[:i] for i in range(2 * (elp_order + 1))]
        return rotations

    def process_requests(self):
        for time_slot in range(len(self.time_slot_requests[0])):
            for channel in range(self.num_channels):
                requests = self.time_slot_requests[channel][time_slot]
                self.process_channel_requests(channel, time_slot, requests)

    def process_channel_requests(self, channel, time_slot, requests):
        # Handle reception requests
        self.allocate_reception_requests(channel, time_slot, requests)

        # Handle transmission requests
        total_rate = sum(req['rate'] for req in requests if req['mode'] == 'T')
        if total_rate <= self.channels[channel].capacity:
            self.allocate_transmission_requests(channel, time_slot, requests)

    def allocate_reception_requests(self, channel, time_slot, requests):
        for req in requests:
            if req['mode'] == 'R':
                self.allocation_schedule[channel][time_slot].append(req)

    def allocate_transmission_requests(self, channel, time_slot, requests):
        for req in requests:
            if req['mode'] == 'T':
                self.allocation_schedule[channel][time_slot].append(req)

    def generate_primary_user_access_patterns(self):
        return [pu.generate_access_pattern(self.num_time_slots_per_cycle) for pu in self.primary_users]

    def generate_attacker_interference_patterns(self):
        return  {attacker.channel_id: attacker.generate_interference_pattern(self.num_time_slots_per_cycle) for attacker in self.attackers}

    def execute_slot_traffic(self, time_slot, primary_user_access_patterns, attackers_interference_pattern, cycle):
        self.slot_trans +=1
        for channel in range(self.num_channels):
            primary_user_activity = any(
                pattern[channel][time_slot] == 'active' for pattern in primary_user_access_patterns
            )

            attacker_interference = attackers_interference_pattern.get(channel + 1, [0] * self.num_time_slots_per_cycle)
            interference = primary_user_activity or attacker_interference[time_slot]

            tx_users_req = [req for req in self.allocation_schedule[channel][time_slot] if req['mode'] == 'T']

            if interference or not tx_users_req:
                continue

            # Update throughput
            self.throughput += len(tx_users_req)

            # Update rendezvous matrix
            for tx_user_req in tx_users_req:
                for user_req in self.allocation_schedule[channel][time_slot]:
                    tx_id = tx_user_req['user_id']
                    user_id = user_req['user_id']
                    if self.rendezvous_matrix[tx_id][user_id] is None:
                        self.rendezvous_matrix[tx_id][user_id] = time_slot + cycle*self.num_time_slots_per_cycle
                        self.rendezvous_matrix[user_id][tx_id] = time_slot + cycle*self.num_time_slots_per_cycle
   
    def execute_cycle_traffic(self, cycle):
        print(f"Executing Cycle {cycle + 1}/{self.num_cycles}")
        primary_user_access_patterns = self.generate_primary_user_access_patterns()
        attackers_interference_pattern = self.generate_attacker_interference_patterns()
        for time_slot in range(self.num_time_slots_per_cycle):
            self.execute_slot_traffic(time_slot, primary_user_access_patterns, attackers_interference_pattern, cycle)

    def post_cycle(self):
        self.time_slot_requests = [[[] for _ in range(len(self.time_slot_requests[0]))] for _ in range(self.num_channels)]
        self.allocation_schedule = [[[] for _ in range(self.num_time_slots_per_cycle)] for _ in range(self.num_channels)]
    
    def execute_traffic(self):
        for cycle in range(self.num_cycles):
            for user in self.secondary_users:
                user.post_requests_to_network(self.time_slot_requests)
            self.process_requests()
            self.execute_cycle_traffic(cycle)
            self.post_cycle()



    def calculate_statistics(self):
        # Check for None entries and raise ValueError if any exist excluding the diagonal
        if any(self.rendezvous_matrix[i][j] is None for i in range(len(self.rendezvous_matrix)) for j in range(len(self.rendezvous_matrix))):
            raise ValueError("Rendezvous matrix contains None entries indicating incomplete rendezvous.")

        # Find the maximum slot after which rendezvous occurred for all pairs excluding the diagonal
        max_rendezvous_slot = max(self.rendezvous_matrix[i][j] for i in range(len(self.rendezvous_matrix)) for j in range(len(self.rendezvous_matrix)))

        # Calculate the average time to rendezvous excluding the diagonal
        total_rendezvous_time = sum(self.rendezvous_matrix[i][j] for i in range(len(self.rendezvous_matrix)) for j in range(len(self.rendezvous_matrix)) if i != j)
        num_secondary_users = len(self.secondary_users)
        avg_time_to_rendezvous = total_rendezvous_time / (2 * num_secondary_users)

        # Calculate the normalized throughput
        normalized_throughput = self.throughput / 100 # Each transaction is 100KB

        return {
            'throughput': normalized_throughput,
            'max_rendezvous_slot': max_rendezvous_slot,
            'avg_time_to_rendezvous': avg_time_to_rendezvous
        }
        
 
