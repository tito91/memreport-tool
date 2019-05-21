import numpy

from src.wedge_data import WedgeData

import matplotlib.pyplot as plt


class Chart:
    inner_size = 0.2
    outer_size = 1.25

    figure = None
    subplot = None
    annotation = None
    chart_data = None
    wedge_series = None

    @staticmethod
    def from_tree(tree):
        Chart.chart_data = Chart._parse_tree(tree)

        Chart.figure, Chart.subplot = plt.subplots()

        axis_count = len(Chart.chart_data)
        wedge_width = (Chart.outer_size - Chart.inner_size) / (axis_count + 1)

        Chart.wedge_series = []

        for x in range(axis_count):
            radius = Chart.outer_size - x * wedge_width
            sizes = [d.size_kb for d in Chart.chart_data[x]]
            colors = [d.color for d in Chart.chart_data[x]]

            wedges, _ = Chart.subplot.pie(sizes, radius=radius, colors=colors, wedgeprops=dict(width=wedge_width, edgecolor='w'))
            Chart.wedge_series.append(wedges)

        Chart.annotation = Chart.subplot.annotate("", xy=(0, 0), xycoords="figure pixels", xytext=(20, 20), textcoords="offset points",
                                 bbox=dict(boxstyle="round", fc="w"),
                                 arrowprops=dict(arrowstyle="->"))
        Chart.annotation.set_visible(False)

        Chart.figure.canvas.mpl_connect("motion_notify_event", Chart._hover)

        plt.show()

    @staticmethod
    def _parse_tree(tree):
        chart_data = []

        node_list = [tree.root]
        while node_list:

            for n in node_list:
                if n.children:
                    break
            else:
                break

            children_flat_list = []
            wedge_info = []
            for node in node_list:
                wedge_info.extend([WedgeData(n.name, n.size_kb, numpy.random.rand(3, )) for n in node.children])
                children_sizes = [node.size_kb for node in node.children]

                filling_space = node.size_kb - sum(children_sizes)
                if filling_space > 0:
                    wedge_info.append(WedgeData('filler', filling_space, (0, 0, 0, 0), is_filler=True))

                if node.children:
                    children_flat_list.extend(node.children)
                else:
                    children_flat_list.append(node)

            node_list = children_flat_list

            if node_list:
                chart_data.append(wedge_info)

        return chart_data

    @staticmethod
    def _update_annotation(pos, description):
        Chart.annotation.xy = pos
        Chart.annotation.set_text(description)
        Chart.annotation.get_bbox_patch().set_alpha(0.4)

    @staticmethod
    def _hover(event):
        if event.inaxes == Chart.subplot:
            pos = [event.x, event.y]
            for series_index, wedges in enumerate(Chart.wedge_series):
                for wedge_index, w in enumerate(wedges):
                    if w.contains_point(pos) and not Chart.chart_data[series_index][wedge_index].is_filler:
                        description = Chart.chart_data[series_index][wedge_index].description
                        Chart._update_annotation(pos, description)
                        Chart.annotation.set_visible(True)
                        Chart.figure.canvas.draw_idle()
                        return
                    else:
                        Chart.annotation.set_visible(False)
            Chart.figure.canvas.draw_idle()
