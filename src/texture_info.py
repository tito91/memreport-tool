from src.filesize.filesize import FileSize
from src.respath import ResPath


class TextureInfo:
    def __init__(self, text):
        items = text.split(', ')

        self.dimensions = items[2].split(' ')[0].split('x')
        self.filesize = FileSize.from_int(int(items[2].split(' ')[1][1:]), 'kb')
        self.format = items[3]
        self.tex_group = items[4]
        self.respath = ResPath(items[5])
        self.is_streaming = True if items[6] == 'YES' else False
        self.usage_count = items[7]

    def __str__(self):
        return 'Name: {}, Dimensions: {}x{}, Size[kb]: {}, Format: {}, TexGroup: {}, IsStreaming: {}, Usages: {}'.format(
            self.respath.chunks[-1], self.dimensions[0], self.dimensions[1],
            self.filesize.get_in_unit('kb'), self.format, self.tex_group, self.is_streaming, self.usage_count)
