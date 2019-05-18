import matplotlib.pyplot as plt
from anytree import PreOrderIter

from src.texture_info_tree import make_sample


class TreePieChart:
    def __init__(self, root):
        self.root = root

    def make_chart(self):
        fig, ax = plt.subplots()

        print([node.name for node in PreOrderIter(self.root, maxlevel=2) if node != self.root])

        wedges, _ = ax.pie([1, 1, 1], wedgeprops=dict(width=0.3))

        annotation = ax.annotate("", xy=(0, 0), xycoords="figure pixels", xytext=(20, 20), textcoords="offset points",
                                 bbox=dict(boxstyle="round", fc="w"),
                                 arrowprops=dict(arrowstyle="->"))
        annotation.set_visible(False)

        def update_annotation(pos):
            annotation.xy = pos
            annotation.set_text('NAME')
            annotation.get_bbox_patch().set_alpha(0.4)

        def hover(event):
            if event.inaxes == ax:
                pos = [event.x, event.y]
                for i, w in enumerate(wedges):
                    if w.contains_point(pos):
                        update_annotation(pos)
                        annotation.set_visible(True)
                        break
                    else:
                        annotation.set_visible(False)
                fig.canvas.draw_idle()

        fig.canvas.mpl_connect("motion_notify_event", hover)

        plt.show()


if __name__ == '__main__':
    TreePieChart(make_sample()).make_chart()
