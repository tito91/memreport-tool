class GroupStats:
    def __init__(self, name):
        self.name = name

        self.total_count = 0
        self.non_pot_count = 0
        self.total_kbs = 0
        self.non_pot_kbs = 0

    def __str__(self):
        return "<{0}>: \n\tTotal count: {1}, \n\tTotal KBs: {2}, \n\tNon-POT count: {3}, \n\tNon-POT KBs: {4}".format(
            self.name, self.total_count, self.total_kbs, self.non_pot_count, self.non_pot_kbs)
        # return "<{0}>: Total KBs: {1}".format(self.name, self.total_kbs)

    def add(self, other):
        self.total_count += other.total_count
        self.non_pot_count += other.non_pot_count
        self.total_kbs += other.total_kbs
        self.non_pot_kbs += other.non_pot_kbs
