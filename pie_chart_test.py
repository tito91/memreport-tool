import matplotlib.pyplot as plt

fig, ax = plt.subplots()

wedges, _ = ax.pie([1, 1, 1], wedgeprops=dict(width=0.3))

annotation = ax.annotate("", xy=(0, 0), xycoords="figure pixels", xytext=(20, 20), textcoords="offset points",
                         bbox=dict(boxstyle="round", fc="w"),
                         arrowprops=dict(arrowstyle="->"))
annotation.set_visible(False)


def update_annot(wedge, pos):
    annotation.xy = pos
    annotation.set_text('NAME')
    annotation.get_bbox_patch().set_alpha(0.4)


def hover(event):
    if event.inaxes == ax:
        pos = [event.x, event.y]
        for i, w in enumerate(wedges):
            if w.contains_point(pos):
                update_annot(w, pos)
                annotation.set_visible(True)
                break
            else:
                annotation.set_visible(False)
        fig.canvas.draw_idle()


fig.canvas.mpl_connect("motion_notify_event", hover)

plt.show()
