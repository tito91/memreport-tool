from src.filesize.filesize import FileSize
from src.memreport_blocks import TextureMemreportBlock, SoundMemreportBlock
from src.asset_info_tree import AssetInfoTree


class MemReport:
    asset_types = ['textures', 'sounds']

    asset_blocks = {'textures': TextureMemreportBlock(), 'sounds': SoundMemreportBlock()}

    def __init__(self, file_path, asset_type, size_threshold=None):
        self.tree = None
        self.size_threshold = size_threshold
        self.file = open(file_path, 'r')
        self.under_threshold_total_size = FileSize.from_int(0)
        self.parse_file(asset_type)

        self.asset_type_display_name = asset_type
        name_char_list = list(asset_type)
        name_char_list[0] = name_char_list[0].upper()
        self.asset_type_display_name = "".join(name_char_list)

    def parse_file(self, asset_type):
        texture_block_reached = False
        content_found = False
        texture_block_start_line_id = 0

        all_lines = self.file.readlines()

        block = MemReport.asset_blocks[asset_type]

        texture_info_list = []

        for line_id, line in zip(range(len(all_lines)), all_lines):
            if line.startswith(block.starting_token) and not texture_block_reached:
                texture_block_reached = True
                texture_block_start_line_id = line_id + block.starting_offset

            if texture_block_reached and content_found and block.line_ends_block(line):
                break

            if texture_block_reached and line_id > texture_block_start_line_id and not line.isspace():
                info = block.info_class(line)
                content_found = True
                if self.size_threshold:
                    if info.filesize.bytes > self.size_threshold.bytes:
                        texture_info_list.append(info)
                    else:
                        self.under_threshold_total_size.bytes += info.filesize.bytes
                else:
                    texture_info_list.append(info)

        self.tree = AssetInfoTree(texture_info_list)
