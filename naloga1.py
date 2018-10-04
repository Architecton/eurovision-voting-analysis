import csv
import numpy as np
import itertools
import group_distance
import sample_distance

# Parsing the data file - notes:
"""
	Rows are countries (columns in original file (Q - BK / 17 - 63/) - 47 columns)
	in list comprehension: l[0][16:63] # select names of countries -> keys

	Note that country names are sometimes ended with a space -> trim.

	For each country A:
		- Make bins corresponding to each other country i.
		- In each bin, sum votes from country A for this country i.

	Summing votes for each country i from country A:
		- There are 47 countries voting.
		- Make a tuple of names of countries (column names 17 - 63).
		- Indices of names of countries are also indices in the bins list.
		- Go over all rows representing votes.
		- Get name (and from name, the index) from row name.
		- Add value in row to appropriate bin.
		- Add entry to data dict.
"""

# Read and process data to be used for clustering.
# param file_name: name of the file containing the data
# return: dictionary with element names as keys and feature vectors as values
def read_file(file_name):
	# Open data file
	with open(file_name, "rt", encoding="latin1") as f:
		raw_data = np.array(list(csv.reader(f))) 											# Read lines from csv file into numpy array
		country_names = raw_data[0, 16:63] 													# Get names of countries (as names of rows 17-63)
		country_names = list(map(lambda x: x.strip(), country_names)) 						# Trim whitespace from start and end.
		country_names[country_names.index("Serbia & Montenegro")] = "Serbia and Montenegro" # Handle country name conflict between name in rows and name in columns
		processed_data = dict() 															# Create empty dictionary for storing cleaned data.
		NUM_COUNTRIES = 47 																	# There are 47 countries participating/voting.
		col_names = list(map(lambda x: x.strip(), raw_data[0, :])) 							# Get names of columns.
		col_names[col_names.index("Serbia & Montenegro")] = "Serbia and Montenegro" 		# Handle country name conflict between name in rows and name in columns.

		# Create rows in processed data matrix.
		for country in country_names:
			bins = np.zeros((NUM_COUNTRIES, ), dtype = int) 		# Create bins.
			index_row = col_names.index(country) 					# Get index of column representing votes from this country.

			# Go over performing countries across all years.
			for i in range(1, raw_data.shape[0]):
				bin_index = country_names.index(raw_data[i, 1].strip()) 	# Compute index of bin for next performance
				val = raw_data[i, index_row] 								# Get number of points awarded by country A (If data exists).
				try:
					points = int(val) 								# Try to convert value to an integer.
					bins[bin_index] += points 						# If successfully converted, add to bin.
				except ValueError:
					pass
			processed_data[country] = bins 							# Add country data to dictionary representing the processed data.

		# Return dictionary representing the processed data
		return processed_data

# get_labels: get a 2 by 47 matrix where the first row contains the country names and the second row their regions
# obtained from the third column in the original data sheet.
# This matrix is used as a label for the data matrix obtained by the read_file function (the indices match).
def get_labels(file_name):
	with open(file_name, "rt", encoding="latin1") as f:
		raw_data = np.array(list(csv.reader(f))) 											# Read lines from csv file into numpy array
		country_names = raw_data[0, 16:63] 													# Get names of countries (as names of rows 17-63)
		country_names = list(map(lambda x: x.strip(), country_names)) 						# Trim whitespace from start and end.
		country_names[country_names.index("Serbia & Montenegro")] = "Serbia and Montenegro" # Handle country name conflict between name in rows and name in columns
		country_regions = [] 																# define list that will store regions of countries in country_names list with same index.
		countries = list(raw_data[1:, 1]) 													# All rows of columns with countries and regions (performances)
		regions = raw_data[1:, 2]

		# Make a set of countries that do not appear
		with_unlisted_regions = {"Andorra", "Czech Republic", "Monaco", "Montenegro", "San Marino"} 

		# Get regions for each country.
		for country in country_names:
			if country in with_unlisted_regions:
				country_regions.append("not listed")
			else:
				index_country = countries.index(country) # Get index of country and use it to get region.
				region = regions[index_country]
				country_regions.append(region)

		# Return matrix where the first row contains the country names and the second row their regions
		return np.stack((country_names, country_regions))


# HierarchicalClustering: class implementing hierarchical clustering functionalities
class HierarchicalClustering:

	# constructor: assign parsed data and create initial clusters where each row is its own data.
	def __init__(self, data):
		# Initialize clustering
		self.data = data
		# self.clusters stores current clustering.
		self.clusters = [[name] for name in self.data.keys()]


	# row_distance: compute distance between data in two rows.
	# Example call: self.row_distance("Polona", "Rajko")
	def row_distance(self, r1, r2):

		# use euclidean distance as similarity measure.
		# change value to "manhattan" to use the manhattan distance.
		distance_meas = "euclidean"

		# similarity: check similarity of samples sample_1 and sample_2 using algorithm provided by function func.
		def similarity(sample_1, sample_2, func):
			return func(sample_1, sample_2)

		# Try to read data from specified rows (data accessed by key)
		try:
			r1_data = self.data[r1]
			r2_data = self.data[r2]
		except KeyError("Specified row not found."):
			pass

		# Select distance measuring function to use depending on the value of
		# distance_meas variable.
		distance_func = None
		if distance_meas == "euclidean":
			distance_func = sample_distance.euclidean_dist
		elif distance_meas == "manhattan":
			distance_func = sample_distance.manhattan_dist

		# Compute and return similarity between the rows using the specified distance.
		return distance_func(r1_data, r2_data)

	# cluster_distance: compute distance between two clusters. Each cluster is specified as a list of lists where each list is itself a cluster.
	# Example call: self.cluster_distance([[["Albert"], ["Branka"]], ["Cene"]], [["Nika"], ["Polona"]])
	def cluster_distance(self, c1, c2):
		# Use average linkage as a distance measurement. Change value to
		# "complete" to use complete linkage measurement or use "single" to use single linkage distance measurement.
		distance_meas = "average"

		# Set distance measuring function according to distance_meas variable value.
		distance_func = None
		if distance_meas == "average":
			distance_func = group_distance.average_linkage
		elif distance_meas == "complete":
			distance_func = group_distance.complete_linkage
		elif distance_meas == "single":
			distance_func = group_distance.single_linkage
		else:
			raise ValueError("Invalid group distance measuring function")
		
		# Compute distance between clusters.
		return distance_func(c1, c2, self.data)


	# Find a pair of closest clusters and returns the pair of clusters and their distance.
	# Example call: self.closest_clusters(self.clusters)
	def closest_clusters(self):

		min_dist = int(1e20) 		# initialize minimal distance to a very large number.
		closest_clusters = None 	# Initialize closest cluster pair to None
		for cluster_pair in itertools.product(self.clusters, self.clusters): 	# Go over pairs of clusters and find pair with minimum distance.
			if cluster_pair[0] != cluster_pair[1]:
				dist = self.cluster_distance(cluster_pair[0], cluster_pair[1])
				if dist < min_dist:
					min_dist = dist
					closest_clusters = cluster_pair

		return closest_clusters, min_dist


	# TODO - 5.10.2018-7.10.2018 ###

	# Given the data in self.data, performs hierarchical clustering. Can use a while loop, iteratively modify self.clusters and store
	# information on which clusters were merged and what was the distance. Store this later information into a suitable structure to be used
	# for plotting of the hierarchical clustering.
	def run(self):
		# TODO
		pass

	# Use cluster information to plot an ASCII representation of the cluster tree.
	def plot_tree(self):
		# TODO
		pass

	#################################

"""
# If running this file as a script
if __name__ == "__main__":

	# Read data.
	DATA_FILE = "eurovision-final.csv"

	# Create a HierarchicalClustering instance initialized with parsed data.
	hc = HierarchicalClustering(read_file(DATA_FILE))

	# Perform clustering
	hc.run()

	# Plot results of clustering.
	hc.plot_tree()
"""

if __name__ == "__main__":
	file_name = "eurovision-final.csv"
	data = read_file(file_name)
	labels = get_labels(file_name)
	hc = HierarchicalClustering(read_file(file_name))
	row_dist_ex = hc.row_distance("Slovenia", "Norway")
	cluster1 = ["Slovenia", "Austria", "Norway"]
	cluster2 = ["Serbia", "Croatia", "France"]
	cluster_dist_ex = hc.cluster_distance(cluster1, cluster2)
	closest = hc.closest_clusters()