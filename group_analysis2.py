from naloga1 import HierarchicalClustering, read_file, get_labels
import numpy as np
########################
# Author: Jernej Vivod #
########################

DATA_FILE = "eurovision-final.csv"					# Read data.
labels = get_labels(DATA_FILE) 						# Get labels (2xn matrix) that maps each country in first column to its region
													# in the second column

hc = HierarchicalClustering(read_file(DATA_FILE)) 	# Create a HierarchicalClustering instance initialized with parsed data.

# Get groups and create a dictionary where index of groups maps to its members
hc.get_groups(11)
hc.extract_group_members()

# For each group in hc.groups compute how many points it gave to every country.
points_to_countries = dict()

for group_index in hc.groups.keys():
	sum_points = np.zeros(47, dtype = int)
	for country in hc.groups[group_index]:
		sum_points = np.add(sum_points, hc.data[country])
	sum_points = np.true_divide(sum_points, len(hc.groups[group_index]))
	points_to_countries[group_index] = sum_points
### TODO: Create a barplot (many on same plot) showing the number of points given to each country by each group.


# TODO: For each group in hc.groups compute how many points it gave to every region.
points_to_regions = dict()

for group_index in hc.groups.keys():
	sum_points = np.zeros(47, dtype = int)
	for country in hc.groups[group_index]:
		sum_points = np.add(sum_points, hc.data[country])

	points = dict()

	for region in set(labels[1,:]):
		points[region] = 0

	for index, country in enumerate(labels[0, :]):
		points[labels[1, index]] += sum_points[index]

	for key in points.keys():
		points[key] /= sum(sum_points)
	
	points_to_regions[group_index] = points

### TODO: Create a barplot (many on same plot) showing the number of points given to each country by each group.	
## USE THE plot_dict MODULE

# TODO: For each group in hc.groups compute how many points it gave to every other group in hc.groups (make a nxn matrix and a heatmap).

points_to_groups = dict()

for group_index in hc.groups.keys():
	sum_points = np.zeros(47, dtype = int)
	for country in hc.groups[group_index]:
		sum_points = np.add(sum_points, hc.data[country])

	points_to_other_groups = dict()
	for key in hc.groups.keys():
		points_to_other_groups[key] = 0

	for index, country in enumerate(labels[0, :]):
		for key in hc.groups.keys():
			if country in hc.groups[key]:
				points_to_other_groups[key] += sum_points[index]

	for key in points_to_other_groups.keys():
		points_to_other_groups[key] / sum(sum_points)

	points_to_groups[group_index] = points_to_other_groups


import matplotlib.pyplot as plt
def plot_dict(data_dict):
	r = plt.figure()
	for i in range(1, len(data_dict.keys()) + 1):
		plt.subplot(3, 4, i)
		plt.bar(range(len(data_dict[i-1])), list(data_dict[i-1].values()))
		if isinstance(list(data_dict[i-1].keys())[0], str):
			labs = list(map(lambda x: x.replace(' ', '\n'), list(data_dict[i-1].keys())))
		else:
			labs = list(data_dict[i-1].keys())

		plt.xticks(range(len(data_dict[i-1])), labs, fontsize = 8)
		if i in {1, 5, 9}:
			plt.ylabel("proportion of points given")

		plt.title("Group {0}".format(i - 1))

	# plt.tight_layout(pad=0.01, w_pad=0.01, h_pad=0.01)
	plt.subplots_adjust(left=0.05, bottom=None, right=0.98, top=None, wspace=None, hspace=0.3)
	plt.suptitle("Proportion of Points Given to Each Region by Each Group", fontsize = 25)
	plt.show()

for key in points_to_regions.keys():
	del points_to_regions[key]["not listed"]

plot_dict(points_to_regions)

plot_dict(points_to_groups)