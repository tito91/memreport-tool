class WedgeData:
    def __init__(self, name, filesize, color, hori_desc, is_filler=False):
        self.name = name
        self.filesize = filesize
        self.color = color
        self.is_filler = is_filler

        self.description = hori_desc
