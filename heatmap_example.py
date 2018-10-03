# Write a program that outputs a heatmap matrix of the similarities between measurements.
# Compute the similarities using either the euclidean distance or the manhattan distance.

# The data matrix is given in the file data.txt
import numpy as np
import matplotlib.pyplot as plt
import math

# Get matrix from file.
data = np.genfromtxt("data.txt", delimiter="   ")

# get_heat_map: get heat map of similarities between samples
# using either euclidean distance or manhattan distance as a similarity measure.
def get_heat_map(data, method):
	# Check for validity of computing method specification.
	if method not in {'euclidean', 'manhattan'}:
		raise ValueError("Invalid argument: " + str(method))

	# similarity: check similarity of samples sample_1 and sample_2 using algorithm
	# provided by function func.
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

	# allocate empty matrix for heat map.
	heat_map = np.zeros((len(data), len(data)))

	# Compare every sample with every other sample and save result in corresponding heat map cell.
	for i in range(len(data)):
		for j in range(len(data)):
			heat_map[i][j] = similarity(data[i], data[j], euclidean_dist if method == 'euclidean' else manhattan_dist);

	# return the computed heat map.
	return heat_map

# Get result.
heat_map = get_heat_map(data, 'euclidean')

# Plot heatmap.
plt.imshow(heat_map, cmap='hot', interpolation='nearest')
plt.show()