import itertools
from lib_naloga1 import sample_distance
from lib_naloga1 import nesttools

# average_linkage: return average distance between samples in group c1 and samples in group c2.
def average_linkage(c1, c2, data):
	c1_elements = list(nesttools.un_nest(c1)) # Get elements in groups c1 and c2.
	c2_elements = list(nesttools.un_nest(c2))
	prod = itertools.product(c1_elements, c2_elements) 	# Get cartesian product of elements from the groups.

	# Create accumulator for measuring the sum of distances of pairs in cartesian product.
	total_dist = 0
	for pair in prod:
		pair_fst_data = data[pair[0]] # Get data for countries in pair.
		pair_snd_data = data[pair[1]]
		dist = sample_distance.euclidean_dist(pair_fst_data, pair_snd_data) # Compute distance and add to total.
		total_dist += dist

	# Return average distance between elements of groups.
	return total_dist / (len(c1_elements) * len(c2_elements))
		
# complete_linkage: return maximal distance between two samples where first sample is in group c1 and second sample in group c2.
def complete_linkage(c1, c2, data):
	c1_elements = list(nesttools.un_nest(c1))	# Get elements in groups c1 and c2.
	c2_elements = list(nesttools.un_nest(c2))

	# Get list of of data for each country in each group.
	c1_data = list(map(lambda x: data[x], c1_elements))
	c2_data = list(map(lambda x: data[x], c1_elements))

	# Initialize max distance to 0.
	max_dist = 0

	# Find max distance between samples in different groups.
	for c1_sample in c1_data:
		for c2_sample in c2_data:
			dist = sample_distance.euclidean_dist(c1_sample, c2_sample)
			if dist > max_dist: 			# If distance is new maximal distance...
				max_dist = dist

	# Return found maximal distance
	return max_dist

# single_linkage: return minimal distance between two samples where first sample is in group c1 and second sample in group c2.
def single_linkage(c1, c2, data):
	c1_elements = list(nesttools.un_nest(c1)) # Get elements in groups c1 and c2.
	c2_elements = list(nesttools.un_nest(c2))

	# Get list of of data for each country in each group.
	c1_data = list(map(lambda x: data[x], c1_elements))
	c2_data = list(map(lambda x: data[x], c1_elements))

	# Initialize min distance to a very large value.
	min_dist = int(1e20)

	# Find max distance between samples in different groups.
	for c1_sample in c1_data:
		for c2_sample in c2_data:
			dist = sample_distance.euclidean_dist(c1_sample, c2_sample)
			if dist < min_dist: 	# If distance is new minimal distance...
				min_dist = dist

	# Return found maximal distance
	return min_dist