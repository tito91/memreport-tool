import numpy
from anytree import findall

from src.filesize.filesize import FileSize
from src.wedge_data import WedgeData

import matplotlib.pyplot as plt
from matplotlib.backend_bases import NavigationToolbar2


class Chart:
    def __init__(self, report):
        self._inner_size = 0.2
        self._outer_size = 1.25
        self.report = report
        self.current_plotted_root = None
        self._subplot = None

        self.root_history = []

        NavigationToolbar2.back = self._back_pressed

        self._figure, self._subplot = plt.subplots()
        self._plot_with_root(report.tree.root, record_history=False)

    def _back_pressed(self, *args):
        if self.root_history:
            new_root = self.root_history.pop()
            self._plot_with_root(new_root, record_history=False)

    def _plot_with_root(self, root, record_history=True):

        if self._subplot:
            self._subplot.clear()

        self._change_root(root, record_history)
        self._chart_data = self._parse_from_root(root)

        axis_count = len(self._chart_data)
        wedge_width = (self._outer_size - self._inner_size) / (axis_count + 1)

        self._wedge_series = []

        for x in range(axis_count):
            radius = self._outer_size - x * wedge_width
            sizes = [d.filesize.bytes for d in self._chart_data[x]]
            colors = [d.color for d in self._chart_data[x]]

            wedges, _ = self._subplot.pie(sizes, radius=radius, colors=colors,
                                          wedgeprops=dict(width=wedge_width, edgecolor='w'))
            self._wedge_series.append(wedges)

        self._wedge_series.reverse()

        self._wedge_annotation = self._subplot.annotate("", xy=(0, 0), xycoords="figure pixels", xytext=(20, 20),
                                                        textcoords="offset points",
                                                        bbox=dict(boxstyle="round", fc="w"),
                                                        arrowprops=dict(arrowstyle="->"))
        self._wedge_annotation.set_visible(False)

        if self.report.size_threshold.bytes:
            size_threshold_text = 'Assets under {} are hidden. Total size of such files: {}'.format(
                self.report.size_threshold, self.report.under_threshold_total_size)
            threshold_annotation = self._subplot.annotate(size_threshold_text, xy=(0, 0), xycoords="figure pixels",
                                                          xytext=(20, 20), textcoords="offset points",
                                                          bbox=dict(boxstyle="round", fc="w"))
            threshold_annotation.set_visible(True)

        self._background = self._figure.canvas.copy_from_bbox(self._subplot.bbox)

        self._figure.canvas.mpl_connect("motion_notify_event", self._hover)
        self._figure.canvas.mpl_connect("button_release_event", self._button_pressed)

        self._draw_cid = self._figure.canvas.mpl_connect('draw_event', self._grab_background)

        self._background = None

        plt.draw()

    def _change_root(self, new_root, record_history):
        if self.current_plotted_root and record_history:
            self.root_history.append(self.current_plotted_root)

        self.current_plotted_root = new_root

    def _grab_background(self, event=None):
        self._wedge_annotation.set_visible(False)

        self.safe_draw()

        self._background = self._figure.canvas.copy_from_bbox(self._figure.bbox)
        self._blit()

    def _blit(self):
        self._figure.canvas.restore_region(self._background)
        self._subplot.draw_artist(self._wedge_annotation)
        self._figure.canvas.blit(self._figure.bbox)

    def safe_draw(self):
        canvas = self._figure.canvas
        canvas.mpl_disconnect(self._draw_cid)
        canvas.draw()
        self._draw_cid = canvas.mpl_connect('draw_event', self._grab_background)

    @staticmethod
    def _parse_from_root(root):
        chart_data = []

        node_list = [root]
        while node_list:

            for n in node_list:
                if n.children:
                    break
            else:
                break

            children_flat_list = []
            wedge_info = []
            for node in node_list:
                wedge_info.extend([WedgeData.for_node(n) for n in node.children])
                children_sizes = [node.filesize.bytes for node in node.children]

                filling_space = node.filesize.bytes - sum(children_sizes)
                if filling_space > 0:
                    wedge_info.append(WedgeData.for_filler(filling_space))

                if node.children:
                    children_flat_list.extend(node.children)
                else:
                    children_flat_list.append(node)

            node_list = children_flat_list

            if node_list:
                chart_data.append(wedge_info)

        return chart_data

    def _update_annotation(self, pos, description):
        self._wedge_annotation.xy = pos
        self._wedge_annotation.set_text(description)
        self._wedge_annotation.get_bbox_patch().set_alpha(0.4)

    def _hover(self, event):
        if event.inaxes == self._subplot:
            pos = [event.x, event.y]
            for series_index, wedges in enumerate(self._wedge_series):
                for wedge_index, w in enumerate(wedges):
                    corresponding_data = self._chart_data[-series_index - 1][wedge_index]
                    if w.contains_point(pos) and not corresponding_data.is_filler:
                        description = corresponding_data.annotation_text
                        self._update_annotation(pos, description)
                        self._wedge_annotation.set_visible(True)
                        self._blit()
                        return
                    else:
                        self._wedge_annotation.set_visible(False)
            self._blit()

    def _button_pressed(self, event):
        if event.inaxes == self._subplot:
            pos = [event.x, event.y]
            for series_index, wedges in enumerate(self._wedge_series):
                for wedge_index, w in enumerate(wedges):
                    corresponding_data = self._chart_data[-series_index - 1][wedge_index]
                    if w.contains_point(pos) and corresponding_data.can_be_root:
                        node = findall(self.current_plotted_root, filter_=lambda n: n.id == corresponding_data.node_id)

                        if len(node) != 1:
                            raise RuntimeError('Invalid tree search result.')

                        self._plot_with_root(node[0])

                        return

    @staticmethod
    def show():
        plt.show()
