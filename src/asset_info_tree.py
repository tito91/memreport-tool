from anytree import Resolver, ChildResolverError, Walker

from src.tree_node import TreeNode


class AssetInfoTree:
    def __init__(self, texture_info_list):
        self.walker = Walker()

        r = Resolver('name')

        id = 0

        self.root = TreeNode('Root', id)

        id += 1

        for info in texture_info_list:
            respath = info.respath

            cur_parent = self.root
            cur_parent.filesize.bytes += info.filesize.bytes
            cur_node = None
            for chunk in respath.chunks:
                try:
                    cur_node = r.get(cur_parent, chunk)
                    cur_parent = cur_node
                except ChildResolverError:
                    cur_node = TreeNode(chunk, id, cur_parent)
                    cur_parent = cur_node

                    id += 1

                    if chunk == respath.chunks[-1]:
                        cur_node.horizontal_desc = str(info)

                finally:
                    cur_node.filesize.bytes += info.filesize.bytes

    def build_node_path(self, node):
        path = self.walker.walk(self.root, node)
        return '/'.join([tn.name for tn in path[2]])
