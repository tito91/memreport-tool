from src.texture_info import TextureInfo
from src.texture_info_tree import TextureInfoTree


class MemReport:
    def __init__(self, file_path, size_threshold=None):
        self.tree = None
        self.size_threshold = size_threshold
        self.file = open(file_path, 'r')
        self.parse_file()

    def parse_file(self):
        texture_block_reached = False
        texture_block_start_line_id = 0

        all_lines = self.file.readlines()

        texture_info_list = []

        for line_id, line in zip(range(len(all_lines)), all_lines):
            if line.startswith('Listing all textures') and not texture_block_reached:
                texture_block_reached = True
                texture_block_start_line_id = line_id + 1

            if texture_block_reached and line.startswith('Total'):
                break

            if texture_block_reached and line_id > texture_block_start_line_id and not line.isspace():
                info = TextureInfo(line)
                if self.size_threshold and info.size_kb > self.size_threshold:
                    texture_info_list.append(info)

        self.tree = TextureInfoTree(texture_info_list)
