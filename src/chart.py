import numpy

from src.wedge_data import WedgeData

import matplotlib.pyplot as plt


class Chart:
    inner_size = 0.2
    outer_size = 1.25

    figure = None
    subplot = None
    wedge_annotation = None
    chart_data = None
    wedge_series = None
    background = None
    draw_cid = None

    @staticmethod
    def from_report(report):
        Chart.chart_data = Chart._parse_tree(report.tree)

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

        Chart.wedge_annotation = Chart.subplot.annotate("", xy=(0, 0), xycoords="figure pixels", xytext=(20, 20), textcoords="offset points",
                                                        bbox=dict(boxstyle="round", fc="w"),
                                                        arrowprops=dict(arrowstyle="->"))
        Chart.wedge_annotation.set_visible(False)

        if report.size_threshold:
            size_threshold_text = 'Size threshold in use. Total size of files under threshold: {}kb'.format(report.under_threshold_total_size)
            threshold_annotation = Chart.subplot.annotate(size_threshold_text, xy=(0, 0), xycoords="figure pixels",
                                                          xytext=(20, 20), textcoords="offset points",
                                                          bbox=dict(boxstyle="round", fc="w"))
            threshold_annotation.set_visible(True)

        Chart.background = Chart.figure.canvas.copy_from_bbox(Chart.subplot.bbox)

        Chart.figure.canvas.mpl_connect("motion_notify_event", Chart._hover)

        Chart.draw_cid = Chart.figure.canvas.mpl_connect('draw_event', Chart.grab_background)

        plt.show()

    @staticmethod
    def grab_background(event=None):
        Chart.safe_draw()

        Chart.background = Chart.figure.canvas.copy_from_bbox(Chart.figure.bbox)
        Chart.blit()

    @staticmethod
    def blit():
        Chart.figure.canvas.restore_region(Chart.background)
        Chart.subplot.draw_artist(Chart.wedge_annotation)
        Chart.figure.canvas.blit(Chart.figure.bbox)

    @staticmethod
    def safe_draw():
        canvas = Chart.figure.canvas
        canvas.mpl_disconnect(Chart.draw_cid)
        canvas.draw()
        Chart.draw_cid = canvas.mpl_connect('draw_event', Chart.grab_background)

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
        Chart.wedge_annotation.xy = pos
        Chart.wedge_annotation.set_text(description)
        Chart.wedge_annotation.get_bbox_patch().set_alpha(0.4)

    @staticmethod
    def _hover(event):
        if event.inaxes == Chart.subplot:
            pos = [event.x, event.y]
            for series_index, wedges in enumerate(Chart.wedge_series):
                for wedge_index, w in enumerate(wedges):
                    if w.contains_point(pos) and not Chart.chart_data[series_index][wedge_index].is_filler:
                        description = Chart.chart_data[series_index][wedge_index].description
                        Chart._update_annotation(pos, description)
                        Chart.wedge_annotation.set_visible(True)
                        Chart.blit()
                        return
                    else:
                        Chart.wedge_annotation.set_visible(False)
            Chart.blit()
