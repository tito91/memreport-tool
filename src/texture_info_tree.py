from anytree import Resolver, ChildResolverError, RenderTree

from src.texture_info import TextureInfo
from src.tree_node import TreeNode


class TextureInfoTree:
    def __init__(self, texture_info_list):
        r = Resolver('name')
        self.root = TreeNode('Root')

        for info in texture_info_list:
            respath = info.respath

            cur_parent = self.root
            cur_parent.size_kb += info.size_kb
            cur_node = None
            for chunk in respath.chunks:
                try:
                    cur_node = r.get(cur_parent, chunk)
                    cur_parent = cur_node
                except ChildResolverError:
                    cur_node = TreeNode(chunk, cur_parent)
                    cur_parent = cur_node
                finally:
                    cur_node.size_kb += info.size_kb

    @staticmethod
    def make_simple_sample():
        info1 = TextureInfo('0x0 (16384 KB, ?), 0x0 (16384 KB), PF_FloatRGBA, TEXTUREGROUP_World,          /tex1.tex1, NO, 0')
        info2 = TextureInfo('1480x1486 (8591 KB, ?), 1480x1486 (8591 KB), PF_B8G8R8A8, TEXTUREGROUP_World, /VideosAssets /dir/tex2.tex2, NO, 0')
        info3 = TextureInfo('1920x1080 (8100 KB, ?), 1920x1080 (8100 KB), PF_B8G8R8A8, TEXTUREGROUP_World, /LoadingScreen/tex3.tex3, NO, 0')

        return TextureInfoTree([info1, info2, info3]).root

    @staticmethod
    def make_sample():
        info1 = TextureInfo('0x0 (16384 KB, ?), 0x0 (16384 KB), PF_FloatRGBA, TEXTUREGROUP_World, /Engine/MapTemplates/Sky/DaylightAmbientCubemap.DaylightAmbientCubemap, NO, 0')
        info2 = TextureInfo('1480x1486 (8591 KB, ?), 1480x1486 (8591 KB), PF_B8G8R8A8, TEXTUREGROUP_World, /Game/BeeSimulator/UI/Tutorial/VideosAssets/T_tutorialVideoFrame.T_tutorialVideoFrame, NO, 0')
        info3 = TextureInfo('1920x1080 (8100 KB, ?), 1920x1080 (8100 KB), PF_B8G8R8A8, TEXTUREGROUP_World, /Game/BeeSimulator/UI/LoadingScreen/T_Loadscreen_2.T_Loadscreen_2, NO, 0')

        return TextureInfoTree([info1, info2, info3]).root


if __name__ == '__main__':
    TextureInfoTree.make_simple_sample()
