import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()

size = 0.3
vals = np.array([[60., 32.], [37., 40.], [29., 10.]])

cmap = plt.get_cmap("tab20c")
outer_colors = cmap(np.arange(3)*4)
inner_colors = cmap(np.array([1, 2, 5, 6, 9, 10]))

wedge_series = []

wedges, _ = ax.pie(vals.sum(axis=1), radius=1, colors=outer_colors,
       wedgeprops=dict(width=size, edgecolor='w'))

wedge_series.append(wedges)


wedges, _ = ax.pie(vals.flatten(), radius=1-size, colors=inner_colors,
       wedgeprops=dict(width=size, edgecolor='w'))

wedge_series.append(wedges)

wedges, _ = ax.pie(vals.flatten(), radius=1-2*size, colors=inner_colors,
       wedgeprops=dict(width=size, edgecolor='w'))

wedge_series.append(wedges)


annotation = ax.annotate("", xy=(0, 0), xycoords="figure pixels", xytext=(20, 20), textcoords="offset points",
                         bbox=dict(boxstyle="round", fc="w"),
                         arrowprops=dict(arrowstyle="->"))
annotation.set_visible(False)


def update_annot(pos):
    annotation.xy = pos
    annotation.set_text('NAME')
    annotation.get_bbox_patch().set_alpha(0.4)


def hover(event):
    if event.inaxes == ax:
        pos = [event.x, event.y]
        for wsi, serie in enumerate(wedge_series):
            for i, w in enumerate(serie):
                if w.contains_point(pos):
                    update_annot(pos)
                    annotation.set_visible(True)
                    fig.canvas.draw_idle()
                    return
                else:
                    annotation.set_visible(False)
            fig.canvas.draw_idle()


fig.canvas.mpl_connect("motion_notify_event", hover)

plt.show()
