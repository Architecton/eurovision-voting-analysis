import matplotlib.pyplot as plt

plt.bar(range(len(points_to_regions[7])), list(points_to_regions[7].values()), align='center')
plt.xticks(range(len(points_to_regions[7])), list(points_to_regions[7].keys()))
plt.show()

plt.bar(range(len(points_to_groups[7])), list(points_to_groups[7].values()), align='center')
plt.xticks(range(len(points_to_groups[7])), list(points_to_groups[7].keys()))
plt.show()
