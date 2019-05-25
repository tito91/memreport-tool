from src.filesize.filesize import FileSize
from src.respath import ResPath


class TextureInfo:
    def __init__(self, text):
        items = text.split(', ')

        self.dimensions = items[2].split(' ')[0].split('x')
        self.filesize = FileSize.from_string(''.join(items[2].split(' ')[1:])[1:-1])
        self.format = items[3]
        self.tex_group = items[4]
        self.respath = ResPath(items[5])
        self.is_streaming = True if items[6] == 'YES' else False
        self.usage_count = items[7]

    def __str__(self):
        return 'Name: {}, Dimensions: {}x{}, Size: {}, Format: {}, TexGroup: {}, IsStreaming: {}, Usages: {}'.format(
            self.respath.chunks[-1], self.dimensions[0], self.dimensions[1],
            str(self.filesize), self.format, self.tex_group, self.is_streaming, self.usage_count)


class AssetInfo:
    def __init__(self, text):
        items = text.split()

        self.respath = ResPath(items[1])
        self.filesize = FileSize.from_string(items[4] + 'kb')

    def __str__(self):
        return 'Name {}, Size: {}'.format(self.respath.chunks[-1], str(self.filesize))
