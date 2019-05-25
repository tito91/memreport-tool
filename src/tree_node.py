from anytree import NodeMixin

from src.filesize.filesize import FileSize


class TreeNode(NodeMixin):
    def __init__(self, name, parent=None):
        super(TreeNode, self).__init__()
        self.filesize = FileSize.from_int(0)
        self.name = name
        self.parent = parent
