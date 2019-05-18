import matplotlib.pyplot as plt

fig, ax = plt.subplots()

size = 0.3
values = [[60., 32., 30.], [37., 40., 40, 20], [29.]]
flat_values = [item for sublist in values for item in sublist]

sums = [sum(series) for series in values]

ax.pie(sums, radius=1, wedgeprops=dict(width=size, edgecolor='w'))

ax.pie(flat_values, radius=1 - size,
       wedgeprops=dict(width=size, edgecolor='w'))

plt.show()
