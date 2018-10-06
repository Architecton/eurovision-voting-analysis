from naloga1 import HierarchicalClustering, read_file

########################
# Author: Jernej Vivod #
########################

DATA_FILE = "eurovision-final.csv"					# Read data.
hc = HierarchicalClustering(read_file(DATA_FILE)) 	# Create a HierarchicalClustering instance initialized with parsed data.

# Get groups and create a dictionary where index of groups maps to its members
hc.get_groups(9)
hc.extract_group_members()

# TODO: For each group in hc.groups compute how many points it gave to every other group in hc.groups (make a nxn matrix).
