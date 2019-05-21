import matplotlib.pyplot as plt

from src.memreport import MemReport
import numpy

from src.wedge_data import WedgeData


mem_report = MemReport('src/example.memreport', size_threshold=20)
root = mem_report.tree.root

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
        wedge_info.extend([WedgeData(n.name, n.size_kb, numpy.random.rand(3,)) for n in node.children])
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


fig, ax = plt.subplots()

outer_size = 1.25
inner_size = 0.2

axis_count = len(chart_data)
wedge_width = (outer_size - inner_size) / (axis_count + 1)

wedge_series = []

for x in range(axis_count):
    radius = outer_size - x * wedge_width
    sizes = [d.size_kb for d in chart_data[x]]
    colors = [d.color for d in chart_data[x]]

    wedges, _ = ax.pie(sizes, radius=radius, colors=colors, wedgeprops=dict(width=wedge_width, edgecolor='w'))
    wedge_series.append(wedges)

annotation = ax.annotate("", xy=(0, 0), xycoords="figure pixels", xytext=(20, 20), textcoords="offset points",
                         bbox=dict(boxstyle="round", fc="w"),
                         arrowprops=dict(arrowstyle="->"))
annotation.set_visible(False)


def update_annotation(pos, description):
    annotation.xy = pos
    annotation.set_text(description)
    annotation.get_bbox_patch().set_alpha(0.4)


def hover(event):
    if event.inaxes == ax:
        pos = [event.x, event.y]
        for serie_index, wedges in enumerate(wedge_series):
            for wedge_index, w in enumerate(wedges):
                if w.contains_point(pos) and not chart_data[serie_index][wedge_index].is_filler:
                    description = chart_data[serie_index][wedge_index].description
                    update_annotation(pos, description)
                    annotation.set_visible(True)
                    fig.canvas.draw_idle()
                    return
                else:
                    annotation.set_visible(False)
        fig.canvas.draw_idle()


fig.canvas.mpl_connect("motion_notify_event", hover)

plt.show()
