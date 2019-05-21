import matplotlib.pyplot as plt

from src.memreport import MemReport
import numpy


def flatten_one_level(container):
    return [item for sublist in container for item in sublist]


memreport = MemReport('src/example.memreport', 20)
root = memreport.tree.root

chart_data = []

node_list = [root]
while node_list:

    for n in node_list:
        if n.children:
            break
    else:
        break

    children_flat_list = []
    sizes = []
    colors = []
    for node in node_list:
        children_sizes = [node.size_kb for node in node.children]

        sizes.extend(children_sizes)
        colors.extend([numpy.random.rand(3,) for x in range(len(children_sizes))])
        filling_space = node.size_kb - sum(children_sizes)
        if filling_space > 0:
            sizes.append(filling_space)
            colors.append((0, 0, 0, 0))

        if node.children:
            children_flat_list.extend(node.children)
        else:
            children_flat_list.append(node)

    node_list = children_flat_list

    if node_list:
        chart_data.append(zip(sizes, colors))


fig, ax = plt.subplots()

outer_size = 1.5
inner_size = 0.2

axis_count = len(chart_data)
wedge_width = (outer_size - inner_size) / (axis_count + 1)

for x in range(axis_count):
    radius = outer_size - x * wedge_width
    sizes, colors = zip(*chart_data[x])

    ax.pie(sizes, radius=radius, colors=colors, wedgeprops=dict(width=wedge_width, edgecolor='w'))

plt.show()
