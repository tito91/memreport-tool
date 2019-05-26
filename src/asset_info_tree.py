from anytree import Resolver, ChildResolverError

from src.tree_node import TreeNode


class AssetInfoTree:
    def __init__(self, texture_info_list):
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
