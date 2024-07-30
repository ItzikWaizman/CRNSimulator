class Channel:
    def __init__(self, channel_id, capacity):
        self.channel_id = channel_id
        self.capacity = capacity

    def __repr__(self):
        return f"Channel(channel_id={self.channel_id}, capacity={self.capacity})"