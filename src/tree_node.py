from anytree import NodeMixin


class TreeNode(NodeMixin):
    def __init__(self, name, parent=None):
        super(TreeNode, self).__init__()
        self.size_kb = 0
        self.name = name
        self.parent = parent
