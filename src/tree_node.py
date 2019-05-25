from anytree import NodeMixin

from src.filesize.filesize import FileSize


class TreeNode(NodeMixin):
    def __init__(self, name, parent=None):
        super(TreeNode, self).__init__()
        self.filesize = FileSize.from_int(0)
        self.name = name
        self.parent = parent
        self.horizontal_desc = None

    def get_horizontal_desc(self):
        return '{}: {}'.format(self.name, str(self.filesize)) if not self.horizontal_desc else self.horizontal_desc
