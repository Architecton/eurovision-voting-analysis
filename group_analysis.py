from naloga1 import HierarchicalClustering, read_file, get_labels
import numpy as np
import matplotlib.pyplot as plt

# Analysis of the results of hierarchical clustering

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

## (1) ## For each group in hc.groups compute how many points it gave to every country. ##

points_to_countries = dict()

# Go over group indices.
for group_index in hc.groups.keys():
	sum_points = np.zeros(47, dtype = int) 						# Create empty vector for computing the cummulative sums of points for each country.
	for country in hc.groups[group_index]: 						# Compute commulative sums.
		sum_points = np.add(sum_points, hc.data[country])
	sum_points = np.true_divide(sum_points, sum(sum_points)) 	# Compute proportion of points given to each country.
	points_to_countries[group_index] = sum_points 				# Add entry to results dict.s


## (2) ## For each group in hc.groups compute how many points it gave to every region. ##

points_to_regions = dict()

# Go over group indices.
for group_index in hc.groups.keys():
	sum_points = np.zeros(47, dtype = int) 		# Create empty vector for computing the cummulative sums of points for each country.
	for country in hc.groups[group_index]: 		# Compute commulative sums.
		sum_points = np.add(sum_points, hc.data[country])

	points = dict() 							# points: dict that maps group index to dict of points ratios for each region.

	for region in set(labels[1,:]): 			# Go over regions and initialize values pointed by region names (keys) to 0.
		points[region] = 0

	for index, country in enumerate(labels[0, :]): 		# Compute cummulative sum for each region
		points[labels[1, index]] += sum_points[index]

	for key in points.keys(): 							# Compute ratios of points to each region.
		points[key] /= sum(sum_points)
	
	points_to_regions[group_index] = points 			# Add computed dict to points_to_regions dict.


## (3) ## For each group in hc.groups compute how many points it gave to every other group in hc.groups (make a nxn matrix and a heatmap). ##

points_to_groups = dict()

# Go over group indices.
for group_index in hc.groups.keys():
	sum_points = np.zeros(47, dtype = int) 					# Create empty vector for computing the cummulative sums of points for each country.
	for country in hc.groups[group_index]: 					# Compute cummulative sums.
		sum_points = np.add(sum_points, hc.data[country])

	points_to_other_groups = dict() 						# points_to_other_groups: dict that maps group index to points ratios for each other group.
	for key in hc.groups.keys(): 							# Initialize all values pointed by group indices to 0.
		points_to_other_groups[key] = 0

	for index, country in enumerate(labels[0, :]): 			# Compute commulative sum of points awarded to each group by group with index group_index.
		for key in hc.groups.keys():
			if country in hc.groups[key]:
				points_to_other_groups[key] += sum_points[index]

	for key in points_to_other_groups.keys(): 				# Compute ratios.
		points_to_other_groups[key] /= sum(sum_points)

	points_to_groups[group_index] = points_to_other_groups 	# Add computed dict to points_to_regions dict.


# Compute total proportion of points to each region.
total = np.zeros(len(hc.data.keys()), dtype = int)

# Get cummulative sum of points for each country.
for key in hc.data.keys():
	total = np.add(total, hc.data[key])

# Create a dict for storing the total region ratios and initialize each region to 0.
total_region_ratios = dict()
for region in set(labels[1,:]):
	total_region_ratios[region] = 0

# Compute cummulative sum for each region.
for index, country in enumerate(labels[0, :]):
	total_region_ratios[labels[1, index]] += total[index]

# Get ratios.
for key in total_region_ratios.keys():
	total_region_ratios[key] /= sum(total)



# plot_dict: plot a dictionary as a bar plot with key on the x axis and value mapped by the key on the y axis.
def plot_dict(data_dict, suptitle, threshold):
	plt.figure() 												# Create new figure.
	for i in range(1, len(data_dict.keys()) + 1): 				# Plot each dict entry in own subplot.
		plt.subplot(3, 4, i)
		b = plt.bar(range(len(data_dict[i-1])), list(data_dict[i-1].values())) 	# Plot values.

		# If keys are of string type, split into multiply lines by replacing space characters with newline characters
		if isinstance(list(data_dict[i-1].keys())[0], str):
			labs = list(map(lambda x: x.replace(' ', '\n'), list(data_dict[i-1].keys())))

			# Color bars which represent values that are a certain threshold above or below the total mean.
			for index, key in enumerate(data_dict[i-1].keys()):
				if data_dict[i-1][key] > total_region_ratios[key] + threshold:
					b[index].set_color('darkorange')
				elif data_dict[i-1][key] < total_region_ratios[key] - threshold:
					b[index].set_color('darkgreen')

		else:
			labs = list(data_dict[i-1].keys())

		# Add x axis ticks.
		plt.xticks(range(len(data_dict[i-1])), labs, fontsize = 8)

		# Add y labels to leftmost subplots.
		if i in {1, 5, 9}:
			plt.ylabel("proportion of points given")

		plt.title("Group {0}".format(i - 1)) 					# Add title to subplot

	# Adjust margins.
	plt.subplots_adjust(left=0.05, bottom=None, right=0.98, top=None, wspace=None, hspace=0.3)
	plt.suptitle(suptitle, fontsize = 25) 						# Add title to main plot.


# Delete "not listed" key from data dict for points to regions by groups data dist (countries with region "not listed" only vote and do not participate).
for key in points_to_regions.keys():
	del points_to_regions[key]["not listed"]

# Plot distributions of point ratios among regions for each group.
plot_dict(points_to_regions, "Proportion of Points Given to Each Region by Each Group", 0.1)

# Plot the total proportion of votes to each region.
plt.subplot(3, 4, 12)
del total_region_ratios["not listed"]
b = plt.bar(range(len(total_region_ratios)), list(total_region_ratios.values()), color = "darkred")
plt.xticks(range(len(total_region_ratios)), list(map(lambda x: x.replace(' ', '\n'), list(total_region_ratios.keys()))), fontsize = 8)
plt.title("Proportions of All Votes")
plt.show()


# Plot distribution of point ratios among other groups for each groups.
plot_dict(points_to_groups, "Proportion of Points Given to Each Group by Each Group", 0.1)