class WedgeData:
    def __init__(self, name, filesize, color, hori_desc, node_id=-1, is_filler=False):
        self.name = name
        self.node_id = node_id
        self.filesize = filesize
        self.color = color
        self.is_filler = is_filler

        self.description = hori_desc
