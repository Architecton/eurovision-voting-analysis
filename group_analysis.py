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
hc.get_groups(9)
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
	num_votes = dict()

	for region in set(labels[1,:]):
		points[region] = 0
		num_votes[region] = 0

	for index, country in enumerate(labels[0, :]):
		points[labels[1, index]] += sum_points[index]
		num_votes[labels[1, index]] += 1

	#for key in points.keys():
	#	points[key] /= num_votes[key]
	
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
	num_votes = dict()
	for key in hc.groups.keys():
		points_to_other_groups[key] = 0
		num_votes[key] = 0

	for index, country in enumerate(labels[0, :]):
		for key in hc.groups.keys():
			if country in hc.groups[key]:
				points_to_other_groups[key] += sum_points[index]
				num_votes[key] += 1

	for key in points_to_other_groups.keys():
		points_to_other_groups[key] /= num_votes[key]

	points_to_groups[group_index] = points_to_other_groups
