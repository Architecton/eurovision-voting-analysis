def inject_distances(clusters, distances):
	for clust_d in distances:
		inject(clust_d[0], clust_d[1], clusters)
	clusters.insert(0, distances[len(distances) - 1][1])

def inject(cluster, distance, clusters):
	for index, c in enumerate(clusters):
		if c == cluster:
			clusters[index] = [distance] + clusters[index]
		elif isinstance(c, list):
			inject(cluster, distance, c)