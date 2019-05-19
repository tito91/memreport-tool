import matplotlib.pyplot as plt

from src.texture_info_tree import TextureInfoTree


def flatten_one_level(container):
    return [item for sublist in container for item in sublist]


root = TextureInfoTree.make_sample()

chart_data = []

node_list = [root]
while node_list:
    children_tuples = [node.children for node in node_list]
    children_flat = flatten_one_level(children_tuples)
    sizes = [node.size_kb for node in children_flat]

    node_list = children_flat

    if node_list:
        chart_data.append(sizes)


fig, ax = plt.subplots()

outer_size = 1.5
inner_size = 0.2

wedge_width = (outer_size - inner_size) / (len(chart_data) + 1)

for x in range(len(chart_data)):
    radius = outer_size - x * wedge_width
    ax.pie(chart_data[x], radius=radius, wedgeprops=dict(width=wedge_width, edgecolor='w'))

plt.show()
