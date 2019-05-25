class WedgeData:
    def __init__(self, name, filesize, color, is_filler=False):
        self.name = name
        self.filesize = filesize
        self.color = color
        self.is_filler = is_filler

        self.description = '{}: {}'.format(self.name, str(self.filesize))
