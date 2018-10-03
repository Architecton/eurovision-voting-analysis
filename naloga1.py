import csv

# Read and process data to be used for clustering.
# param file_name: name of the file containing the data
# return: dictionary with element names as keys and feature vectors as values
def read_file(file_name):
	pass
	# See data_parsing.py

# get_labels: get a 2 by 47 matrix where the first row contains the country names and the second row their regions
# obtained from the third column in the original data sheet.
# This matrix is used as a label for the data matrix obtained by the read_file function (the indices match).
def get_labels(file_name):
	pass
	# See data_parsing.py

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

		# euclidean_dist: compute similarity between samples sample_1 and sample_2 by means of their euclidean distance.
		def euclidean_dist(sample_1, sample_2):
			# Sum squares of differences.
			sum_squares = 0
			for i in range(len(sample_1)):
				sum_squares += (sample_1[i] - sample_2[i])**2;

			# Take square root of sum.
			sum_squares = math.sqrt(sum_squares)

			return sum_squares

		# manhattan_dist: compute similarity between samples sample_1 and sample_2 by means of their manhattan distance.
		def manhattan_dist(sample_1, sample_2):
			sum_abs = 0
			for i in range(len(sample_1)):
				sum_abs += abs(sample_1[i] - sample_2[i])

			return sum_abs


		"""
		Distance between two rows.
		Implement either Euclidean or Manhattan distance.
		
		"""

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
			dist_func = euclidean_dist
		elif distance_meas == "manhattan":
			dist_func = manhattan_dist

		# Compute and return similarity between the rows using the specified distance.
		return similarity(r1_data, r2_data, distance_func)


	# cluster_distance: compute distance between two clusters. Each cluster is specified as a list of lists where each list is itself a cluster.
	# Example call: self.cluster_distance([[["Albert"], ["Branka"]], ["Cene"]], [["Nika"], ["Polona"]])
	def cluster_distance(self, c1, c2):
		# Use average linkage as a distance measurement. Change value to
		# "complete" to use complete linkage measurement or use "single" to use single linkage distance measurement.
		distance_meas = "average"
		# TODO
		pass

	# Find a pair of closest clusters and returns the pair of clusters and their distance.
	# Example call: self.closest_clusters(self.clusters)
	def closest_clusters(self):
		# TODO
		pass

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