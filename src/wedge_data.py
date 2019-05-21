class WedgeData:
    def __init__(self, name, size_kb, color, is_filler=False):
        self.name = name
        self.size_kb = size_kb
        self.color = color
        self.is_filler = is_filler

        size_string = str(round(self.size_kb / 1024., 2)) + 'mb' if self.size_kb > 1024 else '{}kb'.format(size_kb)

        self.description = '{}: {}'.format(self.name, size_string)
