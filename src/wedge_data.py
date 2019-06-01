import numpy

from src.filesize.filesize import FileSize


class WedgeData:

    filler_color = (0, 0, 0, 0)
    merged_color = (1, 0, 0, 1)

    def __init__(self, name, filesize, color, annotation_text, can_be_root, node_id=-1, is_filler=False):
        self.name = name
        self.node_id = node_id
        self.filesize = filesize
        self.color = color
        self.is_filler = is_filler
        self.can_be_root = can_be_root

        self.annotation_text = annotation_text

    @staticmethod
    def for_node(tree_node):
        name = tree_node.name
        filesize = tree_node.filesize
        color = numpy.random.rand(3, )

        annotation_text = tree_node.get_horizontal_desc()
        node_id = tree_node.id

        return WedgeData(name, filesize, color, annotation_text, tree_node.children, node_id)

    @staticmethod
    def for_filler(filling_space):
        return WedgeData('filler', FileSize.from_int(filling_space), WedgeData.filler_color, '', False, is_filler=True)

    @staticmethod
    def for_nodes_to_merge(nodes_to_merge):
        size = FileSize.from_int(sum([x.filesize.bytes for x in nodes_to_merge]))
        return WedgeData('merged', size, WedgeData.merged_color, 'Files below size threshold: {}'.format(str(size)), False)
