from src.asset_info import TextureInfo, AssetInfo


class TextureMemreportBlock:
    def __init__(self):
        self.starting_token = 'Listing all textures'
        self.starting_offset = 1
        self.info_class = TextureInfo

    @staticmethod
    def line_ends_block(line):
        return line.startswith('Total')


class SoundMemreportBlock:
    def __init__(self):
        self.starting_token = 'Obj List: class=SoundWave'
        self.starting_offset = 3
        self.info_class = AssetInfo

    @staticmethod
    def line_ends_block(line):
        return line.isspace()

